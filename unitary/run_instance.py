import os
import sys
from utils import module_from_file


def run():
    working_directory = sys.argv[5]
    module_from_file("generator", os.path.join(working_directory, "generator.py"))


if __name__ == "__main__":
    run()
