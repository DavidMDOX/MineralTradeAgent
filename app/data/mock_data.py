from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any


USERS = {
    "admin": {"password": "admin123", "role": "admin", "name": "系统管理员"},
    "buyer": {"password": "buyer123", "role": "buyer", "name": "采购经理"},
    "sales": {"password": "sales123", "role": "sales", "name": "销售经理"},
    "boss": {"password": "boss123", "role": "boss", "name": "总经理"},
}

ROLE_FOCUS = {
    "admin": {
        "title": "企业中控台",
        "subtitle": "统筹权限、流程、告警与跨模块执行效率",
        "highlights": ["系统健康", "跨部门流程", "权限与审计", "异常告警"],
    },
    "buyer": {
        "title": "采购指挥台",
        "subtitle": "聚焦矿源、到岸成本、交付稳定性与替代供应商",
        "highlights": ["到岸成本", "替代矿源", "交期风险", "库存保障"],
    },
    "sales": {
        "title": "销售获客台",
        "subtitle": "聚焦竞品监控、报价策略、线索质量与成交推进",
        "highlights": ["报价策略", "线索优先级", "竞品波动", "利润空间"],
    },
    "boss": {
        "title": "经营驾驶舱",
        "subtitle": "聚焦利润、现金流、产销协同与市场节奏",
        "highlights": ["利润率", "营运资金", "市场风险", "经营建议"],
    },
}


def build_market_series() -> dict[str, Any]:
    base = date(2025, 12, 1)
    days = [base + timedelta(days=i) for i in range(14)]
    labels = [d.strftime("%m-%d") for d in days]
    lme_copper = [8410, 8432, 8468, 8495, 8518, 8488, 8522, 8560, 8588, 8612, 8596, 8628, 8650, 8676]
    shfe_copper = [69020, 69180, 69320, 69640, 69910, 69780, 70060, 70320, 70550, 70880, 70710, 70950, 71140, 71420]
    inventory = [92800, 91900, 91150, 90500, 89420, 88980, 88020, 87240, 86800, 86050, 85520, 84980, 84500, 83840]
    fx = [7.11, 7.10, 7.10, 7.09, 7.08, 7.08, 7.07, 7.07, 7.06, 7.05, 7.05, 7.04, 7.03, 7.03]
    return {
        "labels": labels,
        "lme_copper": lme_copper,
        "shfe_copper": shfe_copper,
        "inventory": inventory,
        "fx": fx,
        "summary": {
            "lme_latest": lme_copper[-1],
            "lme_change_pct": round((lme_copper[-1] - lme_copper[-5]) / lme_copper[-5] * 100, 2),
            "shfe_latest": shfe_copper[-1],
            "inventory_latest": inventory[-1],
            "inventory_change_pct": round((inventory[-1] - inventory[-5]) / inventory[-5] * 100, 2),
            "fx_latest": fx[-1],
        },
        "events": [
            "虚拟样本：海外铜精矿 TC/RC 延续低位，反映矿端紧张仍未完全缓解。",
            "虚拟样本：华东现货升水回暖，下游在价格回踩后补库意愿提升。",
            "虚拟样本：港口库存继续小幅去化，短期对现货价格形成支撑。",
        ],
    }


def build_suppliers() -> list[dict[str, Any]]:
    return [
        {
            "name": "北岭矿源A",
            "grade": "铜精矿 23%",
            "price": 67650,
            "freight": 780,
            "purity": 92,
            "reliability": 88,
            "lead_time": 6,
            "capacity": 2500,
            "region": "西北",
        },
        {
            "name": "海通资源B",
            "grade": "粗铜 98.5%",
            "price": 69480,
            "freight": 530,
            "purity": 96,
            "reliability": 85,
            "lead_time": 4,
            "capacity": 1800,
            "region": "华东",
        },
        {
            "name": "云川矿贸C",
            "grade": "铜精矿 21%",
            "price": 66880,
            "freight": 960,
            "purity": 89,
            "reliability": 81,
            "lead_time": 8,
            "capacity": 3200,
            "region": "西南",
        },
        {
            "name": "国际矿业D",
            "grade": "阴极铜 99.95%",
            "price": 70820,
            "freight": 420,
            "purity": 99,
            "reliability": 93,
            "lead_time": 5,
            "capacity": 1500,
            "region": "进口",
        },
    ]


def build_competitors() -> list[dict[str, Any]]:
    return [
        {"company": "竞品矿贸甲", "product": "阴极铜", "price": 71750, "channel": "阿里国际站", "trend": "上调 0.8%"},
        {"company": "竞品矿贸乙", "product": "粗铜", "price": 70620, "channel": "1688", "trend": "持平"},
        {"company": "竞品矿贸丙", "product": "铜精矿", "price": 68340, "channel": "官网", "trend": "下调 0.5%"},
    ]


