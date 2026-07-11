# hsys/htools/htools/types/market_tick.py
"""行情数据与交易决策的数据模型。

MarketTick 是整个系统的核心数据单元，从数据采集到策略决策的完整链路都基于它传递。
Decision 是策略引擎的输出，表示对当前行情的交易建议。
"""

from dataclasses import dataclass, field
from .enums import TickSide, DecisionAction


@dataclass
class MarketTick:
    """单笔行情数据。

    代表一次交易或状态更新的最小单元。

    Fields:
        side: 方向标识（LONG=看涨方向/SHORT=看跌方向/FLAT=平盘）
        counter_id: 柜台编号
        trade_seq: 交易序号
        side_sequence: 方向历史序列（L/S/F），GUI 绘趋势图用
        confidence: 数据置信度 0.0~1.0
        timestamp: 事件发生的毫秒时间戳（Unix 毫秒）
        long_score: 多头方向评分
        short_score: 空头方向评分
        session_id: 交易时段标识，用于策略在新时段开始时重置
        status: 当前状态文本
        countdown: 倒计时秒数
        total_amt: 全场成交总量
        total_cnt: 全场成交笔数
        long_amt: 多头方向成交量
        long_cnt: 多头方向成交笔数
        short_amt: 空头方向成交量
        short_cnt: 空头方向成交笔数
        flat_amt: 平盘方向成交量
        flat_cnt: 平盘方向成交笔数
        metadata: 扩展字段，用于携带附加信息
    """
    side: TickSide
    counter_id: str = ""
    trade_seq: str = ""
    side_sequence: list[str] = field(default_factory=list)
    confidence: float = 1.0
    timestamp: int = 0
    long_score: int = 0
    short_score: int = 0
    session_id: str = ""
    status: str = ""
    countdown: int | None = None
    total_amt: int = 0
    total_cnt: int = 0
    long_amt: int = 0
    long_cnt: int = 0
    short_amt: int = 0
    short_cnt: int = 0
    flat_amt: int = 0
    flat_cnt: int = 0
    metadata: dict = field(default_factory=dict)


@dataclass
class Decision:
    """交易策略的决策输出。

    ENTER = 开仓：按 side 方向入场，quantity 指定仓位大小
    PASS = 观望：当前不操作，等待后续行情
    EXIT = 平仓离场：退出当前交易品种/合约

    Fields:
        action: 决策动作类型
        side: 开仓方向（ENTER 时有效）
        quantity: 建议数量/手数
        confidence: 决策置信度 0.0~1.0
        reason: 决策理由说明
    """
    action: DecisionAction
    side: TickSide = TickSide.LONG
    quantity: float = 0
    confidence: float = 0.0
    reason: str = ""
