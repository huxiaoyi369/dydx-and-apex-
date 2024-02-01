from init_dydx_client import init_dydx_client
from send_order_dydx import send_order_dydx
import time
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import ORDER_SIDE_BUY,ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_MARKET
 
 
# 初始化客户端
client_dydx = init_dydx_client()
 
# 获取我们的仓位 ID
account_response = client_dydx.private.get_account()
position_id = account_response.data['account']['positionId']
 
# 发送一个市价买单
currentTime = time.time()
orderResult = send_order_dydx(client_dydx, position_id, MARKET_BTC_USD, ORDER_SIDE_BUY, ORDER_TYPE_MARKET, True, '0.001', '28888', '0.0015', currentTime)
print('order_response',orderResult.data)