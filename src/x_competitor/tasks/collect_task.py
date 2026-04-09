"""情报收集任务"""

from datetime import date

from crewai import Agent, Task


def create_collect_task(agent: Agent, product: str) -> Task:
    today = date.today().isoformat()
    return Task(
        description=(
            f"当前日期：{today}\n\n"
            f"针对竞品「{product}」，使用搜索工具从互联网收集近 6 个月内的"
            f"用户真实测评与负面反馈。\n\n"
            f"**你必须进行至少 5 轮搜索，每轮使用不同的关键词组合：**\n"
            f"第1轮（中文负面）：{product} 缺点 问题\n"
            f"第2轮（中文测评）：{product} 测评 真实体验\n"
            f"第3轮（英文负面）：{product} problems issues complaints\n"
            f"第4轮（英文测评）：{product} review honest opinion\n"
            f"第5轮（论坛定向）：{product} site:reddit.com OR site:youtube.com\n\n"
            f"你也可以根据已收集到的信息追加更多搜索轮次以获取更全面的数据。\n\n"
            f"**数据质量要求：**\n"
            f"- 只收录包含具体使用细节的一手用户反馈\n"
            f"- 丢弃纯转载、营销软文、官方公告\n"
            f"- 每条结果需包含：标题、来源平台、原文链接、发布日期、关键内容摘要（至少50字）\n"
            f"- snippet 中必须保留用户的原始表述，不可改写"
        ),
        expected_output=(
            f"一份结构化的搜索结果列表，包含至少 20 条来自不同平台的用户反馈，"
            f"覆盖中英文内容。每条包含 title、source、url、date、snippet 字段。"
            f"snippet 应保留用户原话。"
        ),
        agent=agent,
    )