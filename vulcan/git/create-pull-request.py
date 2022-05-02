import git
import os
import datetime


GITHUB_REF_NAME = os.getenv("GITHUB_REF_NAME", None)
MSV_PATCH_DIFF_PATH = os.getenv("MSV_PATCH_DIFF_PATH", None)
VULCAN_OUTPUT_DIR = os.getenv("VULCAN_OUTPUT_DIR")
VULCAN_TARGET = os.getenv("VULCAN_TARGET", None)


def create_pull_request(patch_branch):
    pr_title = "Vulcan"
    commit = os.getenv('GITHUB_SHA')
    pr_body = f"This PR is auto-patch by Vulcan for commit: {commit}"
    pr_command = f"gh pr create -B {GITHUB_REF_NAME} -H {patch_branch} -t \"{pr_title}\" -b\"{pr_body}\""
    os.system(pr_command)


def run():
    validation_json_path = os.path.join(VULCAN_OUTPUT_DIR, "validation.json")
    if not os.path.exists(validation_json_path) and len(os.listdir(MSV_PATCH_DIFF_PATH)) != 1:
        return
    
    os.chdir(VULCAN_TARGET)
    if os.path.exists(validation_json_path):
        with open(validation_json_path) as json_file:
            json_data = json.load(json_file)
        p = json_data[0][0]
    else:
        p = os.listdir(MSV_PATCH_DIFF_PATH)[0]
    
    os.system("git clean -xdf")
    os.system(f"git checkout {GITHUB_REF_NAME}")
    os.system("git checkout .")
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    patch_branch = f"{GITHUB_REF_NAME}-auto-patch-{now}"
    os.system(f"git checkout -b {patch_branch}")
    patch_full_path = os.path.join(MSV_PATCH_DIFF_PATH, p)
    os.system(f"git apply {patch_full_path}")
    os.system(f"git add .")
    os.system("git commit -m \"Committed the automatically generated patch\"")
    os.system(f"git push origin {patch_branch}")
    create_pull_request(patch_branch)
    os.system(f"git checkout {GITHUB_REF_NAME}")

run()
