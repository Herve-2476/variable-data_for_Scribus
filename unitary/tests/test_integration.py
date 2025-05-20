import subprocess
import os
import shutil
import sys

sys.path.insert(0, os.path.abspath("."))
from utils import constants  # noqa
from utils.utils import module_from_file  # noqa


def init_run(test_number):

    shutil.copy2(
        f"./unitary/tests/app_settings_{test_number}.py",
        os.path.join(constants.APP_SETTINGS_DIR, constants.APP_SETTINGS_NAME_FILE),
    )

    subprocess.Popen(
        [sys.executable, "run_unitary.py"],
    ).wait()
    os.remove(
        os.path.join(constants.APP_SETTINGS_DIR, constants.APP_SETTINGS_NAME_FILE)
    )


def test_directories():
    init_run(1)
    directories_to_test = [
        r"./rv_test_2/SLA_IN",
        r"./rv_test_2/test_2/SLA",
        r"./rv_test_3/test_2/PDF",
        r"./rv_test_1/PNG",
    ]
    for directory in directories_to_test:
        assert os.path.isdir(directory)
    assert os.path.isfile(os.path.join(r"./rv_test_1/test_1", "settings_unitary.py"))
    assert os.path.isfile(os.path.join(r"./rv_test_1/test_1", "generator.py"))

    settings = module_from_file(("./rv_test_1/test_1", "settings_unitary.py"))
    assert "working_directory" not in settings.__dict__
    assert settings.create_png
    assert not settings.delete_sla
    assert settings.sla_in_dir == r"./rv_test_2/SLA_IN"
    assert settings.sla_created_dir == r"./rv_test_2/test_2/SLA"
    assert settings.pdf_created_dir == r"./rv_test_3/test_2/PDF"
    assert settings.png_created_dir == r"./rv_test_1/PNG"

    for directory in ["rv_test_1", "rv_test_2", "rv_test_3"]:
        shutil.rmtree(directory)


def test_hello_world():

    directories_to_test = [
        ("./unitary/tests/pdf_created", ".pdf"),
        ("./unitary/tests/hello_world/sla_created", ".sla"),
        ("./unitary/tests/hello_world/png_created", ".png"),
    ]
    for directory, ext in directories_to_test:
        if os.path.isdir(directory):
            shutil.rmtree(directory)

    if os.path.isdir("./unitary/tests/hello_world/imposition"):
        shutil.rmtree("./unitary/tests/hello_world/imposition")

    init_run(2)
    for directory, ext in directories_to_test:
        list_dir = sorted(os.listdir(directory))
        assert len(list_dir) == 5
        for i in range(5):
            assert list_dir[i] == f"{i+5}{ext}"
        shutil.rmtree(directory)

    assert os.path.isfile("./unitary/tests/hello_world/imposition/hello_world_1_1.pdf")


def compare_files(file_1, file_2):
    ignore_start = []  # for compare pdf but too much exceptions with two os
    with open(file_1, "rb") as file_1:
        with open(file_2, "rb") as file_2:
            line_1 = True
            while line_1:
                line_1 = file_1.readline()
                line_2 = file_2.readline()
                if line_1 != line_2:
                    test = False
                    for start in ignore_start:
                        if line_1.startswith((start)):
                            test = True
                            break
                    if not test:
                        print("file 1", line_1)
                        print("file 2", line_2)
                        return False
    return True


def test_created_files():
    init_run(3)
    for directory, ext in [
        ("./unitary/tests/hello_world_1/sla_created", ".sla"),
    ]:
        for i in range(5, 7):
            assert compare_files(
                directory + f"/{i}{ext}", directory + f"_compare/{i}{ext}"
            )
