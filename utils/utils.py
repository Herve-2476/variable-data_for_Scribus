import os
import types
import shutil
import importlib.util

# from PIL import Image as ImagePIL
# from reportlab.pdfgen.canvas import Canvas


from utils import constants


def select_scribus_exe():
    # selection of the scribus executable
    scribus_exe = "scribus"  # ok for linux and mac os
    if os.name == "nt":  # windows:
        for scribus_path in constants.SCRIBUS_EXE:
            if os.path.isdir(scribus_path):
                scribus_exe = str(os.path.join(scribus_path, "scribus.exe"))
        if scribus_exe == "scribus":
            msg = "The path for the executable file of scribus is not"
            msg += f" in SCRIBUS_EXE={constants.SCRIBUS_EXE} in the default_settings.py file"
            raise Exception(msg)
    return scribus_exe


def app_settings_test():
    test_and_copy(
        "./unitary",
        "app_settings_init.py",
        constants.APP_SETTINGS_DIR,
        constants.APP_SETTINGS_NAME_FILE,
    )


def clean_console():
    clean_system_command = "cls" if os.name == "nt" else "clear"
    os.system(clean_system_command)


def test_and_copy(
    source_directory_name,
    source_file_name,
    target_directory_name,
    target_file_name,
):
    msg = f"test the presence of the file {target_file_name} "
    msg += f"in the directory {target_directory_name}\n"

    # print(msg)
    if not os.path.isfile(os.path.join(target_directory_name, target_file_name)):
        print(
            f"{constants.TAB}{target_file_name} is not in the directory : {target_directory_name}"
        )
        msg = f"{constants.TAB}copy of the file {target_file_name}"
        msg += f" in the directory : {target_directory_name}\n"
        print(msg)
        shutil.copy2(
            os.path.join(source_directory_name, source_file_name),
            os.path.join(target_directory_name, target_file_name),
        )
        return True
    else:
        print(
            f"{constants.TAB}{target_file_name} is in the directory : {target_directory_name}\n"
        )
        return False


def module_from_file(module):
    module_directory, module_name = module
    spec = importlib.util.spec_from_file_location(
        module_name, os.path.join(module_directory, module_name)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def display_pipe(nom_pipe, pipe):
    ch = ""
    if pipe.splitlines():
        ch += nom_pipe + "\n\n"
        for msg in pipe.splitlines():
            if msg:
                ch += f"{constants.TAB}" + f"{msg.decode('utf-8')}" + "\n"
    if ch != "":
        print(ch)
    return ch


def create_dir(working_directory, directory_name, directory):
    if directory == "":
        directory = os.path.join(working_directory, directory_name[:-4])
    if not os.path.isdir(directory):
        os.makedirs(directory)
        print(f"{constants.TAB}creation of the directory : {directory}")
    else:
        print(f"{constants.TAB}{directory} already exists")
    return directory.replace("\\", "/")


def compute_per_instance(number_of_files, number_of_instances):
    # compute per instance
    q = number_of_files // number_of_instances
    r = number_of_files % number_of_instances
    if r == 0:
        files_quantity_per_instance = [q] * number_of_instances
    else:
        files_quantity_per_instance = [q + 1] * r + [q] * (number_of_instances - r) * (
            q != 0
        )

    return files_quantity_per_instance


def slice_list(number_of_files, number_of_export_instances, slice):
    quantity_per_instance_list = compute_per_instance(
        number_of_files, number_of_export_instances
    )
    quantity_per_slice = []
    for quantity_per_instance in quantity_per_instance_list:
        quantity_per_slice += compute_per_slice(quantity_per_instance, slice)

    return sorted(quantity_per_slice, reverse=True)


def compute_per_slice(number_of_files, slice):
    # compute per instance
    q = number_of_files // slice
    r = number_of_files % slice
    files_quantity_per_slice = [slice] * q + [r] * (r != 0)

    return files_quantity_per_slice


def save_settings(data_settings, target_directory, target_file_name):
    data_list = []
    for key in data_settings.__dict__.keys():
        if key[:2] != "__" and key not in ["working_directory"]:
            if isinstance(data_settings.__dict__[key], str):
                data_list.append(f"{key} = r'{data_settings.__dict__[key]}'\n")
            else:
                data_list.append(f"{key} = {data_settings.__dict__[key]}\n")

    with open(
        os.path.join(target_directory, target_file_name),
        "w",
        encoding="utf-8",
    ) as file:
        file.writelines(data_list)


def test_and_create_directory(directory):
    # print(f"Test the presence of the directory {directory}\n")
    if not os.path.isdir(directory):
        # print(f"{constants.TAB}{directory} does not exist")
        # print(f"{constants.TAB}Creation of the directory {directory}\n")
        os.makedirs(directory)
        return True
    else:
        # print(f"{constants.TAB}{directory} already exist\n")
        return False


def test_and_create_file_from_file(
    source_directory,
    source_file_name,
    target_directory,
    target_file_name,
    variables_to_add={},
    args={},
    save=False,
):
    if save or not os.path.isfile(os.path.join(target_directory, target_file_name)):
        data_settings = module_from_file((source_directory, source_file_name))
        for key in variables_to_add:
            if key not in data_settings.__dict__ or key in args:
                data_settings.__dict__[key] = variables_to_add[key]

        save_settings(data_settings, target_directory, target_file_name)


def working_directory_test():
    app_settings = module_from_file(
        (constants.APP_SETTINGS_DIR, constants.APP_SETTINGS_NAME_FILE)
    )
    if "working_directory" in app_settings.__dict__.keys():
        return app_settings.__dict__["working_directory"]
    else:
        msg = "The variable working_directory is not "
        msg += f"defined in {constants.APP_SETTINGS_NAME_FILE}\n"
        raise Exception(msg)


class Settings:
    def __init__(self, modules_list):
        for module in [module_from_file(module) for module in modules_list]:
            for key in module.__dict__.keys():
                if key[:2] != "__" and not isinstance(
                    module.__dict__[key], types.ModuleType
                ):
                    self.__dict__[key] = module.__dict__[key]
