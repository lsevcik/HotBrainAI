cmake_minimum_required(VERSION 3.24)
project(ClearScans)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_FLAGS " -static -static-libgcc -static-libstdc++ -std=c++23")

add_executable(ClearScans clearScans.cpp)
