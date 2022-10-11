import os
import subprocess
import pathlib
import argparse
import logging
import json
import glob


VULCAN_OUTPUT_DIR = os.getenv("VULCAN_OUTPUT_DIR")


def post_processing():
    patch_dir = os.path.join(VULCAN_OUTPUT_DIR, "patch")
    patch_list = glob.glob(patch_dir+"/*.patch")
    # patch_list = ['1.patch']

    for patch in patch_list:
        print("Postprocessing this: " + patch)

        patch_lines = []
        post_patch_lines = []

        with open(patch, 'r') as file_data:
            # print(file_data.readline(), end="")
            patch_lines = file_data.readlines()

        total_count = 0
        added_count = 0
        deleted_count = 0
        first = True
        plus = False
        minus = False
        in_the_block = False
        fix = 0

        for i, line in enumerate(patch_lines):
            if first or in_the_block:
                post_patch_lines.append(line)
                total_count = total_count + 1
                print(line)
            if line.startswith('---') or line.startswith('+++'):
                continue
            if first:
                in_the_block = True
                if line.startswith('-'):
                    minus = True
                    first = False
                elif line.startswith('+'):
                    plus = True
                    first = False

            if line.startswith('-') and minus:
                deleted_count = deleted_count + 1
                continue
            elif line.startswith('+') and plus:
                added_count = added_count + 1
                continue
            elif line.startswith('+') and minus:
                added_count = added_count + 1
                continue
            elif not first:
                break
                in_the_block = False

        for i, line in enumerate(post_patch_lines):
            if line.startswith('@@'):
                parse_line = line.split(' ')
                new_word = []
                for j, word in enumerate(parse_line):
                    if word.startswith('-'):
                        parse_word = word.split(',')
                        parse_word[1] = str(total_count - 3 - added_count)
                        word = ','.join(parse_word)
                        print(added_count)
                        print(word)
                        parse_line[j] = word
                    elif word.startswith('+'):
                        parse_word = word.split(',')
                        parse_word[1] = str(total_count - 3 - deleted_count)
                        word = ','.join(parse_word)
                        print(deleted_count)
                        print(word)
                        parse_line[j] = word
                    new_word.append(word)
                print(new_word)
                new_line = ' '.join(new_word)
                print(new_line)
                post_patch_lines[i] = new_line

        with open(f'{patch}_post.patch', 'w') as file_data:
            # print(file_data.readline(), end="")
            file_data.writelines(post_patch_lines)

        print(f"sed -i 's/((void \\*)0)/NULL/g' {patch}")
        os.system(f"sed -i 's/((void \\*)0)/NULL/g' {patch}")


post_processing()

