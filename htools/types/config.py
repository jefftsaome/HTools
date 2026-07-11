# htools/types/config.py
"""数据源通用配置模型。

SourceConfig 定义了数据源初始化所需的标准参数，
各数据源可通过 extra 字段携带自己的专属配置。
"""

from dataclasses import dataclass


@dataclass
class SourceConfig:
    """数据源通用配置 schema"""
    source_id: str
    enabled: bool = True
    poll_interval_ms: int = 50
    max_retries: int = 3
    retry_delay_ms: int = 1000
    extra: dict | None = None
