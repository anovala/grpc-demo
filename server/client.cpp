#include <iostream>
#include <grpcpp/grpcpp.h>
#include "device.grpc.pb.h"

#ifdef _WIN32
#include <windows.h>
#endif

int main()
{

#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    auto channel = grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials());
    auto stub = device::DeviceService::NewStub(channel);

    device::DeviceRequest request;
    request.set_device_id("motor_001");

    device::DeviceInfo response;
    grpc::ClientContext context;
    auto status = stub->GetDevice(&context, request, &response);

    if (status.ok()) {
    std::cout << "[OK] 成功调用!" << std::endl;
    std::cout << "   设备: " << response.name() << std::endl;
    std::cout << "   温度: " << response.temperature() << " C" << std::endl;

    }else {
        std::cout << "Failed: " << status.error_message() << std::endl;
    }

    return 0;
}