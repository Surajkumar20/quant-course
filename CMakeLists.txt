cmake_minimum_required(VERSION 3.20)
project(quant_course LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

if(MSVC)
  add_compile_options(/W4 /permissive-)
else()
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

option(QC_SANITIZE "Build with address + undefined-behaviour sanitizers" OFF)
if(QC_SANITIZE AND NOT MSVC)
  add_compile_options(-fsanitize=address,undefined -fno-omit-frame-pointer)
  add_link_options(-fsanitize=address,undefined)
endif()

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.15.2.zip
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

find_package(Threads REQUIRED)
enable_testing()
include(GoogleTest)

# qc_add_test(<name> <sources...>): one gtest executable, registered with ctest.
# Test names are prefixed with <name>_ so `ctest -R ^p02_` selects one project.
function(qc_add_test name)
  add_executable(${name} ${ARGN})
  target_link_libraries(${name} PRIVATE GTest::gtest_main Threads::Threads)
  gtest_discover_tests(${name} TEST_PREFIX "${name}_" DISCOVERY_TIMEOUT 60)
endfunction()

add_subdirectory(00-precourse/p00-toolchain)
add_subdirectory(01-foundations/p02-matrix-library)
add_subdirectory(02-derivatives-pricing/p05-monte-carlo-pricer)
add_subdirectory(02-derivatives-pricing/p07-pde-pricer)
add_subdirectory(03-low-latency-systems/p08-order-book)
add_subdirectory(03-low-latency-systems/p09-spsc-queue)
add_subdirectory(03-low-latency-systems/p10-feed-handler)
