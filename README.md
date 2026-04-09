# x-competitor

3D打印行业竞品自动化分析 Multi-Agent 系统。通过编排三个智能体，实现从数据抓取、痛点提炼到报告生成的端到端自动化。

## 架构

```
情报收集员 ──▶ 数据分析师 ──▶ 报告撰稿人 ──▶ Markdown 报告
  (搜索)        (分析)         (撰写)
```

| Agent | 职责 |
|-------|------|
| 情报收集员 | 多轮中英文搜索，从 Reddit、YouTube、知乎、B站等平台收集用户真实反馈 |
| 数据分析师 | 清洗数据，提取有充分证据支撑的痛点并量化 |
| 报告撰稿人 | 输出结构化 Markdown 竞品劣势分析简报 |

## 快速开始

### 环境要求

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

### 安装

```bash
git clone <repo-url>
cd x-competitor
uv sync
```

### 配置

复制环境变量模板并填入 API key：

```bash
cp .env.example .env
```

需要配置：
- `OPENAI_API_KEY` — LLM API 密钥
- `SERPER_API_KEY` 或 `TAVILY_API_KEY` — 搜索引擎 API 密钥（二选一）

### 运行

```bash
# 分析单个竞品（默认：拓竹 A1）
uv run python -m x_competitor.main

# 指定竞品
uv run python -m x_competitor.main "Creality K1"

# 批量分析多个竞品
uv run python -m x_competitor.main "拓竹 A1" "Creality K1" "AnkerMake M5"

# 禁用搜索缓存
uv run python -m x_competitor.main --no-cache "拓竹 A1"
```

报告输出至 `output/{产品名}_{日期}.md`。

## 项目结构

```
src/x_competitor/
├── main.py          # 入口：CLI 参数、Crew 组装、流水线启动
├── agents/          # Agent 定义（collector, analyst, writer）
├── tasks/           # Task 定义（与 Agent 一一对应）
├── tools/           # 搜索工具封装 + 文件缓存
└── config/          # pydantic-settings 配置管理
```

## 测试

```bash
uv run pytest
```

## License

[MIT](LICENSE)