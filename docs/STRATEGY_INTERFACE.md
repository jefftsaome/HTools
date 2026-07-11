# Strategy 接口实现规范

## 必须实现

- `id` — 返回唯一字符串标识
- `name` — 返回人类可读名称
- `on_tick(tick)` — 每笔行情回调，返回 Decision 或 None
- `reset()` — 重置策略状态

## 约束

- `on_tick` 必须是纯函数（无副作用、无 I/O）
- 单次调用必须在 10ms 内返回
- 策略只读 MarketTick，不得修改

## 注册方式

在 pyproject.toml 中注册 entry_points:
```toml
[project.entry-points."strategies"]
your_strategy = "yourpkg.strategies.your:YourStrategy"
```
