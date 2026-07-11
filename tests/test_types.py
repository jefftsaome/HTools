"""htools 类型测试"""

from htools.types import (
    MarketTick, Decision, TickSide, TickType, DecisionAction,
    SourceStatusEvent, SourceConfig,
)

def test_market_tick_defaults():
    tick = MarketTick(
        instrument_id="B54",
        tick_type=TickType.TRADE,
        side=TickSide.LONG,
        price=9.0,
        volume=1,
        confidence=0.95,
        timestamp=1000,
    )
    assert tick.instrument_id == "B54"
    assert tick.tick_type == TickType.TRADE
    assert tick.side == TickSide.LONG
    assert tick.metadata == {}  # default empty dict
    assert tick.session_id == ""  # default empty str

def test_decision_defaults():
    d = Decision(
        action=DecisionAction.ENTER,
        side=TickSide.LONG,
        quantity=1.0,
        confidence=0.8,
        reason="test",
    )
    assert d.action == DecisionAction.ENTER

def test_source_status_event():
    e = SourceStatusEvent(source_id="leyu", status="connected")
    assert e.source_id == "leyu"
    assert e.status == "connected"

def test_source_config():
    c = SourceConfig(source_id="leyu")
    assert c.source_id == "leyu"
    assert c.enabled is True
    assert c.poll_interval_ms == 50

def test_tick_side_values():
    assert TickSide.LONG == 1
    assert TickSide.SHORT == 2
    assert TickSide.FLAT == 3

def test_tick_type_values():
    assert TickType.TRADE == 1
    assert TickType.SNAPSHOT == 2
    assert TickType.STATUS == 3

def test_decision_action_values():
    assert DecisionAction.ENTER == "ENTER"
    assert DecisionAction.EXIT == "EXIT"
    assert DecisionAction.PASS == "PASS"
