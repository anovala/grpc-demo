#include "DeviceServiceImpl.h"


/*获取设备信息*/
grpc::Status
DeviceServiceImpl::GetDevice( grpc::ServerContext*, const device::DeviceRequest* request ,device::DeviceInfo* response)
{
    response->set_device_id(
        request->device_id()
    );

    response->set_name(
        "Servo Motor"
    );

    response->set_temperature(
        36.5
    );

    response->set_status(
        device::DeviceInfo::RUNNING
    );

    fmt::print("set device id to {} , temperature to 36.5, status to Running\n",request->device_id());

    return grpc::Status::OK;
}


grpc::Status
DeviceServiceImpl::SetPower( grpc::ServerContext*, const device::PowerRequest* request,device::PowerResponse* response)
{
    response->set_success(true);

    std::string powerModeStr = request->enable() ? "Power ON":"Power OFF";

    response->set_message(powerModeStr);
    fmt::print("Set device {}!\n", powerModeStr);

    return grpc::Status::OK;
}