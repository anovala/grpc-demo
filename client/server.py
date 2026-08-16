import grpc
import device_pb2
import device_pb2_grpc
from concurrent import futures
import time
import logging
from typing import Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

class DeviceServiceImpl(device_pb2_grpc.DeviceServiceServicer):
    '''设备服务实现'''

    def __init__(self) -> None:
        # 模拟数据库（存储设备信息）
        self.devices: Dict[str, Dict[str, Any]] = {
            "motor_001": {
                "name": "电机控制器",
                "status": device_pb2.DeviceInfo.RUNNING,
                "temperature": 45.6,
                "power": True
            },
            "sensor_002": {
                "name": "温度传感器",
                "status": device_pb2.DeviceInfo.RUNNING,
                "temperature": 25.3,
                "power": True
            },
            "pump_003": {
                "name": "水泵控制器",
                "status": device_pb2.DeviceInfo.STOPPED,
                "temperature": 18.2,
                "power": False
            }
        }
        logger.info(f"设备服务初始化完成，共 {len(self.devices)} 个设备")

    def GetDevice(self, request: device_pb2.DeviceRequest, 
                  context: grpc.ServicerContext) -> device_pb2.DeviceInfo:
        """
        获取设备信息
        """
        device_id = request.device_id
        logger.info(f"收到 GetDevice 请求: device_id={device_id}")
        
        # 从"数据库"查找设备
        device_data = self.devices.get(device_id)
        
        if device_data is None:
            # 设备不存在
            logger.warning(f"设备 {device_id} 不存在")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"设备 '{device_id}' 不存在")
            return device_pb2.DeviceInfo()
        
        # 构造响应
        response = device_pb2.DeviceInfo()
        response.device_id = device_id
        response.name = device_data["name"]
        response.status = device_data["status"]
        response.temperature = device_data["temperature"]
        
        logger.info(f"GetDevice 成功: {response.name}, 状态={response.status}, 温度={response.temperature}℃")
        return response    

    def SetPower(self, request: device_pb2.PowerRequest,
                 context: grpc.ServicerContext) -> device_pb2.PowerResponse:
        """
        控制设备电源
        """
        device_id = request.device_id
        enable = request.enable
        action = "开启" if enable else "关闭"
        
        logger.info(f"收到 SetPower 请求: device_id={device_id}, action={action}")
        
        # 查找设备
        device_data = self.devices.get(device_id)
        
        if device_data is None:
            logger.warning(f"设备 {device_id} 不存在")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"设备 '{device_id}' 不存在")
            response = device_pb2.PowerResponse()
            response.success = False
            response.message = f"设备 '{device_id}' 不存在"
            return response
        
        # 执行电源控制
        old_status = device_data["status"]
        device_data["power"] = enable
        device_data["status"] = device_pb2.DeviceInfo.RUNNING if enable else device_pb2.DeviceInfo.STOPPED
        
        # 构造响应
        response = device_pb2.PowerResponse()
        response.success = True
        response.message = f"设备 '{device_id}' 已{action} (状态: {'运行' if enable else '停止'})"
        
        logger.info(f"SetPower 成功: {response.message}")
        return response        


def serve(port: int = 50051 , max_workers: int = 10) -> None:
    """
    启动 gRPC 服务器
    
    Args:
        port: 监听端口
        max_workers: 线程池大小
    """

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=[
            ('grpc.max_send_message_length', 10 * 1024 * 1024),  # 10MB
            ('grpc.max_receive_message_length', 10 * 1024 * 1024),  # 10MB
        ]
    )

    device_pb2_grpc.add_DeviceServiceServicer_to_server(
        DeviceServiceImpl(),
        server
    )

    server.add_insecure_port(f'[::]:{port}')

    server.start()
    logger.info(f"✅ gRPC 服务器启动成功")
    logger.info(f"   监听地址: 0.0.0.0:{port}")
    logger.info(f"   线程池大小: {max_workers}")
    logger.info(f"   按 Ctrl+C 停止服务...")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("收到停止信号，正在关闭服务器...")
        server.stop(0)
        logger.info("服务器已停止")        

def main():
    """主函数"""
    # 解析命令行参数
    import argparse
    parser = argparse.ArgumentParser(description='gRPC 设备服务')
    parser.add_argument('-p', '--port', type=int, default=50051,
                       help='监听端口 (默认: 50051)')
    parser.add_argument('-w', '--workers', type=int, default=10,
                       help='线程池大小 (默认: 10)')
    args = parser.parse_args()

    serve(port=args.port, max_workers=args.workers)

if __name__ == "__main__":
    main()