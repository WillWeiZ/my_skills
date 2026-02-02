---
name: stock-a-quotes
description: 查询 A 股实时行情数据。使用新浪财经 API 获取沪深京 A 股的实时价格、涨跌幅、成交量、成交额等信息。适用于股票查询、行情监控、投资分析等场景。
---

# A 股实时行情查询

使用新浪财经 API 获取沪深京 A 股实时行情数据。

## 使用方式

```bash
# 查询上证指数
python skills/stock-a-quotes/scripts/stock_price.py -s 000001

# 查询深证成指
python skills/stock-a-quotes/scripts/stock_price.py --symbol 399001

# 查询具体股票
python skills/stock-a-quotes/scripts/stock_price.py -s 600519  # 贵州茅台
python skills/stock-a-quotes/scripts/stock_price.py -s 000001  # 平安银行
python skills/stock-a-quotes/scripts/stock_price.py -s 300750  # 宁德时代

# JSON 格式输出
python skills/stock-a-quotes/scripts/stock_price.py -s 600519 --json
```

## 输出字段

| 字段 | 说明 |
|------|------|
| code | 股票代码 |
| name | 股票名称 |
| price | 当前价格 |
| change_pct | 涨跌幅 (%) |
| change | 涨跌额 |
| open | 今开价 |
| high | 最高价 |
| low | 最低价 |
| volume | 成交量 (万手) |
| turnover | 成交额 (万元) |
| time | 时间 |

## 代码规则

- 上海市场: 代码以 5/6/9 开头 (如 sh600519)
- 深圳市场: 其他代码 (如 sz000001)
- 支持直接输入数字，自动补全市场前缀

## 数据来源

- **接口**: 新浪财经 (`hq.sinajs.cn`)
- **特点**: 延迟小、国内访问稳定
