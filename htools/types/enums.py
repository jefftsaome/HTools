# hsys/htools/htools/types/enums.py
from enum import IntEnum, Enum


class TickSide(IntEnum):
    """行情方向标识。

    LONG = 看涨方向（预期价格上涨时买入持有）
    SHORT = 看跌方向（预期价格下跌时卖出）
    FLAT = 平盘（价格无显著方向变化）
    """
    LONG = 1
    SHORT = 2
    FLAT = 3


class TickType(IntEnum):
    """行情数据类型。

    TRADE = 已成交的实时交易数据
    SNAPSHOT = 市场快照（当前盘口/深度摘要）
    STATUS = 状态变更通知（连接状态、系统事件等）
    """
    TRADE = 1
    SNAPSHOT = 2
    STATUS = 3


class DecisionAction(str, Enum):
    """交易决策动作类型。

    ENTER = 开仓入场（按指定方向建立头寸）
    EXIT = 平仓离场（了结当前头寸）
    PASS = 观望跳过（当前不操作）
    """
    ENTER = "ENTER"
    EXIT = "EXIT"
    PASS = "PASS"


