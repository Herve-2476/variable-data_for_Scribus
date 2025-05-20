import os
import sys
import shutil
import subprocess
import datetime
import pickle
import copy
from utils.utils import (
    clean_console,
    working_directory_test,
    test_and_create_directory,
    display_pipe,
    Settings,
    create_dir,
    compute_per_instance,
    app_settings_test,
    test_and_create_file_from_file,
)
from utils import constants


class Unitary:
    def __init__(self, argv):
        self.argv = argv
        # clean console
        clean_console()
        # test the presence of app_settings.py
        # if not present, copy of unitary/app_settings_init.py
        app_settings_test()
        # retrieve working_directory in app_settings.py
        working_directory = working_directory_test()
        new_project = test_and_create_directory(working_directory)
        if new_project or not os.path.isfile(
            os.path.join(working_directory, "settings_unitary.py")
        ):
            settings = Settings(
                (
                    (
                        "./unitary",
                        "default_settings.py",
                    ),
                    (
                        constants.APP_SETTINGS_DIR,
                        constants.APP_SETTINGS_NAME_FILE,
                    ),
                )
            )
            settings = self.init_project(working_directory, settings)
            test_and_create_file_from_file(
                constants.APP_SETTINGS_DIR,
                constants.APP_SETTINGS_NAME_FILE,
                working_directory,
                "settings_unitary.py",
                settings.args_added,
                settings.args,
            )
        else:
            settings = Settings(
                (
                    (
                        "./unitary",
                        "default_settings.py",
                    ),
                    (
                        working_directory,
                        "settings_unitary.py",
                    ),
                )
            )
            settings = self.init_project(working_directory, settings)
            test_and_create_file_from_file(
                working_directory,
                "settings_unitary.py",
                working_directory,
                "settings_unitary.py",
                settings.args_added,
                settings.args,
                True,
            )

        msg = f"Creation of {settings.number_of_files} files, "
        msg += f"with {settings.number_of_sla_instances}"
        msg += f" sla instance(s) and {settings.number_of_export_instances}"
        msg += " export instance(s) per sla instance\n"
        print(msg)

        start = datetime.datetime.today()

        self.launching_python_instances(working_directory, settings)
        end = datetime.datetime.today()
        msg = f"Creation of {settings.number_of_files} file(s) "
        msg += f"in {end-start} (hours,minutes,seconds)\n"
        print(msg)

    def launching_python_instances(self, working_directory, settings):

        files_quantity_per_instance_sla_list = compute_per_instance(
            settings.number_of_files,
            settings.number_of_sla_instances,
        )

        first_number = settings.first_number
        data = copy.deepcopy(settings.__dict__)
        with open("./temp/data_sla", "wb") as file:
            pickle.dump(data, file)
        processus = []
        for instance_number, files_quantity_per_sla_instance in enumerate(
            files_quantity_per_instance_sla_list
        ):

            processus.append(
                subprocess.Popen(
                    [
                        sys.executable,
                        os.path.join(working_directory, "generator.py"),
                        str(first_number),
                        str(files_quantity_per_sla_instance),
                        str(instance_number),
                        str(settings.number_of_export_instances),
                        working_directory,
                        os.path.dirname(__file__),
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            )
            first_number += files_quantity_per_sla_instance

        for i, process in enumerate(processus):
            process.wait()
            display_pipe(
                "standard output of the python instance %s" % str(i + 1),
                process.stdout.read(),
            )
            display_pipe(
                "errors of the python instance %s" % str(i + 1), process.stderr.read()
            )

        # tempory directory deletion
        if settings.delete_sla:
            shutil.rmtree(settings.sla_created_dir)
        os.remove("./temp/data_sla")

    def init_project(self, working_directory, settings):
        args = self.retrieve_args(self.argv)
        for arg in args:
            settings.__dict__[arg] = args[arg]

        print(f"Initialization of the project in the directory : {working_directory}\n")
        for directory in ["sla_in_dir", "sla_created_dir"]:
            settings.__dict__[directory] = create_dir(
                working_directory, directory, settings.__dict__[directory]
            )

        for directory in ["png_created_dir", "pdf_created_dir"]:
            if settings.__dict__[f"create_{directory[:3]}"]:
                settings.__dict__[directory] = create_dir(
                    working_directory, directory, settings.__dict__[directory]
                )
        source_file = "./unitary/generator_init.py"
        target_file = os.path.join(working_directory, "generator.py")
        if not os.path.isfile(target_file):
            shutil.copy2(source_file, target_file)
            msg = f"{constants.TAB}copy the file generator.py"
            msg += f" in the directory {working_directory}"
            print(msg)

        settings.args_added = {
            "number_of_files": settings.number_of_files,
            "pdf_created_dir": settings.pdf_created_dir,
            "first_number": settings.first_number,
            "number_of_sla_instances": settings.number_of_sla_instances,
            "number_of_export_instances": settings.number_of_export_instances,
        }
        print()
        settings.args = args
        return settings

    def retrieve_args(self, argv):
        args = {}
        if len(argv) > 1:
            try:
                args["number_of_files"] = int(argv[1])
            except ValueError:
                raise Exception(
                    "the first argument is the number of files and must be an integer"
                )
        if len(argv) > 2:
            try:
                args["number_of_sla_instances"] = int(argv[2])
            except ValueError:
                raise Exception(
                    "the second argument is the number of python instances to create sla files\
                         and must be an integer"
                )
        if len(argv) > 3:
            try:
                args["number_of_export_instances"] = int(argv[3])
            except ValueError:
                raise Exception(
                    "the third argument is the number of scribus instances per python instance\
                         and must be an integer"
                )
        return args
