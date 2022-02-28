# /vulcan/yaml/config.sh

parse_yml_property() {
    PARSE_PROP="$GITHUB_ACTION_PATH/yq eval %s $GITHUB_WORKSPACE/vulcan_target/.vulcan.yml"
    printf "$($(printf "$PARSE_PROP" $1))"
}

parse_yml_properties() {
	VULCAN_YML_NAME=$(parse_yml_property .name)
	VULCAN_YML_URL=$(parse_yml_property .url)
	VULCAN_YML_DOCKER_IMAGE=$(parse_yml_property .docker-image)
	VULCAN_YML_EXTRA_BUILD_ENV_SETTING_COMMAND=$(parse_yml_property .extra-build-env-setting-commands)
	VULCAN_YML_TEST_BUILD_COMMAND=$(parse_yml_property .test-build-command)
	VULCAN_YML_COVERAGE_BUILD_COMMAND=$(parse_yml_property .coverage-build-command)
	VULCAN_YML_TEST_TYPE=$(parse_yml_property .test-type)
	VULCAN_YML_TEST_LIST=$(parse_yml_property .test-list)
	VULCAN_YML_TEST_CASE=$(parse_yml_property .test-case)
	VULCAN_YML_TEST_COMMAND=$(parse_yml_property .test-command)
	VULCAN_YML_TEST_COVERAGE_COMMAND=$(parse_yml_property .test-coverage-command)
}

set_run_configure() {
    if [ -z "$VULCAN_YML_COVERAGE_BUILD_COMMAND" ] || [ -z "$VULCAN_YML_TEST_COVERAGE_COMMAND" ]; 
    then
        echo "WARNING: Not work FL."
        echo "  Set coverage-build-command and test-coverage-command in .vulcan.yml."
    else
        echo "FL will be worked."
        RUN_FL="true"
    fi
    
    if [ -z "$VULCAN_YML_TEST_BUILD_COMMAND" ] || [ -z "$VULCAN_YML_TEST_COMMAND" ]; 
    then
        echo "WARNING: Not work APR."
        echo "  Set test-build-command and test-command in .vulcan.yml."
    else
        echo "APR will be worked."	
        RUN_APR="true"
    fi
}

print_yml_configure() {
    echo ==============.vulcan.yml config==============
    echo yml.name:
	printf "$VULCAN_YML_NAME\n"
	echo yml.url:
	printf "$VULCAN_YML_URL\n"
	echo yml.docker-image:
	printf "$VULCAN_YML_DOCKER_IMAGE\n"
	echo yml.extra-build-env-setting-command:
	printf "$VULCAN_YML_EXTRA_BUILD_ENV_SETTING_COMMAND\n"
	echo yml.test-build-command:
	printf "$VULCAN_YML_TEST_BUILD_COMMAND\n"
	echo yml.coverage-build-command:
	printf "$VULCAN_YML_COVERAGE_BUILD_COMMAND\n"
	echo yml.test-type:
	printf "$VULCAN_YML_TEST_TYPE\n"
	echo yml.test-case:
	printf "$VULCAN_YML_TEST_CASE\n"
	echo yml.test-command:
	printf "$VULCAN_YML_TEST_COMMAND\n"
	echo yml.test-coverage-command:
	printf "$VULCAN_YML_TEST_COVERAGE_COMMAND\n"
	echo RUN_FL:
	printf "$RUN_FL\n"
	echo RUN_APR:
	printf "$RUN_APR\n"
	echo ==============================================
}

# exist dependency
wget -q https://github.com/mikefarah/yq/releases/download/v4.20.2/yq_linux_386 -O $GITHUB_ACTION_PATH/yq && chmod +x $GITHUB_ACTION_PATH/yq

parse_yml_properties
set_run_configure
print_yml_configure
