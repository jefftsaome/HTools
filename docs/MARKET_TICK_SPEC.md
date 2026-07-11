# MarketTick 数据规范

## MarketTick 字段说明

| 字段 | 类型 | 说明 | 示例 |
|:----|:----|:----|:----|
| instrument_id | str | 合约ID（原牌桌ID） | "B54" |
| tick_type | TickType | 行情类型：1=成交, 2=快照, 3=状态 | 1 |
| side | TickSide | 方向：1=LONG, 2=SHORT, 3=FLAT | 1 |
| price | float | 价格（原点数） | 9.0 |
| volume | int | 成交量 | 1 |
| confidence | float | 置信度 0.0-1.0 | 0.97 |
| timestamp | int | 毫秒时间戳 | 1780997461578 |
| session_id | str | 交易时段ID（原靴号），用于策略周期reset | "sess_001" |
| metadata | dict | 扩展字段 | {"table_name":"经典百家乐"} |

## Decision 字段说明

| 字段 | 类型 | 默认值 | 说明 | 示例 |
|:----|:----|:----|:----|:----|
| action | DecisionAction | (必填) | ENTER=下注 / PASS=观望 / EXIT=换桌 | "ENTER" |
| side | TickSide | LONG | LONG/SHORT/FLAT，ENTER 时有效，PASS/EXIT 时忽略 | 1 |
| quantity | float | 0 | 仓位 | 1.0 |
| confidence | float | 0.0 | 置信度 | 0.8 |
| reason | str | "" | 决策理由 | "5连涨触发" |
