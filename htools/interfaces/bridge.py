# htools/interfaces/bridge.py
from abc import ABC, abstractmethod
from typing import AsyncIterator
from ..types import MarketTick


class Bridge(ABC):
    """数据桥接抽象接口 — 连接行情生产方与消费方。

    支持多种介质实现：
        - InProcessBridge: 同一进程内的 asyncio.Queue，延迟最低，适合开发/单机
        - RedisStreamBridge: 跨进程共享数据，适合生产环境多进程架构
        - FileBridge: JSONL 文件持久化，适合离线分析和回放
    """

    @abstractmethod
    async def publish(self, tick: MarketTick):
        """发布一条行情"""
        ...

    @abstractmethod
    async def subscribe(self) -> AsyncIterator[MarketTick]:
        """订阅行情流"""
        ...

    async def health_check(self) -> bool:
        """健康检查（可选实现），默认返回 True"""
        return True
