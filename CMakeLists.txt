cmake_minimum_required(VERSION 3.20)

project(grpc_demo)

set(CMAKE_CXX_STANDARD 20)

find_package(Protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)

find_package(Python3 REQUIRED COMPONENTS Interpreter)


#获取python脚本执行目录
execute_process(
    COMMAND
        ${Python3_EXECUTABLE}
        -c
        "import sysconfig; print(sysconfig.get_path('scripts'))"
    OUTPUT_VARIABLE
        PYTHON_SCRIPTS_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

#protobuf python 代码生成器

if(WIN32)
    set(MYPY_PLUGIN ${PYTHON_SCRIPTS_DIR}/protoc-gen-mypy.exe)
else()
    set(MYPY_PLUGIN ${PYTHON_SCRIPTS_DIR}/protoc-gen-mypy)
endif()

message(STATUS "mypy plugin: ${MYPY_PLUGIN}")

# ============================
# Python protobuf generation
# ============================

#找到python解释器
find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(PROTO_FILE
    ${CMAKE_SOURCE_DIR}/proto/device.proto
)

set(PYTHON_OUT_DIR
    ${CMAKE_SOURCE_DIR}/client
)


#调用protoc生成器，生成python代码
add_custom_command(

    OUTPUT
        ${PYTHON_OUT_DIR}/device_pb2.py
        ${PYTHON_OUT_DIR}/device_pb2_grpc.py
        ${PYTHON_OUT_DIR}/device_pb2.pyi
        ${PYTHON_OUT_DIR}/device_pb2_grpc.pyi

    COMMAND
        Python3::Interpreter

    ARGS
        -m grpc_tools.protoc
        -I ${CMAKE_SOURCE_DIR}/proto
        --python_out=${PYTHON_OUT_DIR}
        --grpc_python_out=${PYTHON_OUT_DIR}
        --plugin=protoc-gen-mypy=${MYPY_PLUGIN}
        --mypy_out=${PYTHON_OUT_DIR}
        ${PROTO_FILE}

    DEPENDS
        ${PROTO_FILE}

)

add_custom_target(
    python_proto
    ALL
    DEPENDS
        ${PYTHON_OUT_DIR}/device_pb2.py
        ${PYTHON_OUT_DIR}/device_pb2_grpc.py
)

add_subdirectory(server)

#安装 python脚本
install(DIRECTORY ${CMAKE_SOURCE_DIR}/client
    DESTINATION script/
)

include(InstallRequiredSystemLibraries)

set(CPACK_PACKAGE_NAME "grpc_demo")
set(CPACK_PACKAGE_VENDOR "Sola")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "gRpc Demo")
set(CPACK_PACKAGE_VERSION "1.0.0")

if(WIN32)
    set(CPACK_GENERATOR "NSIS")
    set(CPACK_NSIS_DISPLAY_NAME "gRPC-demo")
    set(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES64")
    set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}-win64")
elseif(UNIX)
    set(CPACK_GENERATOR "RPM")
    set(CPACK_RPM_PACKAGE_NAME "grpc-demo")
    set(CPACK_RPM_PACKAGE_VERSION "${CPACK_PACKAGE_VERSION}")
    set(CPACK_RPM_PACKAGE_RELEASE "1")

    set(CPACK_RPM_PACKAGE_LICENSE "MIT")

    set(CPACK_RPM_PACKAGE_DESCRIPTION
        "A gRPC client and server demo application."
    )
    set(CPACK_RPM_PACKAGE_ARCHITECTURE "${CMAKE_SYSTEM_PROCESSOR}") 
endif()

include(CPack)

