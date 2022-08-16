#!/usr/bin/env python3
"""
    Author: Hansol Choe
    https://github.com/HansolChoe/gcov-grabber
    A gcov wrapper which makes metadata of gcov files.
"""
import os
import subprocess
import pathlib
import argparse
import logging
import json
from contextlib import contextmanager

VULCAN_YML_GCOV_INCLUSION_LIST = os.getenv("VULCAN_YML_GCOV_INCLUSION_LIST", None)

logger = logging.getLogger(__name__)


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def parse_args():
    parser = argparse.ArgumentParser(description='gcovg: A gcov wrapper which makes metadata of gcov files.')
    parser.add_argument('-f',
                        '--file',
                        help='file patterns to run gcov. For example: (*.o)',
                        required=True,
                        action='append')
    parser.add_argument('-r',
                        '--root-dir',
                        help='root directory to run gcov',
                        default='.')
    parser.add_argument('-g',
                        '--gcov-path',
                        help='path to gcov',
                        required=False,
                        default='gcov')
    parser.add_argument('-o',
                        '--output',
                        help='output file',
                        required=False)
    parser.add_argument('--keep-gcov-files',
                        help='do not clean gcov files(recursively) before run gcov\
                              default: false',
                        action='store_true',
                        default=False)
    parser.add_argument('-e',
                        '--exclusion-list',
                        nargs='+',
                        help='files to exclude in regex patterns',
                        required=False,
                        default=[])
    parser.add_argument('-i',
                        '--inclusion-list',
                        nargs='+',
                        help='files to include in regex patterns',
                        required=False,
                        default=[])
    return parser.parse_args()


def main():
    args = parse_args()
    gcov = args.gcov_path
    root_dir = pathlib.Path(args.root_dir)

    if not pathlib.Path(root_dir).is_dir():
        logger.critical(f'{root_dir} is not a directory')
        exit(1)

    # clean all gcov files if keep_gcov_files flag is not set
    if not args.keep_gcov_files:
        for gcov_file in root_dir.rglob('*.gcov'):
            pathlib.Path(gcov_file).unlink()

    source_dir_list = root_dir.rglob('*.c')
    source_parent_set = set()
    source_str_list = list()
    for path in source_dir_list:
        source_parent_set.add(pathlib.Path(path).parent)
        source_str_list = str(path)

    print(source_str_list)
    exclusion_list = []

    for exclusion_pattern in args.exclusion_list:
        for e in root_dir.rglob(exclusion_pattern):
            exclusion_list.append(e)
    print(f'exclusion_list = {exclusion_list}')

    inclusion_list = []
    # print("Include coverage: " + VULCAN_YML_GCOV_INCLUSION_LIST)
    for e in root_dir.rglob(VULCAN_YML_GCOV_INCLUSION_LIST):  #TODO: It treat only one element for now, have to make it as a list.
        inclusion_list.append(e)
    # print(f'inclusion_list = {inclusion_list}')

    # glob all file's list
    target_file_list = []
    if len(inclusion_list) != 0:
        # print(inclusion_list)
        for file in args.file:
            for p in root_dir.rglob(file):
                if p in inclusion_list:
                    target_file_list.append(p)
    else:
        for file in args.file:
            for p in root_dir.rglob(file):
                if p not in exclusion_list:
                    target_file_list.append(p)
    # print(f'target_file_list = {target_file_list}')
    # run gcov and make metadata
    # for target_file in target_file_list:
    for target_file in target_file_list:
        target_src = ''
        for target_source_file in source_str_list:
            if str(target_file).split("/")[-1].replace(".o", ".c") in target_source_file:
                target_src = target_source_file
                print(f'Target src: {str(target_file)}')
        with cwd(str(pathlib.Path(target_src).parent)):
            print(str(pathlib.Path(target_file).parent))
            print([args.gcov_path, str(target_file)])
            gcov_proc = subprocess.Popen([args.gcov_path, str(target_file.name)],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         stdin=subprocess.PIPE)
            out, err = gcov_proc.communicate()

    gcov_info_dict = dict()
    # for parent_dir in {f.parent for f in target_file_list}:
    for parent_dir in {f.parent for f in source_dir_list}:
        for gcov_file_path in pathlib.Path(parent_dir).glob("*.gcov"):
            with open(gcov_file_path, encoding='utf-8') as gcov_file:
                gcov_source_name = gcov_file.readline().rstrip().split(':', 3)[-1]
                if pathlib.Path(gcov_source_name).is_absolute():
                    gcov_info_dict[gcov_file_path.name] = str(gcov_source_name)
                else:
                    gcov_info_dict[gcov_file_path.name] = str((parent_dir / gcov_source_name))
    gcov_info_json = json.dumps(gcov_info_dict, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(gcov_info_json)
    else:
        print(gcov_info_json)


if __name__ == '__main__':
    main()
