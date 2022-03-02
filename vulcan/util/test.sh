# /vulcan/util/test.sh

TEST_INDEX=1
GCOV_PATH=$GITHUB_WORKSPACE/gcov

_create_gcov_directory() {
	rm -rf $GCOV_PATH
	mkdir $GCOV_PATH
}

_write_test_result() {
	if [ ! -z $? ]; 
	then
		echo fail > $GCOV_PATH/$TEST_INDEX/result.output
	else
		echo pass > $GCOV_PATH/$TEST_INDEX/result.output
	fi
}

_clean_after_collect_gcov() {
	find $GITHUB_WORKSPACE/vulcan_target ! \( -path '$GITHUB_WORKSPACE/vulcan_target/*test*' -prune \) -type f -name "*.o" -exec gcov --preserve-paths {} \;
	mv $GITHUB_WORKSPACE/vulcan_target/*.gcov $GCOV_PATH/$TEST_INDEX
	bash -c 'find $GITHUB_WORKSPACE/vulcan_target -type f -name "*.gcda" -delete'
}

_split_test() {
	for UNIT_TEST in $(sh -c "$VULCAN_YML_TEST_LIST | grep test_")
	do
		echo "Measuring coverage for $UNIT_TEST\n"
		mkdir $GCOV_PATH/$TEST_INDEX
		sh -c "${VULCAN_YML_TEST_COVERAGE_COMMAND//\?/$UNIT_TEST}"
		
		_write_test_result
		_clean_after_collect_gcov
		
		TEST_INDEX=$(( $TEST_INDEX + 1 ))
	done
}

_create_gcov_directory
_split_test
