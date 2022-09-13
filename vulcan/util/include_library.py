import os
import subprocess
import pathlib
import argparse
import logging
import json
import glob
import sys

VULCAN_OUTPUT_DIR = os.getenv("VULCAN_OUTPUT_DIR")
VULCAN_TARGET = os.getenv("VULCAN_TARGET")
VULCAN_YML_TEST_BUILD_COMMAND = os.getenv('VULCAN_YML_TEST_BUILD_COMMAND')


def include_libraries(library_list):
    config_file_autogen = glob.glob(VULCAN_TARGET + '/*.patch')
    build_command_list = VULCAN_YML_TEST_BUILD_COMMAND.splitlines()
    for command in build_command_list:
        if 'autogen.sh' in command:
            autogen_lines = list()
            with open(VULCAN_TARGET + '/autogen.sh') as autogen_file:
                
                print(autogen_file.readline(), end="")


if __name__ == '__main__':
    include_libraries(sys.args[1])
