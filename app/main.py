from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.data.mock_data import USERS, build_dashboard
from app.services.ai import AGENT_CONFIG, AIService

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="矿产贸易企业智能经营平台")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "dev-secret-key-change-me"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
ai_service = AIService()


NAV_ITEMS = [
    {"key": "dashboard", "label": "经营总览", "path": "/dashboard"},
    {"key": "market", "label": "市场行情", "path": "/market"},
    {"key": "procurement", "label": "采购管理", "path": "/procurement"},
    {"key": "production", "label": "生产监测", "path": "/production"},
    {"key": "sales", "label": "销售获客", "path": "/sales"},
    {"key": "agents", "label": "智能 Agent 中枢", "path": "/agents"},
]


def current_user(request: Request):
    username = request.session.get("username")
    if not username or username not in USERS:
        return None
    return {"username": username, **USERS[username]}


def auth_redirect(request: Request):
    if not current_user(request):
        return RedirectResponse("/login", status_code=302)
    return None


def base_context(request: Request, active: str):
    user = current_user(request)
    if not user:
        return None
    data = build_dashboard(user["role"])
    return {
        "request": request,
        "user": user,
        "nav_items": NAV_ITEMS,
        "active_nav": active,
        "data": data,
        "agents": AGENT_CONFIG,
    }


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    if current_user(request):
        return RedirectResponse("/dashboard", status_code=302)
    return RedirectResponse("/login", status_code=302)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = USERS.get(username)
    if not user or user["password"] != password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "用户名或密码错误"}, status_code=400)
    request.session["username"] = username
    return RedirectResponse("/dashboard", status_code=302)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    redirect = auth_redirect(request)
    if redirect:
        return redirect
    return templates.TemplateResponse("dashboard.html", base_context(request, "dashboard"))


@app.get("/market", response_class=HTMLResponse)
def market(request: Request):
    redirect = auth_redirect(request)
    if redirect:
        return redirect
    return templates.TemplateResponse("market.html", base_context(request, "market"))


@app.get("/procurement", response_class=HTMLResponse)
def procurement(request: Request):
    redirect = auth_redirect(request)
    if redirect:
        return redirect
    return templates.TemplateResponse("procurement.html", base_context(request, "procurement"))


@app.get("/production", response_class=HTMLResponse)
def production(request: Request):
    redirect = auth_redirect(request)
    if redirect:
        return redirect
    return templates.TemplateResponse("production.html", base_context(request, "production"))


@app.get("/sales", response_class=HTMLResponse)
def sales(request: Request):
    redirect = auth_redirect(request)
    if redirect:
        return redirect
    return templates.TemplateResponse("sales.html", base_context(request, "sales"))


@app.get("/agents", response_class=HTMLResponse)
def agents_page(request: Request):
    redirect = auth_redirect(request)
    if redirect:
        return redirect
    context = base_context(request, "agents")
    context["agent_result"] = None
    return templates.TemplateResponse("agents.html", context)


@app.post("/agents", response_class=HTMLResponse)
def run_agent(request: Request, agent_key: str = Form(...), user_message: str = Form(...)):
    redirect = auth_redirect(request)
    if redirect:
        return redirect
    context = base_context(request, "agents")
    context["selected_agent"] = agent_key
    context["user_message"] = user_message
    context["agent_result"] = ai_service.run_agent(agent_key, context["data"], user_message)
    return templates.TemplateResponse("agents.html", context)
