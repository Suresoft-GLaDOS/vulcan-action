import os
import datetime
import yaml

GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
VULCAN_TARGET_NAME = os.getenv("VULCAN_TARGET")
VULCAN_TARGET = os.path.join(GITHUB_WORKSPACE, VULCAN_TARGET_NAME)
VULCAN_YML_PATH = os.path.join(VULCAN_TARGET, "vulcan.yml")
VULCAN_SUFFIX = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
VULCAN_OUTPUT_DIR = os.path.realpath( os.path.join(GITHUB_WORKSPACE, "..", "..", "output", GITHUB_REPOSITORY, VULCAN_SUFFIX) )

os.environ["VULCAN_TARGET_NAME"] = VULCAN_TARGET_NAME
os.environ["VULCAN_TARGET"] = VULCAN_TARGET
os.environ["VULCAN_OUTPUT_DIR"] = VULCAN_OUTPUT_DIR


def _parse_yaml():
    with open(VULCAN_YML_PATH) as f:
        yml = yaml.safe_load(f)
    os.environ["VULCAN_YML_NAME"] = yml["name"]
    os.environ["VULCAN_YML_URL"] = yml["url"]
    os.environ["VULCAN_YML_DOCKER_IMAGE"] = yml["docker-image"]
    os.environ["VULCAN_YML_EXTRA_BUILD_ENV_SETTING_COMMAND"] = yml["extra-build-env-setting-commands"]
    os.environ["VULCAN_YML_TEST_CANDIDATES"] = yml["test-candidates"]
    os.environ["VULCAN_YML_TIME_OUT"] = yml["time-out"]
    os.environ["VULCAN_YML_MAX_PATCH"] = yml["max-patch-number"]
    os.environ["VULCAN_YML_TEST_BUILD_COMMAND"] = yml["test-build-command"]
    os.environ["VULCAN_YML_COVERAGE_BUILD_COMMAND"] = yml["coverage-build-command"]
    os.environ["VULCAN_YML_TEST_TYPE"] = yml["test-type"]
    os.environ["VULCAN_YML_TEST_LIST"] = yml["test-list"]
    os.environ["VULCAN_YML_TEST_CASE"] = yml["test-case"]
    os.environ["VULCAN_YML_TEST_COMMAND"] = yml["test-command"]
    os.environ["VULCAN_YML_TEST_COVERAGE_COMMAND"] = yml["test-coverage-command"]
    
    if not os.getenv("VULCAN_YML_COVERAGE_BUILD_COMMAND") or not os.getenv("VULCAN_YML_TEST_COVERAGE_COMMAND"):
        print("WARNING: Not work FL.")
        print("  Set coverage-build-command and test-coverage-command in .vulcan.yml.")
    else:
        print("FL will be worked.")
        os.envrion["RUN_FL"] = "true"

    if not os.getenv("VULCAN_YML_TEST_BUILD_COMMAND") or not os.getenv("VULCAN_YML_TEST_COMMAND"):
        print("WARNING: Not work APR.")
        print("  Set test-build-command and test-command in .vulcan.yml.")
    else:
        print("APR will be worked.")
        os.environ["RUN_APR"] = "true"


def main():
    os.makedirs(VULCAN_OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(VULCAN_YML_PATH):
      print("Requires vulcan.yml in your repository")
      exit(1)

    token = os.getenv("TOKEN", None)
    if token is None:
        print("Requires vulcan action input: token")
        print("Vulcan action with: token: ${{ secrets.GITHUB_TOKEN }}"
        exit(1)

    _parse_yaml()
    os.system("entry.sh")


main()