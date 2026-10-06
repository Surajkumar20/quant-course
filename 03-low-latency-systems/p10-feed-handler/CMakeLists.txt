add_library(p10_feed src/feed.cpp)
target_include_directories(p10_feed PUBLIC include)

qc_add_test(p10 tests/test_feed.cpp)
target_link_libraries(p10 PRIVATE p10_feed)
