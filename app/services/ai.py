from __future__ import annotations

import html
import os
import re
from textwrap import dedent
from typing import Any

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


AGENT_CONFIG = {
    "market": {
        "name": "市场策略 Agent",
        "focus": "聚焦铜价/矿价、库存、汇率与交易节奏，输出行情判断与短期策略。",
        "system": "你是矿产贸易企业的市场策略分析师。你的输出必须专业、简洁、结构化，避免 markdown 符号、星号、井号、&&。用中文输出，强调结论、依据、风险、行动建议。",
    },
    "procurement": {
        "name": "采购优化 Agent",
        "focus": "聚焦矿源选择、到岸成本、交期风险、替代供应商与议价建议。",
        "system": "你是矿产贸易企业的采购优化专家。请基于成本、纯度、可靠性、交期与库存保障输出采购建议。不要使用 markdown 语法符号。",
    },
    "production": {
        "name": "生产监测 Agent",
        "focus": "聚焦开采作业进度、设备利用率、矿石品位、安全与产量偏差。",
        "system": "你是矿山生产与调度顾问。请从采出矿量、矿石品位、设备状态与安全风险给出清晰判断与班次建议。禁止输出 markdown 符号。",
    },
    "sales": {
        "name": "销售增长 Agent",
        "focus": "聚焦竞品价格、目标客户、建议报价、销售文案与线索优先级。",
        "system": "你是矿产贸易企业的销售增长顾问。输出要突出客户分层、报价策略、销售动作与跟进节奏，不要使用 markdown 符号。",
    },
    "boss": {
        "name": "经营驾驶舱 Agent",
        "focus": "聚焦利润、现金流、库存、产销协同与管理层决策。",
        "system": "你是矿产贸易企业老板的经营参谋。请给出高层可直接决策的经营摘要，避免技术行话堆砌，不使用 markdown 符号。",
    },
}


def _format_prompt(agent_key: str, context: dict[str, Any], user_message: str) -> str:
    return dedent(
        f"""
        当前 Agent：{AGENT_CONFIG[agent_key]['name']}
        专业重点：{AGENT_CONFIG[agent_key]['focus']}

        企业上下文（虚拟演示数据）：
        1. 市场摘要：LME 最新价 {context['market']['summary']['lme_latest']}，上期所主力 {context['market']['summary']['shfe_latest']}，库存 {context['market']['summary']['inventory_latest']}。
        2. 生产摘要：日采出矿量 {context['production']['summary']['daily_output']} 吨，品位均值 {context['production']['summary']['avg_grade']}，设备开机率 {context['production']['summary']['equipment_uptime']}%。
        3. 采购摘要：最佳供应商 {context['suppliers'][0]['name']}，综合分 {context['suppliers'][0]['score']}，到岸成本 {context['suppliers'][0]['landed_cost']}。
        4. 销售摘要：重点线索 {context['leads'][0]['company']}，竞品参考价 {context['competitors'][0]['price']}。

        用户问题：{user_message}

        请按以下结构输出：
        标题：一句话结论
        关键判断：3 点以内
        主要依据：3 点以内
        行动建议：3 点以内
        风险提醒：2 点以内
        """
    ).strip()


