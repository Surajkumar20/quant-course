add_library(p00_tvm src/tvm.cpp)
target_include_directories(p00_tvm PUBLIC include)

qc_add_test(p00 tests/test_tvm.cpp)
target_link_libraries(p00 PRIVATE p00_tvm)
