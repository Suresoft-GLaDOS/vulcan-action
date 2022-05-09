# /vulcan/util/test.sh

TEST_INDEX=1
GCOV_PATH=$VULCAN_OUTPUT_DIR/gcov

_create_gcov_directory() {
	mkdir -p $GCOV_PATH
}

_write_test_command() {
	printf "${VULCAN_YML_TEST_COVERAGE_COMMAND/@testcase@/$UNIT_TEST}" > $GCOV_PATH/$TEST_INDEX/test.command
}

_write_test_result() {
	if [ ! $? -eq 0 ];
	then
		echo failed > $GCOV_PATH/$TEST_INDEX/result.test
	else
		echo passed > $GCOV_PATH/$TEST_INDEX/result.test
	fi
}

_clean_after_collect_gcov() {
	# find $VULCAN_TARGET ! \( -path '*test*' -prune \) -type f -name "*.o" -execdir gcov --preserve-paths {} \;
	python3 ${GITHUB_ACTION_PATH}/vulcan/util/gcovg.py -r $VULCAN_TARGET -f "*.o" -o ${VULCAN_OUTPUT_DIR}/gcov_map.json
	find $VULCAN_TARGET -type f -name "*.gcov" -exec mv {} $GCOV_PATH/$TEST_INDEX \;
	# mv $VULCAN_TARGET/*.gcov $GCOV_PATH/$TEST_INDEX
	# genhtml $GCOV_PATH/$TEST_INDEX/generated.info --output-directory=$GCOV_PATH/$TEST_INDEX/html > /dev/null
	find $VULCAN_TARGET -type f -name "*.gcda" -delete
}

_split_test() {
	while read UNIT_TEST
	do
		echo "Measuring coverage for $UNIT_TEST"
		mkdir $GCOV_PATH/$TEST_INDEX
		_write_test_command
		
		sh -c "${VULCAN_YML_TEST_COVERAGE_COMMAND/@testcase@/$UNIT_TEST}"
		_write_test_result
		_clean_after_collect_gcov
		
		TEST_INDEX=$(( $TEST_INDEX + 1 ))
	done <<< $VULCAN_YML_TEST_CASE
}

echo "Run VULCAN_YML_COVERAGE_BUILD_COMMAND"
cd $VULCAN_TARGET
sh -c "$VULCAN_YML_COVERAGE_BUILD_COMMAND"

if [ ! $? -eq 0 ]; then
  echo "Build failed"
  exit 1
fi

echo "Run split test by VULCAN_YML_TEST_COVERAGE_COMMAND"
cd $VULCAN_TARGET
_create_gcov_directory
_split_test
git clean -f > /dev/null
