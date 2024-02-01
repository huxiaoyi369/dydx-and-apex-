import asyncio
from apexpro.http_public import HttpPublic
from dydx3 import Client
from dydx3.constants import MARKET_ETH_USD
 
 
# 定义交易对列表
symbol = 'ETHUSDC'
market = MARKET_ETH_USD
 
# 定义异步函数来获取 APEX 的价格
async def get_apex_price():
    # 初始化API客户端
    apexclient = HttpPublic("https://pro.apex.exchange")
    # 获取深度数据
    trades_data = apexclient.depth(symbol=symbol)['data']
    # 返回卖一价和买一价
    return trades_data['a'][0][0], trades_data['b'][0][0], trades_data['a'][0][1], trades_data['b'][0][1]
 
# 定义异步函数来获取 dydx 的价格
async def get_dydx_price():
    # 初始化API客户端
    dydxclient = Client(host='https://api.dydx.exchange')
    # 获取深度数据
    orderbook_response = dydxclient.public.get_orderbook(market=market)
    orderbook_data = orderbook_response.data
    # 返回卖一价和买一价
    return orderbook_data['asks'][0]['price'], orderbook_data['bids'][0]['price'], orderbook_data['asks'][0]['size'], orderbook_data['bids'][0]['size']
 
# 定义异步函数来计算价差
async def calculate_spread():
    # 创建两个任务，分别获取 APEX 和 dydx 的价格
    task1 = asyncio.create_task(get_apex_price())
    task2 = asyncio.create_task(get_dydx_price())
    # 等待两个任务完成，并获取结果
    s_first_price_apex, b_first_price_apex,s_first_size_apex,b_first_size_apex = await task1
    s_first_price_dydx, b_first_price_dydx,s_first_size_dydx,b_first_size_dydx   = await task2
    # 计算价差
    spread1 = ((float(b_first_price_apex) - float(s_first_price_dydx))/float(s_first_price_apex))*100
    spread2 = ((float(b_first_price_dydx) - float(s_first_price_apex))/float(s_first_price_dydx))*100
    return s_first_price_apex,b_first_price_apex,s_first_price_dydx,b_first_price_dydx,s_first_size_apex,b_first_size_apex,s_first_size_dydx,b_first_size_dydx,spread1,spread2
 
 
if __name__ == '__main__':
    # 创建事件循环
    loop = asyncio.get_event_loop()
    # 运行异步函数
    loop.run_until_complete(calculate_spread())
    # 关闭事件循环
    loop.close()