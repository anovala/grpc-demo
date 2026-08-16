#pragma once

#include "device.grpc.pb.h"

class DeviceServiceImpl final
    :
    public device::DeviceService::Service
{

public:
    grpc::Status GetDevice(
        grpc::ServerContext* context,
        const device::DeviceRequest* request,
        device::DeviceInfo* response
    ) override;


    grpc::Status SetPower(
        grpc::ServerContext* context,
        const device::PowerRequest* request,
        device::PowerResponse* response
    ) override;

};