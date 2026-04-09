"""3D打印行业竞品分析 Multi-Agent 系统入口"""

import argparse
from datetime import date

from crewai import Crew, Process
from dotenv import load_dotenv

from x_competitor.agents.analyst import create_analyst_agent
from x_competitor.agents.collector import create_collector_agent
from x_competitor.agents.writer import create_writer_agent
from x_competitor.config import settings
from x_competitor.tasks.analyze_task import create_analyze_task
from x_competitor.tasks.collect_task import create_collect_task
from x_competitor.tasks.write_task import create_write_task

load_dotenv()

DEFAULT_PRODUCTS = ["拓竹 A1"]


def run(product: str) -> str:
    """组装 Crew 并执行完整分析流水线，返回报告内容。"""
    print(f"\n{'='*60}")
    print(f"  开始分析竞品: {product}")
    print(f"{'='*60}\n")

    # Agents
    collector = create_collector_agent()
    analyst = create_analyst_agent()
    writer = create_writer_agent()

    # Tasks（顺序定义，上游输出自动传递给下游）
    collect_task = create_collect_task(collector, product)
    analyze_task = create_analyze_task(analyst, product)
    write_task = create_write_task(writer, product)

    # Crew — Sequential Process
    crew = Crew(
        agents=[collector, analyst, writer],
        tasks=[collect_task, analyze_task, write_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    # 保存报告到 output/
    output_dir = settings.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{product.replace(' ', '_')}_{date.today()}.md"
    output_path = output_dir / filename
    output_path.write_text(str(result), encoding="utf-8")
    print(f"\n报告已保存至: {output_path}")

    return str(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="3D打印行业竞品自动化分析系统",
    )
    parser.add_argument(
        "products",
        nargs="*",
        default=DEFAULT_PRODUCTS,
        help="要分析的竞品名称列表（默认: 拓竹 A1）",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="禁用搜索结果缓存",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.no_cache:
        settings.cache_ttl_hours = 0

    from x_competitor.tools.cache import purge_expired

    removed = purge_expired()
    if removed:
        print(f"已清理 {removed} 个过期缓存文件")

    print("x-competitor: 3D打印行业竞品自动化分析系统")
    print(f"待分析竞品: {', '.join(args.products)}")

    for product in args.products:
        run(product)

    print(f"\n全部 {len(args.products)} 个竞品分析完成。")


if __name__ == "__main__":
    main()