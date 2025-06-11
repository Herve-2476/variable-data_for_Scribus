import os
import types
import shutil
import importlib.util
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
import time
import sys

# from PIL import Image as ImagePIL
# from reportlab.pdfgen.canvas import Canvas


from utils import constants


def write_pid(dir):
    pid = str(os.getpid())
    with open(os.path.join(dir, pid), "w") as f:
        f.write("")
    return pid


def delete_pid(dir, pid):
    os.remove(os.path.join(dir, pid))


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


def test_copy_file_without_attribute(
    source_directory_name,
    source_file_name,
    target_directory_name,
    target_file_name,
    attribute_to_delete,
):
    if not os.path.isfile(os.path.join(target_directory_name, target_file_name)):
        with open(
            os.path.join(source_directory_name, source_file_name),
            "r",
        ) as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if line.startswith(attribute_to_delete):
                break
        lines.pop(i)
        with open(os.path.join(target_directory_name, target_file_name), "w") as file:
            file.writelines(lines)
        print(f"{constants.TAB}Creation of the file {target_file_name}")

    else:
        print(f"{constants.TAB}{target_file_name} already exist")


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
                ch += f"{constants.TAB}" + f"{msg}"[2:-1] + "\n"
    if ch != "":
        print(ch)
    return ch


def clean_directory(dir):
    for file in os.listdir(dir):
        os.remove(os.path.join(dir, file))


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


def retrieve_data(directory, file_name, save=False):
    """read the file and create a dictionnary with the name of
    the object for the key and lines of code for the value.
    Save is requested to save the file without the variable objects"""
    with open(os.path.join(directory, file_name), "r", encoding="utf-8") as file:
        lines = file.readlines()
    new_lines = []
    objects_dict = {}
    i = 0
    while i < len(lines):
        if lines[i].startswith("__"):
            name_obj = lines[i].split("=")[0].rstrip()[2:]
            objects_dict[name_obj] = [lines[i][2:]]
            i += 1
            while i < len(lines) and not lines[i].startswith("__"):
                objects_dict[name_obj].append(lines[i])
                i += 1
        else:
            new_lines.append(lines[i] + "\n")
            i += 1
    if save:
        with open(f"./temp/{file_name}", "w", encoding="utf-8") as file:
            file.writelines(new_lines)
    return objects_dict


def retrieve_file_dimensions(file_for_dimensions):
    pdf = PdfReader(file_for_dimensions)
    page = pagexobj(pdf.pages[0])

    file_width, file_height = (page.BBox[2] - page.BBox[0]) / constants.R, (
        page.BBox[3] - page.BBox[1]
    ) / constants.R

    return file_width, file_height


def retrieve_image_dimensions(path, resolution):
    im = ImagePIL.open(path)
    w, h = im.size  # en pixels (pas ceux d'un pdf=72/inch)
    return w / resolution * 25.4, h / resolution * 25.4


def image_to_pdf(path, new_path, resolution):
    im = ImagePIL.open(path)
    w, h = im.size  # en pixels (pas ceux d'un pdf=72/inch)
    w, h = w / resolution * 72, h / resolution * 72
    can = Canvas(new_path)
    can.setPageSize((w, h))
    can.drawInlineImage(im, 0, 0, w, h)
    can.save()


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


def retrieve_working_directory(file):
    with open(file, "r") as f:
        return f.read().split("=")[-1]


class Settings:
    def __init__(self, modules_list):
        for module in [module_from_file(module) for module in modules_list]:
            for key in module.__dict__.keys():
                if key[:2] != "__" and not isinstance(
                    module.__dict__[key], types.ModuleType
                ):
                    self.__dict__[key] = module.__dict__[key]


DIRS = [
    "VariableDataPrinting",
    "Variable_Data_Printing_server",
    "Variable_Data_Printing_Front_End",
    "Variable_Data_Printing_API_Rest",
]


def update_packages():
    try:
        shutil.copy2(
            "./modified_modules/__init__.py",
            "./venv/Lib/site-packages/reportlab/graphics/barcode/__init__.py",
        )
        shutil.copy2(
            "./modified_modules/ecc200datamatrix.py",
            "./venv/Lib/site-packages/reportlab/graphics/barcode/ecc200datamatrix.py",
        )
    except:  # noqa
        python = sys.version_info
        python = ".".join([str(python.major), str(python.minor)])
        shutil.copy2(
            "modified_modules/__init__.py",
            f"./venv/lib/python{python}/site-packages/reportlab/graphics/barcode/__init__.py",
        )
        shutil.copy2(
            "./modified_modules/ecc200datamatrix.py",
            f"./venv/lib/python{python}/site-packages/reportlab/graphics/barcode/ecc200datamatrix.py",
        )
