# htools/utils/time.py
"""时间工具 — 时间戳生成与格式化。

供三个团队共用。
"""

from __future__ import annotations

import datetime
import time


def now_ms() -> int:
    """返回当前毫秒时间戳。

    Returns:
        当前时间的毫秒时间戳（int），如 1780997461578。
    """
    return int(time.time() * 1000)


def format_ts(timestamp_ms: int, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """将毫秒时间戳格式化为字符串。

    Args:
        timestamp_ms: 毫秒时间戳。
        fmt: 时间格式字符串，默认 "%Y-%m-%d %H:%M:%S"。

    Returns:
        格式化后的时间字符串。
    """
    return datetime.datetime.fromtimestamp(
        timestamp_ms / 1000, tz=datetime.timezone.utc
    ).strftime(fmt)


def format_ts_local(timestamp_ms: int, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """将毫秒时间戳格式化为本地时间字符串。

    Args:
        timestamp_ms: 毫秒时间戳。
        fmt: 时间格式字符串。

    Returns:
        格式化后的本地时间字符串。
    """
    return datetime.datetime.fromtimestamp(timestamp_ms / 1000).strftime(fmt)


def ms_since(timestamp_ms: int) -> int:
    """计算指定时间戳距今的毫秒数。

    Args:
        timestamp_ms: 过去的毫秒时间戳。

    Returns:
        距今的毫秒数。
    """
    return now_ms() - timestamp_ms
