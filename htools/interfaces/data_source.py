# htools/interfaces/data_source.py
from abc import ABC, abstractmethod
from typing import AsyncIterator, Callable, Literal
from ..types import MarketTick, SourceStatusEvent


SourceStatus = Literal["idle", "running", "error", "stopped"]


class DataSource(ABC):
    """行情数据源抽象接口。

    实现此接口的类负责从特定渠道获取实时行情数据（MarketTick），
    并通过异步迭代器对外输出。

    用法（hsys 侧）：
        source = create_source()
        async for tick in source.start():
            process(tick)

    实现规范（hdt 侧）：
        - start() 被调用后必须持续产出 MarketTick 直到 stop() 被调用
        - 网络异常时应自动重连（内部实现），不得抛出未捕获异常
        - 状态变更通过 set_on_status_change 注册的回调通知
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """返回数据源唯一标识，如 'market_feed_1'。"""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """返回人类可读的数据源名称，如 '行情源 A'。"""
        ...

    @property
    @abstractmethod
    def status(self) -> SourceStatus:
        """当前状态：'idle' / 'running' / 'error' / 'stopped'"""
        ...

    @abstractmethod
    async def start(self) -> AsyncIterator[MarketTick]:
        """启动采集，返回 MarketTick 异步迭代器"""
        ...

    @abstractmethod
    async def stop(self):
        """停止采集"""
        ...

    def set_on_status_change(self, callback: Callable[[SourceStatusEvent], None]):
        """注册状态变更回调（可选）"""
        pass
