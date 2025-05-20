import os
import importlib.util

try:
    from . import cts
    from . import default_settings
except ImportError:
    import cts
    import default_settings


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def compute_per_slice(number_of_files, slice):
    # compute per instance
    q = number_of_files // slice
    r = number_of_files % slice
    files_quantity_per_slice = [slice] * q + [r] * (r != 0)

    return files_quantity_per_slice


def display_pipe(nom_pipe, pipe):
    ch = ""
    if pipe.splitlines():
        ch += nom_pipe + "\n\n"
        for msg in pipe.splitlines():
            if msg:
                ch += f"{cts.TAB}" + f"{msg}"[2:] + "\n"
    print(ch)


def slice_list(number_of_files, number_of_export_instances, slice):
    quantity_per_instance_list = compute_per_instance(
        number_of_files, number_of_export_instances
    )
    quantity_per_slice = []
    for quantity_per_instance in quantity_per_instance_list:
        quantity_per_slice += compute_per_slice(quantity_per_instance, slice)

    return sorted(quantity_per_slice, reverse=True)


class data_settings:

    """retrieve the data from the default_settings file in utils and then from the
    app_setting.py file in the root and then from the settings.py
     in the working directory (the latter crush the previous"""

    def __init__(self, new_project=False):

        app_settings = module_from_file(
            cts.APP_SETTINGS_NAME_FILE,
            os.path.join(cts.ROOT_DIRECTORY, cts.APP_SETTINGS_NAME_FILE),
        )

        # add absolute path to the dictionnary (to retrieve after the value)
        for directory in cts.DIRECTORIES_TO_CREATE + ["working_directory"]:
            default_settings.__dict__[directory] = ""

        # retrieve the value from default_settings.py and
        # app_setting.py (the latter crush the former)
        for key in default_settings.__dict__:
            if key[:2] != "__":
                self.__dict__[key] = app_settings.__dict__.get(
                    key, default_settings.__dict__[key]
                )
        # retrieve the value from data_settings and settings.py (the latter crush the former)
        if not new_project:

            settings = module_from_file(
                cts.SETTINGS_NAME_FILE,
                os.path.join(self.working_directory, cts.SETTINGS_NAME_FILE),
            )
            for key in self.__dict__:
                if key[:2] != "__":
                    self.__dict__[key] = settings.__dict__.get(key, self.__dict__[key])

        # True can not be an argument for subprocess.Popen
        for key in ["delete_sla", "create_pdf", "create_png"]:
            self.__dict__[key] = "True" if self.__dict__[key] else ""

        # initialization of the working directories
        for directory in cts.DIRECTORIES_TO_CREATE:

            if not self.__dict__[directory]:
                self.__dict__[directory] = os.path.abspath(
                    os.path.join(self.working_directory, directory[:-4])
                )
