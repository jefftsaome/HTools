"""测试替身 — 供三仓库独立测试使用。

用法：
    # 在 hsys 测试中使用 FakeSource
    source = FakeSource([MarketTick(...)])
    controller.register_source(source)

    # 在 hstg 测试中使用 FakeStrategy
    strategy = FakeStrategy(Decision(ENTER, LONG, ...))

    # 在集成测试中使用 FakeBridge
    bridge = FakeBridge()
    await bridge.publish(tick)
    async for t in bridge.subscribe():
        ...
"""

import asyncio
from ..interfaces import DataSource, Strategy, Bridge
from ..types import MarketTick, Decision, TickSide, DecisionAction

class FakeSource(DataSource):
    """按预设序列吐 MarketTick 的假数据源"""

    def __init__(self, ticks: list[MarketTick] | None = None):
        self._ticks = ticks or []
        self._id = "fake_source"
        self._name = "Fake Source"
        self._status = "idle"

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> str:
        return self._status

    async def start(self):
        for tick in self._ticks:
            yield tick

    async def stop(self):
        pass


class FakeStrategy(Strategy):
    """固定返回指定决策的假策略"""

    def __init__(self, decision: Decision | None = None):
        self._decision = decision or Decision(
            action=DecisionAction.PASS,
            reason="fake",
        )

    @property
    def id(self) -> str:
        return "fake_strategy"

    @property
    def name(self) -> str:
        return "Fake Strategy"

    def on_tick(self, tick: MarketTick) -> Decision | None:
        return self._decision

    def reset(self):
        pass


class FakeBridge(Bridge):
    """基于 asyncio.Queue 的假桥接 — 用于集成测试。"""

    def __init__(self):
        self._queue: asyncio.Queue[MarketTick] = asyncio.Queue()

    async def publish(self, tick: MarketTick):
        await self._queue.put(tick)

    async def subscribe(self):
        while True:
            yield await self._queue.get()

    async def health_check(self) -> bool:
        return True
