# hsys/htools/htools/interfaces/strategy.py
from abc import ABC, abstractmethod
from ..types import MarketTick, Decision


class Strategy(ABC):
    """交易策略抽象接口。

    实现此接口的类根据实时行情（MarketTick）做出交易决策（Decision）。

    用法（hsys 侧）：
        for tick in ticks:
            decision = strategy.on_tick(tick)
            if decision:
                execute(decision)

    实现规范（hstg 侧）：
        - on_tick 必须是纯函数（无 I/O、无副作用）
        - 单次调用必须在 10ms 内返回，避免阻塞行情处理
        - 策略不得修改传入的 MarketTick 对象
        - reset() 清除内部状态，用于新交易周期开始
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """策略唯一标识，如 'momentum'。"""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """策略显示名称，如 '趋势追踪策略'。"""
        ...

    @abstractmethod
    def on_tick(self, tick: MarketTick) -> Decision | None:
        """每笔行情回调。返回 None 表示不操作。"""
        ...

    @abstractmethod
    def reset(self) -> None:
        """重置策略状态（新周期时调用）"""
        ...
