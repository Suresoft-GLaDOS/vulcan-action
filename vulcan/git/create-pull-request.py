import git
import json
import os
import datetime


GITHUB_REF_NAME = os.getenv("GITHUB_REF_NAME", None)
MSV_PATCH_DIFF_PATH = os.getenv("MSV_PATCH_DIFF_PATH", None)
VULCAN_OUTPUT_DIR = os.getenv("VULCAN_OUTPUT_DIR")
VULCAN_TARGET = os.getenv("VULCAN_TARGET", None)
VALIDATION_REPORT_DIR = os.path.join(VULCAN_OUTPUT_DIR, "validation")

PR_INFO = dict()


def construct_pr_info():
    with open(os.path.join(VULCAN_OUTPUT_DIR, "issue_link")) as f:
        PR_INFO["issue_link"] = f.read().strip()
    PR_INFO["issue_number"] = PR_INFO["issue_link"].split("/")[-1]
    
    print(f"[DEBUG] generate pr title", flush=True)
    pr_title = f"Fixed #{PR_INFO['issue_number']}"
    PR_INFO["title"] = pr_title


def create_pull_request(patch_branch):
    pr_title = PR_INFO["title"]
    commit = os.getenv('GITHUB_SHA')
    pr_body = f"This PR is auto-patch by Vulcan for commit: {commit} Fixed #{PR_INFO['issue_number']}"
    pr_command = f"gh pr create -B {GITHUB_REF_NAME} -H {patch_branch} -t \"{pr_title}\" -b\"{pr_body}\""
    os.system(pr_command)


def run():
    print(f"[DEBUG] create pr", flush=True)
    validation_json_path = os.path.join(VALIDATION_REPORT_DIR, "validation.json")
    
    os.chdir(VULCAN_TARGET)
    if os.path.exists(validation_json_path):
        with open(validation_json_path) as json_file:
            json_data = json.load(json_file)
        p = json_data["results"][0]["id"]
    else:
        p = os.listdir(MSV_PATCH_DIFF_PATH)[0]
    
    os.system("git clean -xdf")
    os.system(f"git checkout {GITHUB_REF_NAME}")
    os.system("git checkout .")
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    patch_branch = f"{GITHUB_REF_NAME}-auto-patch-{now}"
    os.system(f"git checkout -b {patch_branch}")
    patch_full_path = os.path.join(MSV_PATCH_DIFF_PATH, p)
    os.system(f"patch -p0 < {patch_full_path}")
    os.system(f"git add .")
    os.system(f"git commit -m \"Fixed automatically #{PR_INFO['issue_number']} by Vulcan\"")
    os.system(f"git push origin {patch_branch}")
    create_pull_request(patch_branch)
    os.system(f"git checkout {GITHUB_REF_NAME}")


construct_pr_info()
run()
