# DataSource 接口实现规范

## 必须实现

- `id` — 返回唯一字符串标识
- `name` — 返回人类可读名称
- `status` — 返回 'idle'/'running'/'error'/'stopped'
- `start()` — 异步迭代器，产出 MarketTick
- `stop()` — 停止采集

## 约束

- `start()` 被调用后必须持续产出 MarketTick 直到 `stop()` 被调用
- 发生网络错误时应自动重连（3 次），超出后停止产出并设置 status='error'
- 不得抛出未捕获的异常

## 注册方式

在 pyproject.toml 中注册 entry_points:
```toml
[project.entry-points."data_sources"]
your_source = "yourpkg.sources.your:YourSource"
```
