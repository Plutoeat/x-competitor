"""搜索工具与缓存单元测试"""

import json
import os
import time
from unittest.mock import patch

import pytest

from x_competitor.tools.search_tool import CachedSearchTool, create_search_tool


class TestCreateSearchTool:
    """测试 create_search_tool 工厂函数"""

    @patch.dict(os.environ, {"SERPER_API_KEY": "test-serper-key"}, clear=False)
    def test_returns_cached_tool_with_serper(self):
        from x_competitor.config.settings import Settings

        s = Settings(serper_api_key="test-serper-key")
        with patch("x_competitor.tools.search_tool.settings", s):
            tool = create_search_tool()
        assert isinstance(tool, CachedSearchTool)
        assert "Serper" in type(tool._inner).__name__

    @patch.dict(os.environ, {"TAVILY_API_KEY": "test-tavily-key"}, clear=False)
    def test_returns_cached_tool_with_tavily(self):
        from x_competitor.config.settings import Settings

        s = Settings(tavily_api_key="test-tavily-key")
        with patch("x_competitor.tools.search_tool.settings", s):
            tool = create_search_tool()
        assert isinstance(tool, CachedSearchTool)
        assert "Tavily" in type(tool._inner).__name__

    def test_serper_preferred_over_tavily(self):
        from x_competitor.config.settings import Settings

        s = Settings(serper_api_key="key1", tavily_api_key="key2")
        with patch("x_competitor.tools.search_tool.settings", s):
            tool = create_search_tool()
        assert "Serper" in type(tool._inner).__name__

    def test_raises_when_no_key_configured(self):
        from x_competitor.config.settings import Settings

        s = Settings(serper_api_key="", tavily_api_key="")
        with patch("x_competitor.tools.search_tool.settings", s):
            with pytest.raises(ValueError, match="未配置搜索引擎"):
                create_search_tool()


class TestCache:
    """测试搜索缓存"""

    def test_cache_hit(self, tmp_path):
        from x_competitor.tools import cache

        with patch.object(cache, "settings") as mock_settings:
            mock_settings.cache_dir = tmp_path
            mock_settings.cache_ttl_hours = 24

            cache.put("test_query", "test_result")
            assert cache.get("test_query") == "test_result"

    def test_cache_miss(self, tmp_path):
        from x_competitor.tools import cache

        with patch.object(cache, "settings") as mock_settings:
            mock_settings.cache_dir = tmp_path
            mock_settings.cache_ttl_hours = 24

            assert cache.get("nonexistent") is None

    def test_cache_expired(self, tmp_path):
        from x_competitor.tools import cache

        with patch.object(cache, "settings") as mock_settings:
            mock_settings.cache_dir = tmp_path
            mock_settings.cache_ttl_hours = 1

            cache.put("old_query", "old_result")

            # 手动修改时间戳为 2 小时前
            cache_files = list(tmp_path.glob("*.json"))
            data = json.loads(cache_files[0].read_text())
            data["ts"] = time.time() - 7200
            cache_files[0].write_text(json.dumps(data))

            assert cache.get("old_query") is None

    def test_purge_expired(self, tmp_path):
        from x_competitor.tools import cache

        with patch.object(cache, "settings") as mock_settings:
            mock_settings.cache_dir = tmp_path
            mock_settings.cache_ttl_hours = 1

            # 写入 2 个缓存：1 个过期，1 个有效
            cache.put("fresh", "fresh_result")
            cache.put("stale", "stale_result")

            # 将 stale 的时间戳改为 2 小时前
            for f in tmp_path.glob("*.json"):
                data = json.loads(f.read_text())
                if data["result"] == "stale_result":
                    data["ts"] = time.time() - 7200
                    f.write_text(json.dumps(data))

            removed = cache.purge_expired()
            assert removed == 1
            assert cache.get("fresh") == "fresh_result"
            assert cache.get("stale") is None