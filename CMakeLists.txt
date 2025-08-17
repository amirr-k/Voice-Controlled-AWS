cmake_minimum_required(VERSION 3.10)     # Requires CMake 3.10+
project(AudioService)                    # Project name
set(CMAKE_CXX_STANDARD 11)            
add_executable(audio_service audio_service.cpp)

# Download httplib.h if missing
if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/httplib.h")
    file(DOWNLOAD 
        "https://raw.githubusercontent.com/yhirose/cpp-httplib/master/httplib.h"
        "${CMAKE_CURRENT_SOURCE_DIR}/httplib.h"
    )
endif()

target_include_directories(audio_service PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})