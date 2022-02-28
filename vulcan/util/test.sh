# /vulcan/util/test.sh

TEST_INDEX=1
sh -c "$VULCAN_YML_TEST_LIST | grep test_ > AUTOMAKE_TEST_CASE.output"
GCOV_PATH=$GITHUB_WORKSPACE/gcov

rm -rf $GCOV_PATH
mkdir $GCOV_PATH

for UNIT_TEST in $(cat AUTOMAKE_TEST_CASE.output)
do
    echo "$UNIT_TEST\n"
    head -$TEST_INDEX AUTOMAKE_TEST_CASE.output | tail -1 > TEST_CASE.output
	sh -c "$VULCAN_YML_TEST_COVERAGE_COMMAND"
	
	mkdir $GCOV_PATH/$TEST_INDEX
	if [ ! -z $? ]; 
	then
		$GCOV_PATH/$TEST_INDEX/output > fail
	else
		$GCOV_PATH/$TEST_INDEX/output > pass
	fi
	
	bash -c 'find $GITHUB_WORKSPACE/vulcan_target -type f -name "*.gcov" -execdir mv {} $GCOV_PATH/$TEST_INDEX \;'
	bash -c 'find $GITHUB_WORKSPACE/vulcan_target -type f -name "*.gcda" -delete'
	
	TEST_INDEX=$(( $TEST_INDEX + 1 ))
done

