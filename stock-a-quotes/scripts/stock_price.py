#!/usr/bin/env python3
"""
A 股实时行情查询脚本
使用新浪财经 API 获取沪深京 A 股实时价格数据
"""

import json
import sys
import argparse
import re


def get_stock_price_sina(symbol):
    """获取单只股票价格 (新浪财经)"""
    try:
        import requests
        
        # 新浪财经 API
        url = f"http://hq.sinajs.cn/list={symbol}"
        
        headers = {
            "Referer": "http://finance.sina.com.cn/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        session = requests.Session()
        session.trust_env = False  # 禁用环境变量代理
        
        response = session.get(url, headers=headers, timeout=15)
        response.encoding = 'gbk'
        
        # 解析返回数据
        # 格式: var hq_str_sh600000="平安银行,12.340,12.350,12.320,12.350,12.310,12.320,12.330,12345678,12345678,2026-02-02,10:25:00,00";
        text = response.text
        
        # 匹配数据
        match = re.search(r'hq_str_(\w+)="(.+)"', text)
        if not match:
            return {"error": f"未找到股票 {symbol} 的数据"}
        
        code = match.group(1)
        data = match.group(2).split(',')
        
        if len(data) < 32:
            return {"error": f"数据格式错误 for {symbol}"}
        
        # 计算涨跌幅
        close_yesterday = float(data[2])
        price_current = float(data[3])
        change = price_current - close_yesterday
        change_pct = (change / close_yesterday) * 100 if close_yesterday else 0
        
        return {
            "code": code,
            "name": data[0].strip(),
            "open": float(data[1]),
            "close_yesterday": close_yesterday,
            "price": price_current,
            "high": float(data[4]),
            "low": float(data[5]),
            "volume": int(float(data[8]) / 100),  # 成交量(手)
            "turnover": float(data[9]) / 10000,   # 成交额(万元)
            "change": round(change, 3),
            "change_pct": round(change_pct, 2),
            "date": data[30],
            "time": data[31]
        }
        
    except Exception as e:
        return {"error": str(e)}


def format_output(result):
    """格式化输出"""
    if isinstance(result, dict) and "error" in result:
        return f"错误: {result['error']}"
    
    stock = result
    change_str = f"{stock['change']:+.3f}" if stock['change'] >= 0 else f"{stock['change']:.3f}"
    pct_str = f"{stock['change_pct']:+.2f}%" if stock['change_pct'] >= 0 else f"{stock['change_pct']:.2f}%"
    
    return (f"{stock['code']} | {stock['name']} | "
            f"¥{stock['price']:.2f} | "
            f"{pct_str} {change_str} | "
            f"今开: {stock['open']:.2f} | "
            f"高: {stock['high']:.2f} | "
            f"低: {stock['low']:.2f} | "
            f"vol: {stock['volume']/10000:.2f}万 | "
            f"time: {stock['time']}")


def main():
    parser = argparse.ArgumentParser(description='A 股实时行情查询 (新浪财经)')
    parser.add_argument('--symbol', '-s', type=str, required=True, help='股票代码 (如 600000, 000001)')
    parser.add_argument('--json', '-j', action='store_true', help='JSON 格式输出')
    
    args = parser.parse_args()
    
    # 补全代码
    code = args.symbol.zfill(6)
    if not code.startswith(('sh', 'sz')):
        # 根据代码判断市场
        if code.startswith(('5', '6', '9')):
            code = 'sh' + code
        else:
            code = 'sz' + code
    
    result = get_stock_price_sina(code)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == "__main__":
    main()
