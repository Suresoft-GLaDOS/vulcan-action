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
    for patch in patch_list:
        print("Postprocessing this: " + patch)
        os.system(f"sed -i 's/((void *)0)/NULL/g' {patch}")


post_processing()