def build_leads() -> list[dict[str, Any]]:
    return [
        {"company": "华南电缆厂", "contact": "王经理", "intent": "高", "product": "阴极铜", "volume": 900, "status": "待报价"},
        {"company": "江浙铜材加工厂", "contact": "陈总", "intent": "中高", "product": "粗铜", "volume": 600, "status": "跟进中"},
        {"company": "新能源连接器企业", "contact": "刘经理", "intent": "中", "product": "高纯铜", "volume": 300, "status": "待首次触达"},
    ]


def build_production() -> dict[str, Any]:
    labels = [f"班次{i}" for i in range(1, 9)]
    ore_tons = [520, 548, 560, 572, 590, 584, 603, 615]
    ore_grade = [1.18, 1.20, 1.19, 1.23, 1.25, 1.24, 1.27, 1.29]
    equipment = [94, 95, 96, 95, 97, 96, 97, 98]
    safety = [100, 100, 99, 100, 100, 98, 100, 100]
    return {
        "labels": labels,
        "ore_tons": ore_tons,
        "ore_grade": ore_grade,
        "equipment": equipment,
        "safety": safety,
        "summary": {
            "daily_output": 4592,
            "target_completion": 102.8,
            "avg_grade": round(sum(ore_grade) / len(ore_grade), 2),
            "equipment_uptime": round(sum(equipment) / len(equipment), 1),
            "safety_score": round(sum(safety) / len(safety), 1),
        },
        "alerts": [
            "虚拟样本：2 号采区钻机在第 6 班次温升偏高，建议夜班前完成润滑检查。",
            "虚拟样本：破碎段吞吐量高于周均值 4.1%，建议同步检查皮带余量。",
            "虚拟样本：精选段回收率稳定，当前可维持高负荷生产节奏。",
        ],
    }


def supplier_score(item: dict[str, Any]) -> float:
    landed_cost_score = 100 - ((item["price"] + item["freight"]) - 67000) / 50
    purity_score = item["purity"]
    reliability_score = item["reliability"]
    lead_time_score = max(0, 100 - item["lead_time"] * 8)
    capacity_score = min(100, item["capacity"] / 35)
    score = (
        landed_cost_score * 0.35
        + purity_score * 0.2
        + reliability_score * 0.25
        + lead_time_score * 0.1
        + capacity_score * 0.1
    )
    return round(score, 1)


def build_dashboard(role: str) -> dict[str, Any]:
    market = build_market_series()
    suppliers = build_suppliers()
    production = build_production()
    ranked = sorted(
        [{**s, "score": supplier_score(s), "landed_cost": s["price"] + s["freight"]} for s in suppliers],
        key=lambda x: x["score"],
        reverse=True,
    )
    competitors = build_competitors()
    leads = build_leads()

    common_metrics = [
        {"label": "LME 铜价", "value": f"${market['summary']['lme_latest']}/t", "delta": f"{market['summary']['lme_change_pct']}%"},
        {"label": "上期所主力", "value": f"¥{market['summary']['shfe_latest']}/t", "delta": "近两周上行"},
        {"label": "港口库存", "value": f"{market['summary']['inventory_latest']:,} t", "delta": f"{market['summary']['inventory_change_pct']}%"},
        {"label": "日采出矿量", "value": f"{production['summary']['daily_output']} t", "delta": f"达成率 {production['summary']['target_completion']}%"},
    ]

    role_cards = {
        "admin": [
            {"title": "待处理异常", "value": "3", "note": "采区设备 1 / 报价审批 2"},
            {"title": "跨部门任务", "value": "12", "note": "采购 4 / 销售 5 / 生产 3"},
        ],
        "buyer": [
            {"title": "首选矿源", "value": ranked[0]["name"], "note": f"综合分 {ranked[0]['score']}"},
            {"title": "最低到岸成本", "value": f"¥{min(x['landed_cost'] for x in ranked):,.0f}/t", "note": "当前可议价窗口"},
        ],
        "sales": [
            {"title": "今日重点线索", "value": leads[0]["company"], "note": f"需求 {leads[0]['volume']} t"},
            {"title": "建议挂牌价", "value": "¥71,980/t", "note": "较竞品均价高 0.6%"},
        ],
        "boss": [
            {"title": "预计毛利率", "value": "8.4%", "note": "受库存下降与现货升水支撑"},
            {"title": "经营风险等级", "value": "中", "note": "重点关注进口矿源扰动"},
        ],
    }

    return {
        "role_focus": ROLE_FOCUS[role],
        "common_metrics": common_metrics,
        "role_cards": role_cards[role],
        "market": market,
        "suppliers": ranked,
        "competitors": competitors,
        "leads": leads,
        "production": production,
        "breadcrumbs": {
            "dashboard": ["首页", ROLE_FOCUS[role]["title"]],
            "market": ["首页", "市场行情"],
            "procurement": ["首页", "采购管理"],
            "production": ["首页", "生产监测"],
            "sales": ["首页", "销售获客"],
            "agents": ["首页", "智能 Agent 中枢"],
        },
    }
