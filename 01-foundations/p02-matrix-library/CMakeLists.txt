add_library(p02_matrix src/matrix.cpp)
target_include_directories(p02_matrix PUBLIC include)

qc_add_test(p02 tests/test_matrix.cpp)
target_link_libraries(p02 PRIVATE p02_matrix)

add_executable(p02_bench bench/bench_matmul.cpp)
