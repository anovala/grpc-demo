if(MSVC)
    # 告诉 MSVC：源文件是 UTF-8，用 UTF-8 编译字符串
    add_compile_options(/utf-8)
endif()

set(PROTO_FILE
    ${CMAKE_SOURCE_DIR}/proto/device.proto
)

set(PROTO_SRCS
    ${CMAKE_CURRENT_BINARY_DIR}/device.pb.cc
)

set(PROTO_HDRS
    ${CMAKE_CURRENT_BINARY_DIR}/device.pb.h
)

set(GRPC_SRCS
    ${CMAKE_CURRENT_BINARY_DIR}/device.grpc.pb.cc
)

set(GRPC_HDRS
    ${CMAKE_CURRENT_BINARY_DIR}/device.grpc.pb.h
)


# 生成c++的grpc代码
add_custom_command(
    OUTPUT
        ${PROTO_SRCS}
        ${PROTO_HDRS}
        ${GRPC_SRCS}
        ${GRPC_HDRS}

    COMMAND protobuf::protoc

    ARGS
        --cpp_out=${CMAKE_CURRENT_BINARY_DIR}
        --grpc_out=${CMAKE_CURRENT_BINARY_DIR}
        --plugin=protoc-gen-grpc=$<TARGET_FILE:gRPC::grpc_cpp_plugin>
        -I ${CMAKE_SOURCE_DIR}/proto
        ${PROTO_FILE}

    DEPENDS
        ${PROTO_FILE}
)

add_executable(
    server
    server.cpp
    DeviceServiceImpl.cpp
    ${PROTO_SRCS}
    ${GRPC_SRCS}
)

target_link_libraries(
    server
    gRPC::grpc++
    protobuf::libprotobuf
    fmt::fmt
)

target_include_directories(
    server
    PRIVATE
    ${CMAKE_CURRENT_BINARY_DIR}
)

add_executable(client client.cpp ${PROTO_SRCS} ${GRPC_SRCS})

target_link_libraries(client  gRPC::grpc++ protobuf::libprotobuf fmt::fmt)
target_include_directories(client PRIVATE ${CMAKE_CURRENT_BINARY_DIR})


#安装exe和dll

install(TARGETS server client
    RUNTIME DESTINATION bin 
)

install(DIRECTORY ${CMAKE_BINARY_DIR}/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/bin/
    DESTINATION bin 
    CONFIGURATIONS Release
    FILES_MATCHING PATTERN "*.dll"
    )
install(DIRECTORY ${CMAKE_BINARY_DIR}/vcpkg_installed/${VCPKG_TARGET_TRIPLET}/debug/bin/
    DESTINATION bin     
    CONFIGURATIONS Debug
    FILES_MATCHING PATTERN "*.dll"
    )
