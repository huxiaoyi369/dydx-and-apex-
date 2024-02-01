import subprocess
import time
 
def run_program():
    # 这里替换为你需要执行的程序命令
    process = subprocess.Popen(["python", "place_order_btc.py"])  # 例如：python your_program.py
    return process
 
if __name__ == "__main__":
    while True:
        program = run_program()
        while program.poll() is None:
            # 程序正在运行
            time.sleep(5)  # 每5秒检查一次程序状态
        # 程序已终止，等待一段时间后重启
        print("程序已终止，重新启动中...")
        time.sleep(3)  # 等待3秒