import json
import os
import shutil
import yaml

GITHUB_ACTION_PATH = os.getenv("GITHUB_ACTION_PATH")
VULCAN_OUTPUT_DIR_BASE = os.environ["VULCAN_OUTPUT_DIR_BASE"] = os.getenv("VULCAN_OUTPUT_DIR")
VULCAN_TARGET_NAME = os.getenv("VULCAN_TARGET_NAME")
VULCAN_TARGET = os.getenv("VULCAN_TARGET")
VULCAN_YML_PATH = os.path.join(VULCAN_TARGET, "vulcan.yml")
VULCAN_YML_TIME_OUT = os.getenv("VULCAN_YML_TIME_OUT")
VULCAN_YML_TEST_TIME_OUT = os.getenv("VULCAN_YML_TEST_TIME_OUT")
RUN_FL = os.getenv("RUN_FL")
RUN_APR = os.getenv("RUN_APR")

# for SBFL
SBFL_REPO = os.environ["SBFL_REPO"] = r"/home/workspace/sbfl"

# for MSV
MSV_REPO = os.environ["MSV_REPO"] = r"/home/workspace/msv"
MSV_SEARCH_REPO = os.environ["MSV_SEARCH_REPO"] = r"/home/workspace/msv-search"

# for Client
CLIENT_REPO = os.environ["CLIENT"] = r"/home/workspace/client"

# mutable environment variables
MUTABLE_ENV = dict()


def set_environments(vulcan_output_path):
    # --------- mutable path ---------
    os.makedirs(vulcan_output_path, exist_ok=True)
    MUTABLE_ENV["VULCAN_OUTPUT_DIR"] = os.environ["VULCAN_OUTPUT_DIR"] = vulcan_output_path
    MUTABLE_ENV["CXBUILD_OUTPUT_DIR"] = os.environ["CXBUILD_OUTPUT_DIR"] = MUTABLE_ENV["VULCAN_OUTPUT_DIR"]

    MUTABLE_ENV["FL_JSON"] = os.environ["FL_JSON"] = os.path.join(MUTABLE_ENV["VULCAN_OUTPUT_DIR"], "fl.json")
    MUTABLE_ENV["INFO_JSON"] = os.environ["INFO_JSON"] = os.path.join(MUTABLE_ENV["VULCAN_OUTPUT_DIR"], "info.json")
    MUTABLE_ENV["FL_CLUSTER_JSON"] = os.environ["FL_CLUSTER_JSON"] = os.path.join(MUTABLE_ENV["VULCAN_OUTPUT_DIR"], "fl_cluster.json")

    MUTABLE_ENV["MSV_WORKSPACE"] = os.environ["MSV_WORKSPACE"] = f"{MUTABLE_ENV['VULCAN_OUTPUT_DIR']}/msv-workspace"
    MUTABLE_ENV["VULCAN_TARGET_WORKDIR"] = os.environ["VULCAN_TARGET_WORKDIR"] = f"{MUTABLE_ENV['VULCAN_OUTPUT_DIR']}/msv-workspace/{VULCAN_TARGET_NAME}-workdir"
    MUTABLE_ENV["MSV_JSON"] = os.environ["MSV_JSON"] = f"{MUTABLE_ENV['VULCAN_OUTPUT_DIR']}/msv-output/msv-result.json"
    MUTABLE_ENV["MSV_PASS_JSON"] = os.environ["MSV_PASS_JSON"] = f"{MUTABLE_ENV['VULCAN_OUTPUT_DIR']}/msv-output/msv-result-pass.json"
    MUTABLE_ENV["MSV_PATCH_DIFF_PATH"] = os.environ["MSV_PATCH_DIFF_PATH"] = f"{MUTABLE_ENV['VULCAN_OUTPUT_DIR']}/patch"
    # --------------------------------


def run_test():
    """
    1. run test & collect gcov
    """
    testrun_py_path = os.path.join(GITHUB_ACTION_PATH, "vulcan", "util", "testrun.py")
    testrun_cmd = f"python3 {testrun_py_path}"
    os.system(testrun_cmd)


def run_fl():
    """
    1. run sbfl
    """
    os.chdir(SBFL_REPO)
    fl_cmd = f"python3 -m sbfl -f Jaccard {MUTABLE_ENV['VULCAN_OUTPUT_DIR']}/gcov/* -s {MUTABLE_ENV['FL_JSON']} -i {MUTABLE_ENV['INFO_JSON']} -c {MUTABLE_ENV['FL_CLUSTER_JSON']}"
    print(f"[DEBUG] {fl_cmd}", flush=True)
    os.system(fl_cmd)


