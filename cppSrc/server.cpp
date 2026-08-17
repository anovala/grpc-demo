#include <grpcpp/grpcpp.h>

#include "DeviceServiceImpl.h"


int main()
{

    DeviceServiceImpl service;
    grpc::ServerBuilder builder;

    builder.AddListeningPort(
        "0.0.0.0:50051",
        grpc::InsecureServerCredentials()
    );

    builder.RegisterService(
        &service
    );

    auto server = builder.BuildAndStart();
    std::cout <<"Server running\n";
    server->Wait();

    return 0;
}