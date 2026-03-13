# 矿产贸易企业智能经营平台 v2

这是一个可直接运行和部署的矿产贸易企业 Agent 演示系统，适合向客户展示市场行情、采购管理、生产监测、销售获客与多 Agent 智能分析。

## 本次已修复与增强
- 首页文案已改为“矿产贸易企业”
- 新增“生产监测管理模块”
- 使用更贴近真实业务的虚拟历史数据展示图表
- admin / buyer / sales / boss 登录后均有更明确的角色侧重点
- 修复页面无限延伸、下拉体验不佳的问题
- 增加清晰的界面层级、面包屑和流程指引
- 优化 Agent 输出排版，避免出现 **、&& 等符号
- 每个 Agent 都有更清晰的专业定位

## 本地运行
```bash
python -m venv .venv
source .venv/bin/activate   # Windows 用 .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

打开：`http://127.0.0.1:8000`

## 测试账号
- admin / admin123
- buyer / buyer123
- sales / sales123
- boss / boss123

## OpenAI 配置
可选环境变量：
- `OPENAI_API_KEY`
- `OPENAI_MODEL`，默认 `gpt-4o-mini`
- `SECRET_KEY`

如果没有配置 `OPENAI_API_KEY`，系统会自动使用内置 fallback AI 输出，仍可演示。

## Render 部署
仓库根目录已包含：
- `Dockerfile`
- `render.yaml`
- `.env.example`

Render 中选择 **New Web Service** 或 **Blueprint** 都可以。