def run_apr():
    """
    1. generate metaprogram
    2. search plausible patch configuration
    3. generate patch diff
    4. write msv-result-pass.json
    """
    os.chdir(MUTABLE_ENV['VULCAN_OUTPUT_DIR'])
    os.makedirs(MUTABLE_ENV['MSV_WORKSPACE'], exist_ok=True)
    
    msv_runner_cmd = f"python3 {MSV_REPO}/msv-runner.py -s {MUTABLE_ENV['FL_JSON']} -r {VULCAN_TARGET} {MUTABLE_ENV['MSV_WORKSPACE']} {MSV_REPO}"
    print(f"[DEBUG] {msv_runner_cmd}", flush=True)
    os.system(msv_runner_cmd)
    
    msv_search_cmd = f"python3 {MSV_SEARCH_REPO}/msv-search.py -o {MUTABLE_ENV['VULCAN_OUTPUT_DIR']}/msv-output -w {MUTABLE_ENV['VULCAN_TARGET_WORKDIR']} -T {VULCAN_YML_TIME_OUT} -t {VULCAN_YML_TEST_TIME_OUT} -m prophet -p {MSV_REPO} --use-pass-test -- {MSV_REPO}/tools/msv-test.py {MUTABLE_ENV['VULCAN_TARGET_WORKDIR']}/src {MUTABLE_ENV['VULCAN_TARGET_WORKDIR']}/tests {MUTABLE_ENV['VULCAN_TARGET_WORKDIR']}"
    print(f"[DEBUG] {msv_search_cmd}", flush=True)
    os.system(msv_search_cmd)
    
    diff_gen_cmd = f"python3 {MSV_SEARCH_REPO}/diff_gen.py -g -i {MUTABLE_ENV['VULCAN_OUTPUT_DIR']}/msv-output -o {MUTABLE_ENV['VULCAN_OUTPUT_DIR']}/patch {MUTABLE_ENV['VULCAN_TARGET_WORKDIR']}"
    print(f"[DEBUG] {diff_gen_cmd}", flush=True)
    os.system(diff_gen_cmd)
    
    with open(MUTABLE_ENV["MSV_JSON"]) as f:
        json_data = json.load(f)
    with open(MUTABLE_ENV["MSV_PASS_JSON"], "w") as f:
        plausible_data = [x for x in json_data if x["pass_result"]]
        json.dump(plausible_data, f)


def run_validate():
    """
    1. run validator
    """
    validation_cmd = f"python3 {os.path.join(CLIENT_REPO, 'client.py')}"
    print(f"[DEBUG] {validation_cmd}", flush=True)
    os.system(validation_cmd)


def run_create_issue():
    os.chdir(VULCAN_TARGET)
    create_issue_sh_path = os.path.join(GITHUB_ACTION_PATH, "vulcan", "git", "create-issue.sh")
    create_issue_cmd = f"bash {create_issue_sh_path}"
    os.system(create_issue_cmd)


def run_create_pull_request():
    create_pull_request_py_path = os.path.join(GITHUB_ACTION_PATH, "vulcan", "git", "create-pull-request.py")
    create_pr_cmd = f"python3 {create_pull_request_py_path}"
    os.system(create_pr_cmd)


def handle_cluster(cluster_data):
    with open(VULCAN_YML_PATH) as f:
        origin_yaml_data = yaml.safe_load(f)
    for k in cluster_data:
        set_environments(os.path.join(VULCAN_OUTPUT_DIR_BASE, k))
        yaml_data = origin_yaml_data.copy()
        exclusion_list = []
        for c in filter(lambda v: v != cluster_data[k], cluster_data.values() ):
            exclusion_list.extend(list(map(lambda p: p.split("/")[-1], c)))
        shutil.copytree(f"{VULCAN_OUTPUT_DIR_BASE}/gcov", f"{MUTABLE_ENV['VULCAN_OUTPUT_DIR']}/gcov", dirs_exist_ok=True, ignore=lambda *args: exclusion_list)
        test_list = yaml_data["test-list"].splitlines()
        for i, e in enumerate(exclusion_list):
            del test_list[int(e)-i]
        test_list = "\n".join(test_list)
        yaml_data["test-list"] = test_list
        with open(VULCAN_YML_PATH, "w") as f:
            yaml.dump(yaml_data, f)
        run_fl()
        if RUN_APR:
            run_apr()
        if not os.path.exists(MUTABLE_ENV["MSV_PATCH_DIFF_PATH"]):
            os.makedirs(MUTABLE_ENV["MSV_PATCH_DIFF_PATH"], exist_ok=True)
        if len(os.listdir(MUTABLE_ENV["MSV_PATCH_DIFF_PATH"])) > 1:
            run_validate()
        run_create_issue()
        if len(os.listdir(MUTABLE_ENV["MSV_PATCH_DIFF_PATH"])) > 0:
            run_create_pull_request()


def run_modules():
    set_environments(VULCAN_OUTPUT_DIR_BASE)
    if RUN_FL:
        run_test()
        run_fl()
    if os.path.exists(MUTABLE_ENV["FL_CLUSTER_JSON"]):
        with open(MUTABLE_ENV["FL_CLUSTER_JSON"]) as f:
            cluster_data = json.load(f)
        if len(cluster_data) > 1:
            handle_cluster(cluster_data)
            return
    if RUN_APR:
        run_apr()
    if not os.path.exists(MUTABLE_ENV["MSV_PATCH_DIFF_PATH"]):
        os.makedirs(MUTABLE_ENV["MSV_PATCH_DIFF_PATH"], exist_ok=True)
    if len(os.listdir(MUTABLE_ENV["MSV_PATCH_DIFF_PATH"])) > 1:
        run_validate()
    run_create_issue()
    if len(os.listdir(MUTABLE_ENV["MSV_PATCH_DIFF_PATH"])) > 0:
        run_create_pull_request()


run_modules()
