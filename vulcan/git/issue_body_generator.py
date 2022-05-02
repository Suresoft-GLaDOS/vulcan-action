import itertools
import json
import os

GITHUB_ACTOR = os.getenv("GITHUB_ACTOR", None)
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_SERVER_URL = os.getenv("GITHUB_SERVER_URL")
GITHUB_SHA = os.getenv("GITHUB_SHA")
VULCAN_OUTPUT_DIR = os.getenv("VULCAN_OUTPUT_DIR")
VULCAN_TARGET = os.getenv("VULCAN_TARGET")
VULCAN_TRIGGER_URL = f"{GITHUB_SERVER_URL}/{GITHUB_REPOSITORY}/blob/{GITHUB_SHA}"
CODE_BLOCK = "\x60\x60\x60"
CODE_BLOCK_FORMAT = "diff"


def _open_collapsed_section(body, description):
    return f"{body}\n\n<details><summary>{description}</summary>\n"


def _close_collapsed_section(body):
    return f"{body}\n\n</details>\n"


def _write_5_more_equal_fl_info(body, fl_info):
    content1 = "Clicking on the link, you take the page with code highlighted."
    content2 = "There are a lot of the suspicious code snippets and show 5 among them."
    content3 = "Recommend that split your tests or adde new tests."
    body = f"{body}\n\n----\n{content1}\n{content2}\n{content3}\n"
    body = _open_collapsed_section(body, "Click here for FL information")
    for d in fl_info:
        buggy_source = d[0]
        buggy_line = d[1]
        buggy_score = d[2]
        body = f"{body}\n\n----\nSuspicious score: {buggy_score:.2f} {VULCAN_TRIGGER_URL}/{buggy_source}#L{buggy_line}\n"
    
    body = _close_collapsed_section(body)
    return body


def _write_basic_fl_info(body, fl_info):
    buggy_source = fl_info[0][0]
    buggy_line = fl_info[0][1]
    buggy_score = fl_info[0][2]
    content1 = "Clicking on the link, you take the page with code highlighted."
    content2 = "Here is most suspicious code piece."
    content3 = "Recommend debugging here.\nClick below the collapsed section for more FL information."
    body = f"{body}\n\n{content1}\n- [ ] {content2}\n{VULCAN_TRIGGER_URL}/{buggy_source}#L{buggy_line}\n{content3}\n"
    body = _open_collapsed_section(body, "Click here for more FL")
    for d in fl_info[1:]:
        buggy_source = d[0]
        buggy_line = d[1]
        buggy_score = d[2]
        body = f"{body}\n\n----\nSuspicious score: {buggy_score:.2f} {VULCAN_TRIGGER_URL}/{buggy_source}#L{buggy_line}\n"
    body = _close_collapsed_section(body)
    return body


def _gen_info():
    body = f"This issue is generated by Vulcan for commit: {GITHUB_SHA}\n"
    info_json = os.path.join(VULCAN_OUTPUT_DIR, "info.json")
    with open(info_json) as json_file:
        info_data = json.load(json_file)
    coverage_info = info_data["coverage"]
    sources_info = info_data["sources"]
    passing_tests_info = info_data["test"]["passing"]
    failed_tests_info = info_data["test"]["failing"]
    total_test = len(passing_tests_info) + len(failed_tests_info)
    
    body = f"{body}\nCoverage: {coverage_info} percent\n"
    body = _open_collapsed_section(body, "Click here for a list of target sources")
    for s in sources_info:
        source_name = s.replace(".gcov", "")
        body = f"{body}\n\n[{source_name}]({VULCAN_TRIGGER_URL}/{source_name})"
    body = _close_collapsed_section(body)
    
    failed_tests_info_content = f"There is(are) {len(failed_tests_info)}/{total_test} failed test(s)"
    body = f"{body}\n\n{failed_tests_info_content}"
    body = _open_collapsed_section(body, "Click here for the failed test commands")
    for i, f in enumerate(failed_tests_info):
        command_file = os.path.join(f, "test.command")
        with open(command_file) as cmd_file:
            test_command = cmd_file.read()
        failed_test_content = f"{i+1}. [FAILED] {test_command}"
        body = f"{body}\n\n{failed_test_content}"
    body = _close_collapsed_section(body)
    return body


def _gen_fl_info():
    body = ""
    with open(os.path.join(VULCAN_OUTPUT_DIR, "fl.json")) as f:
        f_json = sorted(json.load(f), key=lambda k: k[2], reverse=True)
        with open(os.path.join(VULCAN_OUTPUT_DIR, "fl_sortby_score.json"), "w") as sort_f:
            json.dump(f_json, sort_f)
        with open(os.path.join(VULCAN_OUTPUT_DIR, "fl_top5.json"), "w") as top_f:
            json.dump(f_json[:5], top_f)
    
    if len(list(itertools.groupby(f_json[:5], lambda d: d[2]))) == 1:
        body = _write_5_more_equal_fl_info(body, f_json[:5])
    else:
        body = f"{body}\n\n----"
        body = _open_collapsed_section(body, "Click here for FL information")
        body = _write_basic_fl_info(body, f_json[:5])
        body = _close_collapsed_section(body)
    return body


def _gen_patch_info():
    body = ""
    plausible_count = os.getenv("VULCAN_PLAUSIBLE_COUNT")
    body = f"{body}\n\n----\n{plausible_count} patch(es) generaetd by vulcan\n"
    body = _open_collapsed_section(body, "plausible patch diff info")
    validation_json_path = os.path.join(VULCAN_OUTPUT_DIR, "validation.json")
    if os.path.exists(validation_json_path):
        with open(validation_json_path) as json_file:
            json_data = json.load(json_file)
    for i, p in enumerate(os.listdir(os.path.join(VULCAN_OUTPUT_DIR, "patch"))):
        if os.path.exists(validation_json_path):
            p = json_data[i][0]
        p_full_path = os.path.join(VULCAN_OUTPUT_DIR, "patch", p)
        with open(p_full_path) as f:
            code = f.read()
        body = f"{body}\n\n----\n{CODE_BLOCK} {CODE_BLOCK_FORMAT}\n{code}\n{CODE_BLOCK}\n"
    body = _close_collapsed_section(body)
    return body


def generate_issue_body():
    '''
    |     info     |
    | ------------ |
    |   fl info    |
    | ------------ |
    |  patch info  |
    '''
    title = "Vulcan"
    info = _gen_info()
    fl_info = _gen_fl_info()
    if os.listdir(os.getenv("MSV_PATCH_DIFF_PATH")):
        patch_info = _gen_patch_info()
    body = f"{info}{fl_info}{patch_info}"
    with open(os.path.join(VULCAN_OUTPUT_DIR, "issue_body"), "w") as f:
        f.write(body)


generate_issue_body()
