# htools/types/events.py
"""数据源状态事件类型定义。

SourceStatusEvent 用于在数据源状态发生变化时通知系统框架。
状态值说明：
    connected     - 数据源已成功连接并开始采集
    disconnected  - 数据源连接已断开
    error         - 数据源发生不可恢复的错误
    reconnecting  - 数据源正在自动重连中
"""

from dataclasses import dataclass


@dataclass
class SourceStatusEvent:
    """数据源状态变更事件"""
    source_id: str
    status: str
    message: str = ""
    timestamp: int = 0
