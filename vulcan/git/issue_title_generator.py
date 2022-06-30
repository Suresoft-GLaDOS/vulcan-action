import os

VULCAN_OUTPUT_DIR = os.getenv("VULCAN_OUTPUT_DIR")


def collect_failed_test_command():
    print(f"[DEBUG] collect failed test command", flush=True)
    gcov_dir = os.path.join(VULCAN_OUTPUT_DIR, "gcov")
    with open(os.path.join(VULCAN_OUTPUT_DIR, "failed.command"), "a") as failed:
        for g in os.listdir(gcov_dir):
            with open(os.path.join(gcov_dir, g, "result.test")) as result:
                test_result = result.read()
            with open(os.path.join(gcov_dir, g, "test.command")) as command:
                test_command = command.read()
            if test_result == "failed":
                failed.write(test_command.strip() + "\n")


def generate_issue_title():
    '''
    issue: Failed test(s) {test command} etc.
    pr:    Fixed test(s) {test command} etc. (#)
    '''
    print(f"[DEBUG] create issue title", flush=True)
    with open(os.path.join(VULCAN_OUTPUT_DIR, "failed.command")) as f:
        failed_cmds = f.readlines()
    with open(os.path.join(VULCAN_OUTPUT_DIR, "issue_title"), "w") as f:
        len_failed_cmds = len(failed_cmds)
        if len_failed_cmds > 1:
            issue_title = f"Failed tests {failed_cmds[0]} etc."
        elif len_failed_cmds == 1:
            issue_title = f"Failed test {failed_cmds[0]}"
        else: # Should not happned
            issue_title = f"[CRITICAL] No failed test"
        f.write(issue_title)


collect_failed_test_command()
generate_issue_title()
