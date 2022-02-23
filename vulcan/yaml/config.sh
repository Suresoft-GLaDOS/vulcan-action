# /vulcan/yaml/config.sh

# exist dependency
wget -q https://github.com/mikefarah/yq/releases/download/v4.20.2/yq_linux_386 -O $GITHUB_ACTION_PATH/yq && chmod +x $GITHUB_ACTION_PATH/yq

PARSE_PROP="$GITHUB_ACTION_PATH/yq eval '$1' $GITHUB_WORKSPACE/vulcan_target/.vulcan.yml"
VULCAN_YML_NAME=$($(printf $PARSE_PROP .name))
VULCAN_YML_URL=$($(printf $PARSE_PROP .url))
VULCAN_YML_DOCKER_IMAGE=$($(printf $PARSE_PROP .docker-image))
VULCAN_YML_EXTRA_BUILD_ENV_SETTING_COMMAND=$($(printf $PARSE_PROP .extra-build-env-setting-commands))
VULCAN_YML_TEST_BUILD_COMMAND=$($(printf $PARSE_PROP .test-build-command))
VULCAN_YML_COVERAGE_BUILD_COMMAND=$($(printf $PARSE_PROP .test-build-command))
VULCAN_YML_COVERAGE_BUILD_COMMAND=$($GITHUB_ACTION_PATH/yq eval '.coverage-build-command')
VULCAN_YML_TEST_TYPE=$($(printf $PARSE_PROP .test-type))
VULCAN_YML_TEST_CASE=$($(printf $PARSE_PROP .test-case))
VULCAN_YML_TEST_COMMAND=$($(printf $PARSE_PROP .test-command))
VULCAN_YML_TEST_COVERAGE_COMMAND=$($(printf $PARSE_PROP .test-coverage-command))

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
