import grpc
import device_pb2
import device_pb2_grpc

channel = grpc.insecure_channel(
    "localhost:50051"
)

stub = device_pb2_grpc.DeviceServiceStub(
    channel
)

request = device_pb2.DeviceRequest(
    device_id="motor_001"
)

response = stub.GetDevice(
    request
)

print(response)

power = device_pb2.PowerRequest(device_id="motor_001", enable=False);
response = stub.SetPower(power)

print(response)

