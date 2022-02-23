# /vulcan/yaml/config.sh

# exist dependency
wget -q https://github.com/mikefarah/yq/releases/download/v4.20.2/yq_linux_386 -O $GITHUB_ACTION_PATH/yq && chmod +x $GITHUB_ACTION_PATH/yq

VULCAN_YML_NAME=$($GITHUB_ACTION_PATH/yq eval '.name')
VULCAN_YML_URL=$($GITHUB_ACTION_PATH/yq eval '.url')
VULCAN_YML_DOCKER_IMAGE=$($GITHUB_ACTION_PATH/yq eval '.docker-image')
VULCAN_YML_EXTRA_BUILD_ENV_SETTING_COMMAND=$($GITHUB_ACTION_PATH/yq eval '.extra-build-env-setting-commands')
VULCAN_YML_TEST_BUILD_COMMAND=$($GITHUB_ACTION_PATH/yq eval '.test-build-command')
VULCAN_YML_COVERAGE_BUILD_COMMAND=$($GITHUB_ACTION_PATH/yq eval '.coverage-build-command')
VULCAN_YML_TEST_TYPE=$($GITHUB_ACTION_PATH/yq eval '.test-type')
VULCAN_YML_TEST_CASE=$($GITHUB_ACTION_PATH/yq eval '.test-case')
VULCAN_YML_TEST_COMMAND=$($GITHUB_ACTION_PATH/yq eval '.test-command')
VULCAN_YML_TEST_COVERAGE_COMMAND=$($GITHUB_ACTION_PATH/yq eval '.test-coverage-command')

echo .vulcan.yml.name: ${VULCAN_YML_NAME:-Not set}
echo .vulcan.yml.url: ${VULCAN_YML_URL:-Not set}
echo .vulcan.yml.docker-image: ${VULCAN_YML_DOCKER_IMAGE:-Not set}
echo .vulcan.yml.extra-build-env-setting-command: ${VULCAN_YML_EXTRA_BUILD_ENV_SETTING_COMMAND:-Not set}
echo .vulcan.yml.test-build-command: ${VULCAN_YML_TEST_BUILD_COMMAND:-Not set}
echo .vulcan.yml.coverage-build-command: ${VULCAN_YML_COVERAGE_BUILD_COMMAND:-Not set}
echo .vulcan.yml.test-type: ${VULCAN_YML_TEST_TYPE:-Not set}
echo .vulcan.yml.test-case: ${VULCAN_YML_TEST_CASE:-Not set}
echo .vulcan.yml.test-command: ${VULCAN_YML_TEST_COMMAND:-Not set}
echo .vulcan.yml.test-coverage-command: ${VULCAN_YML_TEST_COVERAGE_COMMAND:-Not set}
