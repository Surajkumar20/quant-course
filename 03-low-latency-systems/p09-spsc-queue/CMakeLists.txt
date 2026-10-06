add_library(p09_spsc INTERFACE)
target_include_directories(p09_spsc INTERFACE include)

qc_add_test(p09 tests/test_spsc_queue.cpp)
target_link_libraries(p09 PRIVATE p09_spsc)

add_executable(p09_bench bench/bench_spsc.cpp)
target_link_libraries(p09_bench PRIVATE p09_spsc Threads::Threads)
