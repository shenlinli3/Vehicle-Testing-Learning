import can
import threading
import time

# # 加载 vcan 模块
# sudo modprobe vcan

# # 创建 vcan0 接口
# sudo ip link add dev vcan0 type vcan
# sudo ip link set up vcan0

# # 创建 vcan1 接口
# sudo ip link add dev vcan1 type vcan
# sudo ip link set up vcan1

# # 可以继续创建更多，例如 vcan2, vcan3
# sudo ip link add dev vcan2 type vcan
# 
# ip link show type vcan

def send_can_frame(bus, arbitration_id, data):
    msg = can.Message(arbitration_id=arbitration_id, data=data)
    try:
        bus.send(msg)
        print(f"Sent message on {bus.channel_info}")
    except can.CanError:
        print("Failed to send message")

def receive_can_frames(bus, event):
    print(f"Listening on {bus.channel_info}")
    event.set()  # 通知发送线程接收循环已经开始
    while True:
        msg = bus.recv(timeout=10.0)  # 阻塞，并等待最多10秒
        if msg:
            print(f"Received message on {bus.channel_info}: {msg}")

def can_worker(channel):
    """为每个 vcan 接口管理的线程"""
    bus = can.interface.Bus(channel=channel, interface='socketcan')
    
    # 定义接收开始事件
    start_event = threading.Event()

    # 启动车辆总线上接收的线程
    receive_thread = threading.Thread(target=receive_can_frames, args=(bus, start_event))
    receive_thread.start()

    # 等待接收线程完全启动
    start_event.wait()
    time.sleep(1)  # optional, 提供额外准备时间
    
    # 发送 CAN 帧
    send_can_frame(bus, arbitration_id=0x123, data=[0xDE, 0xAD, 0xBE, 0xEF])

    receive_thread.join()

def main():
    channels = ['vcan0', 'vcan1', 'vcan2']
    threads = []
    for channel in channels:
        thread = threading.Thread(target=can_worker, args=(channel,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
    