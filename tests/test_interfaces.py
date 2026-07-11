"""htools 接口测试"""

import pytest
from htools.interfaces import DataSource, Strategy, Bridge
from htools.testing import FakeSource, FakeStrategy
from htools.types import MarketTick, TickSide, TickType, DecisionAction

@pytest.mark.asyncio
async def test_fake_source_implements_data_source():
    source = FakeSource()
    assert isinstance(source, DataSource)
    assert source.id == "fake_source"
    assert source.status == "idle"

@pytest.mark.asyncio
async def test_fake_source_yields_ticks():
    tick = MarketTick(
        instrument_id="test", tick_type=TickType.TRADE,
        side=TickSide.LONG, price=9.0, volume=1,
        confidence=0.95, timestamp=1000,
    )
    source = FakeSource([tick])
    result = []
    async for t in source.start():
        result.append(t)
        break
    assert result[0] == tick

@pytest.mark.asyncio
async def test_fake_strategy_implements_strategy():
    strategy = FakeStrategy()
    assert isinstance(strategy, Strategy)
    assert strategy.id == "fake_strategy"

@pytest.mark.asyncio
async def test_fake_strategy_returns_decision():
    strategy = FakeStrategy()
    tick = MarketTick(
        instrument_id="test", tick_type=TickType.TRADE,
        side=TickSide.LONG, price=9.0, volume=1,
        confidence=0.95, timestamp=1000,
    )
    result = strategy.on_tick(tick)
    assert result is not None
    assert result.action == DecisionAction.PASS

@pytest.mark.asyncio
async def test_bridge_health_check_default():
    class DummyBridge(Bridge):
        async def publish(self, tick): pass
        async def subscribe(self):
            yield
            return
    bridge = DummyBridge()
    healthy = await bridge.health_check()
    assert healthy is True
