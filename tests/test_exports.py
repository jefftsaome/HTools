"""验证 htools 所有导出可正常 import"""

from htools import interfaces, types, testing

def test_imports():
    assert interfaces.DataSource is not None
    assert interfaces.Strategy is not None
    assert interfaces.Bridge is not None
    
    assert types.MarketTick is not None
    assert types.Decision is not None
    assert types.TickSide is not None
    assert types.TickType is not None
    assert types.DecisionAction is not None
    assert types.SourceStatusEvent is not None
    
    assert testing.FakeSource is not None
    assert testing.FakeStrategy is not None
