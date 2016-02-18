all-traces: basic.trace \
						meng-thesis-example.trace \
						array-overflow.trace \
						array-param.trace \
						struct-basic.trace \
						globals.trace \
						string-array.trace \
						structs-and-arrays.trace \
						pointer-chain.trace \
						typedef-test.trace \
						type-qualifiers.trace \
						shadowing.trace \
						pointers-gone-wild.trace \
						number-types.trace \
						fjalar-ArraysInStructTest.trace \
						fjalar-ArrayTest.trace \
						fjalar-CoercePointerTest.trace \
						fjalar-crazy-test-1.trace \
						fjalar-FloatTest.trace \
						fjalar-function-pointer.trace \
						fjalar-functions.trace \
						fjalar-GlobalTest.trace \
						fjalar-inline-func.trace \
						fjalar-IntTest.trace \
						fjalar-local-ptr.trace \
						fjalar-MultiDimArrayTest.trace \
						fjalar-NestedStructTest.trace \
						fjalar-NestedStructVarList.trace \
						fjalar-pointer-levels.trace \
						fjalar-PointerTest.trace \
						fjalar-small-test.trace \
						fjalar-StaticArraysTest.trace \
						fjalar-string-arrays.trace \
						fjalar-StructPtrTest.trace \
						fjalar-TrivialTest.trace \
						fjalar-TypedefTest.trace \
            ex1.trace \
            reverse_llist.trace \

#%: %.c
#	@gcc -ggdb -O0 -fno-omit-frame-pointer $< -o $@

# use '|| true' to always return success and keep 'make' running even on errors
#%.vgtrace: % ../valgrind-3.11.0/inst/bin/valgrind
#	../valgrind-3.11.0/inst/bin/valgrind --tool=memcheck --source-filename=$<.c --trace-filename=$<.vgtrace ./$< || true

%.vgtrace: %.c ../valgrind-3.11.0/inst/bin/valgrind
	@gcc -ggdb -O0 -fno-omit-frame-pointer $< -o $(basename $@).o
	@../valgrind-3.11.0/inst/bin/valgrind --tool=memcheck --source-filename=$< --trace-filename=$(basename $<).vgtrace ./$(basename $<).o || true

%.trace: %.vgtrace ../vg_to_opt_trace.py
	python2.7 ../vg_to_opt_trace.py --create_jsvar=trace $(basename $<) > $(basename $<).trace || true

clean:
	rm -f *.trace *.vgtrace *.out *.o
