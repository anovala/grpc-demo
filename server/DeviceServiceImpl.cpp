#include "DeviceServiceImpl.h"


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

    return grpc::Status::OK;
}


grpc::Status
DeviceServiceImpl::SetPower( grpc::ServerContext*, const device::PowerRequest* request,device::PowerResponse* response)
{
    response->set_success(true);

    response->set_message(
        request->enable() ? "Power ON":"Power OFF"
    );

    return grpc::Status::OK;
}