# htools/utils/validate.py
"""数据校验工具 — MarketTick / Decision 字段合法性检查。

供三个团队共用。

用法：
    tick = MarketTick(...)
    errors = validate_market_tick(tick)
    if errors:
        log.error(f"行情数据校验失败: {errors}")

    if is_valid_decision(decision):
        execute(decision)
"""

from __future__ import annotations

from ..types import MarketTick, Decision, TickSide, DecisionAction


def validate_market_tick(tick: MarketTick) -> list[str]:
    """校验 MarketTick 字段合法性。

    Args:
        tick: 待校验的 MarketTick 实例。

    Returns:
        错误信息列表，空列表表示全部合法。
    """
    errors: list[str] = []

    if not isinstance(tick.side, TickSide):
        errors.append(f"side 必须是 TickSide 枚举，实际为 {type(tick.side).__name__}")

    if tick.confidence < 0.0 or tick.confidence > 1.0:
        errors.append(f"confidence 必须在 0.0~1.0 之间，实际为 {tick.confidence}")

    if not isinstance(tick.timestamp, int) or tick.timestamp <= 0:
        errors.append(f"timestamp 必须是正整数毫秒时间戳，实际为 {tick.timestamp}")

    return errors


def validate_decision(decision: Decision) -> list[str]:
    """校验 Decision 字段合法性。

    Args:
        decision: 待校验的 Decision 实例。

    Returns:
        错误信息列表，空列表表示全部合法。
    """
    errors: list[str] = []

    if not isinstance(decision.action, DecisionAction):
        errors.append(f"action 必须是 DecisionAction 枚举，实际为 {type(decision.action).__name__}")

    if not isinstance(decision.side, TickSide):
        errors.append(f"side 必须是 TickSide 枚举，实际为 {type(decision.side).__name__}")

    if not isinstance(decision.quantity, (int, float)) or decision.quantity < 0:
        errors.append(f"quantity 必须是非负数字，实际为 {decision.quantity}")

    if decision.confidence < 0.0 or decision.confidence > 1.0:
        errors.append(f"confidence 必须在 0.0~1.0 之间，实际为 {decision.confidence}")

    if not decision.reason:
        errors.append("reason 不能为空")

    return errors


def is_valid_market_tick(tick: MarketTick) -> bool:
    """快捷检查 MarketTick 是否合法。

    Returns:
        True 表示全部字段合法。
    """
    return len(validate_market_tick(tick)) == 0


def is_valid_decision(decision: Decision) -> bool:
    """快捷检查 Decision 是否合法。

    Returns:
        True 表示全部字段合法。
    """
    return len(validate_decision(decision)) == 0
