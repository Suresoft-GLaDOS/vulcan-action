import os
import subprocess


TEST_INDEX=0
VULCAN_OUTPUT_DIR = os.getenv("VULCAN_OUTPUT_DIR")
VULCAN_TARGET = os.getenv("VULCAN_TARGET")
VULCAN_YML_COVERAGE_BUILD_COMMAND = os.getenv("VULCAN_YML_COVERAGE_BUILD_COMMAND")
VULCAN_YML_TEST_COVERAGE_COMMAND = os.getenv("VULCAN_YML_TEST_COVERAGE_COMMAND")
VULCAN_YML_TEST_LIST = os.getenv("VULCAN_YML_TEST_LIST")
VULCAN_YML_TEST_CASE = os.getenv("VULCAN_YML_TEST_CASE")
VULCAN_YML_GCOV_EXCLUSION_LIST = os.getenv("VULCAN_YML_GCOV_EXCLUSION_LIST")
GITHUB_ACTION_PATH = os.getenv("GITHUB_ACTION_PATH", "/")
GCOV_PATH = os.path.join(VULCAN_OUTPUT_DIR, "gcov")


def _create_directory(path):
    os.makedirs(path, exist_ok=True)


def _clean_after_collect_gcov():
    gcov_exclusion_list = VULCAN_YML_GCOV_EXCLUSION_LIST.splitlines() if VULCAN_YML_GCOV_EXCLUSION_LIST is not None else ""
    gcov_exclusion_list_command = ''.join([' -e ' + e for e in gcov_exclusion_list])
    os.system(f"python3 {GITHUB_ACTION_PATH}/vulcan/util/gcovg.py -r {VULCAN_TARGET} -f \"*.o\" -o {VULCAN_OUTPUT_DIR}/gcov_map.json {gcov_exclusion_list_command}")
    os.system(f"find {VULCAN_TARGET} -type f -name \"*.gcov\" -exec mv {'{}'} {GCOV_PATH}/{TEST_INDEX} \;")
    os.system(f"find {VULCAN_TARGET} -type f -name \"*.gcda\" -delete")


def _split_test():
    global TEST_INDEX
    for UNIT_TEST in VULCAN_YML_TEST_LIST.splitlines():
        index = str(TEST_INDEX)
        _create_directory(os.path.join(GCOV_PATH, index))
        test_command = VULCAN_YML_TEST_COVERAGE_COMMAND.replace("@testcase@", UNIT_TEST)
        with open(os.path.join(GCOV_PATH, index, "test.command"), "w") as f:
            f.write(test_command)

        print(f"Measuring coverage for {test_command}", flush=True)
        print([test_command.replace("\"", "")])
        # test_result = os.system(test_command.replace("\""))
        test_result = subprocess.run([test_command.replace("\"", "")])

        with open(os.path.join(GCOV_PATH, index, "result.test"), "w") as f:
            if test_result != 0:
                f.write("failed")
            else:
                f.write("passed")
        _clean_after_collect_gcov()
        TEST_INDEX += 1


def run():
    print("Run VULCAN_YML_COVERAGE_BUILD_COMMAND", flush=True)
    os.chdir(VULCAN_TARGET)
    build_result = os.system("sh -c \"$VULCAN_YML_COVERAGE_BUILD_COMMAND\"")

    if build_result != 0:
        print("Build failed", flush=True)
        exit(1)

    print("Run split test by VULCAN_YML_TEST_COVERAGE_COMMAND", flush=True)
    os.chdir(VULCAN_TARGET)
    _create_directory(GCOV_PATH)
    _split_test()
    # os.system("git clean -f > /dev/null")


run()