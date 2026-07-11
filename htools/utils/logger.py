# htools/utils/logger.py
"""基础日志配置 — loguru 控制台输出 + 普通文件输出。

供三个团队共用。加密日志 sink（每行独立 AES-GCM）是 hsys 专属功能，
留在 hsys 层实现。
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from loguru._logger import Logger

_LOGGING_CONFIGURED = False


def setup_logging(
    level: str = "DEBUG",
    console: bool = True,
    file_path: Path | None = None,
) -> None:
    """配置 loguru 日志格式。

    Args:
        level: 日志级别，默认 "DEBUG"。
        console: True 输出到 stderr。
        file_path: 日志文件路径，None 则不写文件。
    """
    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return

    logger.remove()
    logger.configure(extra={"event": "system"})

    if console and sys.stderr is not None:
        logger.add(
            sys.stderr,
            level=level,
            colorize=True,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <7}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            ),
        )

    if file_path is not None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(file_path),
            level=level,
            rotation="50 MB",
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <7} | {name}:{line} | {message}",
        )

    _LOGGING_CONFIGURED = True


def get_logger(name: str) -> Logger:
    """获取指定名称的日志器实例。

    Args:
        name: 日志器名称，通常传 __name__。

    Returns:
        loguru logger 实例。
    """
    return logger.bind(event=name)
