"""搜索工具封装 — 根据配置自动选择 Serper 或 Tavily，支持结果缓存"""

from crewai.tools import BaseTool
from crewai_tools import SerperDevTool, TavilySearchTool

from x_competitor.config import settings
from x_competitor.tools import cache


class CachedSearchTool(BaseTool):
    """在底层搜索工具外包一层缓存。"""

    name: str = "web_search"
    description: str = "搜索互联网获取信息。输入搜索关键词，返回搜索结果。"
    _inner: BaseTool

    def __init__(self, inner: BaseTool, **kwargs):
        super().__init__(**kwargs)
        self._inner = inner

    def _run(self, query: str, **kwargs) -> str:
        cached = cache.get(query)
        if cached is not None:
            return cached
        result = self._inner.run(query, **kwargs)
        cache.put(query, result)
        return result


def create_search_tool() -> BaseTool:
    """根据 settings 中可用的 API key 创建搜索工具实例。

    优先使用 Serper，若未配置则回退到 Tavily。
    返回的工具自带缓存，相同查询不会重复调用 API。
    """
    if settings.serper_api_key:
        inner = SerperDevTool()
    elif settings.tavily_api_key:
        inner = TavilySearchTool()
    else:
        raise ValueError(
            "未配置搜索引擎 API key，请在 .env 中设置 SERPER_API_KEY 或 TAVILY_API_KEY"
        )
    return CachedSearchTool(inner=inner)