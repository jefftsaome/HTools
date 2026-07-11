# htools/utils/retry.py
"""异步重试工具 — 指数退避 + 最大重试次数。

供三个团队共用以实现断线重连、网络请求重试等场景。
"""

from __future__ import annotations

import asyncio
import functools
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def async_retry(
    coro_factory: Callable[[], Awaitable[T]],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> T:
    """带指数退避的异步重试。

    Args:
        coro_factory: 返回 coroutine 的可调用对象（每次重试重新创建）。
        max_retries: 最大重试次数，默认 3。
        base_delay: 初始延迟秒数，默认 1.0。
        max_delay: 最大延迟秒数，默认 60.0。
        backoff: 退避倍数，默认 2.0（即 1s → 2s → 4s ...）。
        exceptions: 可重试的异常类型元组，默认所有 Exception。

    Returns:
        协程的返回值。

    Raises:
        exceptions: 最后一次重试仍失败时抛出原始异常。
    """
    last_exc: Exception | None = None
    delay = base_delay

    for attempt in range(max_retries + 1):
        try:
            return await coro_factory()
        except exceptions as e:
            last_exc = e
            if attempt < max_retries:
                await asyncio.sleep(delay)
                delay = min(delay * backoff, max_delay)

    if last_exc is not None:
        raise last_exc


def retryable(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
):
    """装饰器：将异步函数包装为可重试版本。

    Usage:
        @retryable(max_retries=3)
        async def fetch_data(url: str) -> bytes:
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await async_retry(
                lambda: func(*args, **kwargs),
                max_retries=max_retries,
                base_delay=base_delay,
                max_delay=max_delay,
                backoff=backoff,
                exceptions=exceptions,
            )
        return wrapper
    return decorator
