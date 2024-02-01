from init_apex_client import init_client
from send_order_apex import send_order_apex
import time
 
# 初始化客户端
client_apex = init_client()
configs = client_apex.configs()
 
# 获取用户和账户信息
client_apex.get_user()
client_apex.get_account()
 
 
# 发送一个市价买单
currentTime = time.time()
limitFeeRate = client_apex.account['takerFeeRate']
orderResult = send_order_apex(client_apex, symbol="BTC-USDC", side="BUY",
                                           type="MARKET", size="0.001", expirationEpochSeconds= currentTime,
                                           price="28888.5", limitFeeRate=limitFeeRate)
print(orderResult)