project(xpcs-eigen)

cmake_minimum_required(VERSION 3.5)

#set(CMAKE_BUILD_TYPE RELEASE)
set(CMAKE_BUILD_TYPE DEBUG)

add_definitions(-std=c++0x)

set(sources
    src/configuration.cpp
    src/h5result.cpp
    src/corr.cpp
    src/imm.cpp
    src/sparsedata.cpp
    src/funcs.cpp
    src/darkImage.cpp
    src/main.cpp)


find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()


# TODO. Fix the hard-coded path. 
include_directories("/usr/local/hdf5/include" "/usr/local/boost_1_64_0/")
link_directories("/usr/local/hdf5/lib")

add_subdirectory("src/gflags")
add_executable(corr ${sources})

target_link_libraries(corr hdf5 gflags)
