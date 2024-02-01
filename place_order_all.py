from init_apex_client import init_client
import asyncio
from send_order_apex import send_order_apex
from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
from dydx3.constants import MARKET_BTC_USD,MARKET_ETH_USD,MARKET_LINK_USD,MARKET_LTC_USD,MARKET_AVAX_USD,MARKET_ATOM_USD,MARKET_DOGE_USD,MARKET_BCH_USD,MARKET_MATIC_USD,MARKET_SOL_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET,ORDER_TYPE_LIMIT
from get_depth_data_btc import calculate_spread as calculate_spread_btc
from get_depth_data_eth import calculate_spread as calculate_spread_eth
from get_depth_data_link import calculate_spread as calculate_spread_link
from get_depth_data_ltc import calculate_spread as calculate_spread_ltc
from get_depth_data_avax import calculate_spread as calculate_spread_avax
from get_depth_data_atom import calculate_spread as calculate_spread_atom
from get_depth_data_doge import calculate_spread as calculate_spread_doge
from get_depth_data_bch import calculate_spread as calculate_spread_bch
from get_depth_data_matic import calculate_spread as calculate_spread_matic
from get_depth_data_sol import calculate_spread as calculate_spread_sol
import time
 
#价格设置需要更精确，不然发不出去！
 
# 初始化apex客户端
client_apex = init_client()
configs = client_apex.configs()
# 获取apex用户和账户信息
client_apex.get_user()
client_apex.get_account()
 
 
# 初始化dydx客户端
client_dydx = init_dydx_client()
# 获取我们的dydx仓位 ID
account_response = client_dydx.private.get_account()
position_id = account_response.data['account']['positionId']
 
arbitrage_count = 0
 
 
async def execute_trade(client_apex, client_dydx, position_id, market, spread1, spread2, size, price1,price2, symbol,s_first_price,b_first_price):
    global arbitrage_count
    if spread1 > 0.7:
        if arbitrage_count<8:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_sell = asyncio.create_task(
                send_order_apex(client_apex, symbol=symbol, side="SELL",
                                type="MARKET", size=size, expirationEpochSeconds=currentTime+100,
                                price=price1, limitFeeRate=limitFeeRate)
            )
            task_dydx_buy = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_BUY, ORDER_TYPE_LIMIT,
                                True, size, b_first_price, '0.0015', currentTime+100)
            )
            arbitrage_count += 1
            orderResult1 = await task_apex_sell
            orderResult2 = await task_dydx_buy
            print(orderResult1, orderResult2)
 
    if spread2 > 0.7:
        if arbitrage_count >-8:
            currentTime = time.time()
            limitFeeRate = client_apex.account['takerFeeRate']
            task_apex_buy = asyncio.create_task(
                send_order_apex(client_apex, symbol=symbol, side="BUY",
                                type="MARKET", size=size, expirationEpochSeconds=currentTime+100,
                                price=price2, limitFeeRate=limitFeeRate)
            )
            task_dydx_sell = asyncio.create_task(
                send_order_dydx(client_dydx, position_id, market, ORDER_SIDE_SELL, ORDER_TYPE_LIMIT,
                                True, size, s_first_price, '0.0015', currentTime+100)
            )
            arbitrage_count -= 1
            orderResult1 = await task_apex_buy
            orderResult2 = await task_dydx_sell
            print(orderResult1, orderResult2)
 
 
async def arbitrage():
    while True:
        # 计算价差
        _, _, s_first_price_dydx_btc, b_first_price_dydx_btc, _, _, _, _, spread1_btc, spread2_btc = await calculate_spread_btc()
        _, _, s_first_price_dydx_eth, b_first_price_dydx_eth, _, _, _, _, spread1_eth, spread2_eth = await calculate_spread_eth()
        _, _, s_first_price_dydx_link, b_first_price_dydx_link, _, _, _, _, spread1_link, spread2_link = await calculate_spread_link()
        _, _, s_first_price_dydx_ltc, b_first_price_dydx_ltc, _, _, _, _, spread1_ltc, spread2_ltc = await calculate_spread_ltc()
        _, _, s_first_price_dydx_avax, b_first_price_dydx_avax, _, _, _, _, spread1_avax, spread2_avax = await calculate_spread_avax()
        _, _, s_first_price_dydx_atom, b_first_price_dydx_atom, _, _, _, _, spread1_atom, spread2_atom = await calculate_spread_atom()
        _, _, s_first_price_dydx_doge, b_first_price_dydx_doge, _, _, _, _, spread1_doge, spread2_doge = await calculate_spread_doge()
        _, _, s_first_price_dydx_bch, b_first_price_dydx_bch, _, _, _, _, spread1_bch, spread2_bch = await calculate_spread_bch()
        _, _, s_first_price_dydx_matic, b_first_price_dydx_matic, _, _, _, _, spread1_matic, spread2_matic = await calculate_spread_matic()
        _, _, s_first_price_dydx_sol, b_first_price_dydx_sol, _, _, _, _, spread1_sol, spread2_sol = await calculate_spread_sol()
        # 根据价差判断是否发送交易
 
        await execute_trade(client_apex, client_dydx, position_id, MARKET_BTC_USD, spread1_btc, spread2_btc, '0.001', '18888','58888', 'BTC-USDC',s_first_price_dydx_btc,b_first_price_dydx_btc)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_ETH_USD, spread1_eth, spread2_eth, '0.01', '888','5888', 'ETH-USDC',s_first_price_dydx_eth,b_first_price_dydx_eth)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_LINK_USD, spread1_link, spread2_link, '1', '8','58', 'LINK-USDC',s_first_price_dydx_link,b_first_price_dydx_link)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_LTC_USD, spread1_ltc, spread2_ltc, '0.5', '48', '488','LTC-USDC',s_first_price_dydx_ltc,b_first_price_dydx_ltc)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_AVAX_USD, spread1_avax, spread2_avax, '1', '8', '188','AVAX-USDC',s_first_price_dydx_avax,b_first_price_dydx_avax)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_ATOM_USD, spread1_atom, spread2_atom, '3', '4', '88','ATOM-USDC',s_first_price_dydx_atom,b_first_price_dydx_atom)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_DOGE_USD, spread1_doge, spread2_doge, '300', '0.04', '2','DOGE-USDC',s_first_price_dydx_doge,b_first_price_dydx_doge)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_BCH_USD, spread1_bch, spread2_bch, '0.1', '88', '588','BCH-USDC',s_first_price_dydx_bch,b_first_price_dydx_bch)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_MATIC_USD, spread1_matic, spread2_matic, '30', '0.1', '4','MATIC-USDC',s_first_price_dydx_matic,b_first_price_dydx_matic)
        await execute_trade(client_apex, client_dydx, position_id, MARKET_SOL_USD, spread1_sol, spread2_sol, '0.5', '48', '488','SOL-USDC',s_first_price_dydx_sol,b_first_price_dydx_sol)
        # 调用 execute_trade 处理其他币种的交易逻辑
 
        await asyncio.sleep(1)
 
 
# 运行异步函数
asyncio.run(arbitrage())