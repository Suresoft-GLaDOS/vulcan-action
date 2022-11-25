import datetime
import os
import pprint
import sys
import yaml

GITHUB_ACTION_PATH = os.getenv("GITHUB_ACTION_PATH", "/")
GITHUB_ACTOR = os.getenv("GITHUB_ACTOR")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
VULCAN_TARGET_NAME = os.getenv("VULCAN_TARGET")
VULCAN_TARGET = os.path.join(GITHUB_WORKSPACE, VULCAN_TARGET_NAME) if VULCAN_TARGET_NAME else GITHUB_WORKSPACE
VULCAN_TARGET_NAME = VULCAN_TARGET_NAME if VULCAN_TARGET_NAME else os.path.basename(VULCAN_TARGET)
VULCAN_YML_PATH = os.path.join(VULCAN_TARGET, "vulcan.yml")
VULCAN_SUFFIX = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
VULCAN_OUTPUT_DIR = os.path.realpath( os.path.join(GITHUB_WORKSPACE, "..", "..", "output", GITHUB_ACTOR, GITHUB_REPOSITORY, VULCAN_SUFFIX) )

# reset some environment variables
os.environ["VULCAN_TARGET_NAME"] = VULCAN_TARGET_NAME
os.environ["VULCAN_TARGET"] = VULCAN_TARGET
os.environ["VULCAN_OUTPUT_DIR"] = VULCAN_OUTPUT_DIR


def _parse_yaml():
    with open(VULCAN_YML_PATH) as f:
        yml = yaml.safe_load(f)
    for k, v in yml.items():
        if v is None:
            yml[k] = ""
        if type(v) is not str:
            yml[k] = str(v)
    
    pprint.pprint(yml)
    
    os.environ["VULCAN_YML_NAME"] = yml["name"]
    os.environ["VULCAN_YML_URL"] = yml["url"] if "url" in yml else ""
    os.environ["VULCAN_YML_DOCKER_IMAGE"] = yml["docker-image"] if "docker-image" in yml else ""
    os.environ["VULCAN_YML_EXTRA_BUILD_ENV_SETTING_COMMAND"] = yml["extra-build-env-setting-commands"]
    os.environ["VULCAN_YML_TEST_CANDIDATES"] = yml["test-candidates"]
    os.environ["VULCAN_YML_TIME_OUT"] = yml["time-out"]
    os.environ["VULCAN_YML_TEST_TIME_OUT"] = yml["test-time-out"] if "test-time-out" in yml else "3000"
    os.environ["VULCAN_YML_MAX_PATCH"] = yml["max-patch-number"]
    os.environ["VULCAN_YML_TEST_BUILD_COMMAND"] = yml["test-build-command"]
    os.environ["VULCAN_YML_COVERAGE_BUILD_COMMAND"] = yml["coverage-build-command"]
    os.environ["VULCAN_YML_GCOV_EXCLUSION_LIST"] = yml["gcov-exclusion-list"] if "gcov-exclusion-list" in yml else ""
    os.environ["VULCAN_YML_GCOV_INCLUSION_LIST"] = yml["gcov-inclusion-list"] if "gcov-inclusion-list" in yml else ""
    os.environ["VULCAN_YML_LIBRARY_LIST"] = yml["library-list"] if "library-list" in yml else ""
    os.environ["VULCAN_YML_TEST_TYPE"] = yml["test-type"]
    os.environ["VULCAN_YML_TEST_LIST"] = yml["test-list"]
    os.environ["VULCAN_YML_TEST_CASE"] = yml["test-case"]
    os.environ["VULCAN_YML_TEST_COMMAND"] = yml["test-command"]
    os.environ["VULCAN_YML_TEST_COVERAGE_COMMAND"] = yml["test-coverage-command"]
    os.environ["VULCAN_YML_BUILD_SUBDIR"] = yml["build-subdir"] if "build-subdir" in yml else ""

    if not os.getenv("VULCAN_YML_COVERAGE_BUILD_COMMAND") or not os.getenv("VULCAN_YML_TEST_COVERAGE_COMMAND"):
        print("WARNING: Not work FL.", flush=True)
        print("  Set coverage-build-command and test-coverage-command in .vulcan.yml.", flush=True)
    else:
        print("FL will be worked.", flush=True)
        os.environ["RUN_FL"] = "true"

    if not os.getenv("VULCAN_YML_TEST_BUILD_COMMAND") or not os.getenv("VULCAN_YML_TEST_COMMAND"):
        print("WARNING: Not work APR.", flush=True)
        print("  Set test-build-command and test-command in .vulcan.yml.", flush=True)
    else:
        print("APR will be worked.", flush=True)
        os.environ["RUN_APR"] = "true"


def main():
    token = os.getenv("TOKEN", None)
    if token is None:
        print("Requires vulcan action input: token", flush=True)
        print("Vulcan action with: token: ${{ secrets.GITHUB_TOKEN }}", flush=True)
        exit(1)

    if not os.path.exists(VULCAN_YML_PATH):
        print("Requires vulcan.yml in your repository", flush=True)
        exit(1)

    os.makedirs(VULCAN_OUTPUT_DIR, exist_ok=True)
    _parse_yaml()
    sys.stdout.flush()
    entry_sh_path = os.path.join(GITHUB_ACTION_PATH, "vulcan", "entry.sh")
    os.system(f"bash {entry_sh_path}")


main()