class AIService:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key and OpenAI else None

    def run_agent(self, agent_key: str, context: dict[str, Any], user_message: str) -> dict[str, str]:
        prompt = _format_prompt(agent_key, context, user_message)
        if self.client:
            try:
                response = self.client.responses.create(
                    model=self.model,
                    input=[
                        {"role": "system", "content": AGENT_CONFIG[agent_key]["system"]},
                        {"role": "user", "content": prompt},
                    ],
                )
                text = getattr(response, "output_text", "") or self._fallback(agent_key, context, user_message)
            except Exception:
                text = self._fallback(agent_key, context, user_message)
        else:
            text = self._fallback(agent_key, context, user_message)
        return {
            "agent_name": AGENT_CONFIG[agent_key]["name"],
            "focus": AGENT_CONFIG[agent_key]["focus"],
            "raw_text": text,
            "html": self.to_html(text),
        }

    def _fallback(self, agent_key: str, context: dict[str, Any], user_message: str) -> str:
        market = context["market"]["summary"]
        production = context["production"]["summary"]
        top_supplier = context["suppliers"][0]
        top_lead = context["leads"][0]
        competitor = context["competitors"][0]

        templates = {
            "market": f"标题：短期市场偏强，但不宜追高采购\n关键判断：库存持续下降；内外盘价格同步抬升；现货补库意愿恢复。\n主要依据：LME 铜价最新 {market['lme_latest']} 美元/吨；上期所主力 {market['shfe_latest']} 元/吨；港口库存回落至 {market['inventory_latest']} 吨。\n行动建议：分批锁定 30% 至 40% 近月需求；高位报价时同步关注基差；对进口矿源保持替代预案。\n风险提醒：海外供应扰动可能放大波动；若终端需求回落，现货升水可能快速走弱。",
            "procurement": f"标题：当前优先推进 {top_supplier['name']} 的谈判\n关键判断：其综合分最高；到岸成本与可靠性平衡最好；交期可满足近期生产。\n主要依据：综合分 {top_supplier['score']}；到岸成本 {top_supplier['landed_cost']} 元/吨；交期 {top_supplier['lead_time']} 天。\n行动建议：先锁定主供应商 50% 需求；用第二供应商做议价锚点；对低价但长交期矿源只做补充。\n风险提醒：运输扰动会抬高到岸成本；低品位矿源会增加后续加工压力。",
            "production": f"标题：生产运行总体稳定，可维持偏高负荷\n关键判断：日产量达标；矿石品位稳中有升；设备开机率处于良好区间。\n主要依据：日采出矿量 {production['daily_output']} 吨；平均品位 {production['avg_grade']}；设备开机率 {production['equipment_uptime']}%。\n行动建议：重点检查 2 号采区钻机温升；给破碎段预留维护窗口；保持夜班安全巡检频率。\n风险提醒：单点设备异常可能拖累班次产量；连续高负荷下需防止皮带与润滑系统疲劳。",
            "sales": f"标题：建议围绕高意向客户稳价成交\n关键判断：重点线索质量较高；竞品价格仍有上探；当前有利润保护空间。\n主要依据：重点客户 {top_lead['company']} 需求 {top_lead['volume']} 吨；竞品参考价 {competitor['price']} 元/吨；现货端支撑偏强。\n行动建议：优先向高意向客户给出阶梯报价；文案强调稳定供货与品位保障；对中意向客户设置时效性优惠。\n风险提醒：若竞品突然降价，需快速重估报价；成交过度依赖单一客户会放大回款风险。",
            "boss": f"标题：当前经营节奏适合稳采购、快转化、控风险\n关键判断：市场偏强支撑毛利；生产端稳定可保障交付；销售端重点客户具备转单潜力。\n主要依据：LME 铜价 {market['lme_latest']}；日采出矿量 {production['daily_output']} 吨；高意向客户为 {top_lead['company']}。\n行动建议：维持分批采购策略；推动高意向客户在一周内完成报价闭环；建立进口矿源备选机制。\n风险提醒：价格波动与运输扰动是主要不确定性；高位库存不宜过快累积。",
        }
        return templates[agent_key]

    @staticmethod
    def clean_text(text: str) -> str:
        text = text.replace("&&", " ")
        text = re.sub(r"[*#`>\-]{2,}", " ", text)
        text = re.sub(r"\*", "", text)
        text = re.sub(r"\s+", " ", text)
        text = text.replace("标题：", "\n标题：")
        text = text.replace("关键判断：", "\n关键判断：")
        text = text.replace("主要依据：", "\n主要依据：")
        text = text.replace("行动建议：", "\n行动建议：")
        text = text.replace("风险提醒：", "\n风险提醒：")
        return text.strip()

    @classmethod
    def to_html(cls, text: str) -> str:
        text = cls.clean_text(text)
        sections = []
        current_title = None
        current_items: list[str] = []
        for chunk in [line.strip() for line in text.split("\n") if line.strip()]:
            if "：" in chunk:
                label, content = chunk.split("：", 1)
                if label in {"标题", "关键判断", "主要依据", "行动建议", "风险提醒"}:
                    if current_title is not None:
                        sections.append((current_title, current_items))
                    current_title = label
                    current_items = [item.strip() for item in re.split(r"；|。", content) if item.strip()]
                    continue
            current_items.append(chunk)
        if current_title is not None:
            sections.append((current_title, current_items))

        html_parts = []
        for title, items in sections:
            safe_items = "".join(f"<li>{html.escape(i)}</li>" for i in items)
            if title == "标题":
                html_parts.append(f"<section class='agent-section hero'><h3>{html.escape(items[0]) if items else '分析结果'}</h3></section>")
            else:
                html_parts.append(f"<section class='agent-section'><h4>{html.escape(title)}</h4><ul>{safe_items}</ul></section>")
        return "".join(html_parts) or f"<p>{html.escape(text)}</p>"
