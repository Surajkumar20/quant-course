add_library(p08_book src/order_book.cpp)
target_include_directories(p08_book PUBLIC include)

qc_add_test(p08 tests/test_order_book.cpp)
target_link_libraries(p08 PRIVATE p08_book)

add_executable(p08_bench bench/bench_book.cpp)
target_link_libraries(p08_bench PRIVATE p08_book)
