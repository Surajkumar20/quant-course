add_library(p05_mc src/mc.cpp)
target_include_directories(p05_mc PUBLIC include)
target_link_libraries(p05_mc PUBLIC Threads::Threads)

qc_add_test(p05 tests/test_mc.cpp)
target_link_libraries(p05 PRIVATE p05_mc)
