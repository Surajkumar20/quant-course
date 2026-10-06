add_library(p07_pde src/pde.cpp)
target_include_directories(p07_pde PUBLIC include)

qc_add_test(p07 tests/test_pde.cpp)
target_link_libraries(p07 PRIVATE p07_pde)
