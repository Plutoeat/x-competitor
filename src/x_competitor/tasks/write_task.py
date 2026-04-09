"""报告撰写任务"""

from datetime import date

from crewai import Agent, Task


def create_write_task(agent: Agent, product: str) -> Task:
    today = date.today().isoformat()
    return Task(
        description=(
            f"报告日期：{today}\n\n"
            f"基于上游数据分析师提供的「{product}」痛点分析结果，撰写一份结构化的"
            f"Markdown 格式竞品劣势分析简报。\n\n"
            f"**报告结构要求：**\n"
            f"1. **概述**：竞品基本信息、本次分析的数据来源和覆盖范围、报告日期\n"
            f"2. **核心痛点排名**：按频次和严重程度综合排序的痛点表格\n"
            f"3. **详细分析**：每个痛点的深入描述、数据支撑、用户原文引用\n"
            f"4. **总结与建议**：基于竞品劣势可利用的竞争机会和产品改进方向\n\n"
            f"**严格约束：**\n"
            f"- 只使用上游分析师提供的数据和引用，绝不自行编造\n"
            f"- 如果某个痛点没有用户原文引用，直接从报告中删除该痛点\n"
            f"- 所有数据（频次、占比、数量）必须与上游分析结果完全一致\n"
            f"- 不得出现'需补充'、'待验证'等占位性内容\n\n"
            f"报告风格：专业、客观、数据驱动，适合产品和运营团队阅读"
        ),
        expected_output=(
            f"一份完整的 Markdown 格式「{product}」竞品劣势分析简报，"
            f"包含概述、核心痛点排名、详细分析、总结与建议四个章节。"
            f"每个痛点都有真实用户原文支撑，不含任何无证据的推测内容。"
        ),
        agent=agent,
    )