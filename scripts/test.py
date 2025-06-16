
import threading
import time
import can
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# CAN 接口列表
CAN_INTERFACES = ['vcan0', 'vcan1', 'vcan2']

# 锁用于线程安全的日志输出
log_lock = threading.Lock()

def send_message(interface):
    """发送 CAN 消息"""
    try:
        bus = can.interface.Bus(interface='socketcan', channel=interface, bitrate=500000)
        for i in range(5):
            msg = can.Message(arbitration_id=0x123, data=[i, i+1, i+2, i+3, i+4, i+5, i+6, i+7], is_extended_id=False)
            bus.send(msg)
            logging.info(f"Sent message on {interface}: {msg}")
        bus.shutdown()
    except Exception as e:
        logging.error(f"Error on {interface}: {e}")

def receive_messages():
    """监听所有 CAN 接口的消息"""
    try:
        for interface in CAN_INTERFACES:
            bus = can.interface.Bus(interface='socketcan', channel=interface, bitrate=500000)
            logging.info(f"Listening on {interface}")
            while True:
                msg = bus.recv(timeout=1.0)  # 设置超时
                if msg:
                    logging.info(f"Received message on {interface}: {msg}")
                time.sleep(0.1)
    except Exception as e:
        logging.error(f"Error in receive thread: {e}")

def main():
    # 启动接收线程
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    # 启动发送线程
    threads = []
    for interface in CAN_INTERFACES:
        thread = threading.Thread(target=send_message, args=(interface,))
        threads.append(thread)
        thread.start()

    # 等待所有发送线程完成
    for thread in threads:
        thread.join()

    # 等待接收线程完成
    receive_thread.join()

if __name__ == "__main__":
    main()
