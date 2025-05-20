import copy
import datetime
import math
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import collections
import pickle
import cts
from utils.utils import slice_list, select_scribus_exe


# https://www.datacamp.com/tutorial/python-xml-elementtree


class SLA:
    """This class parse the sla files"""

    def __init__(self, argv):

        (
            self.first_number,
            self.number_of_files,
            self.sla_instance_number,
            self.number_of_export_instances,
        ) = (
            int(argv[1]),
            int(argv[2]),
            int(argv[3]),
            int(argv[4]),
        )

        with open("./temp/data_sla", "rb") as file:
            self.settings = pickle.load(file)

        self.objects = {}
        self.middle_of_objects = {}
        self.Coordinates = collections.namedtuple("Coordinates", "XPOS YPOS")
        self.colors_set = set()
        self.withoutname_index = 1
        files_list = sorted(os.listdir(self.settings["sla_in_dir"]))
        files_list = [
            sla_file
            for sla_file in files_list
            if os.path.splitext(sla_file)[1] == ".sla"
        ]
        if not files_list:
            raise Exception(
                f"There is no sla files to treat in the directory {self.settings['sla_in_dir']}"
            )

        for i, sla_file in enumerate(files_list):
            if os.path.splitext(sla_file)[1] == ".sla":

                sla_file = os.path.join(self.settings["sla_in_dir"], sla_file)
                tree = ET.parse(sla_file)
                root = tree.getroot()
                if i == 0:
                    msg = f"\n\nthe header of {os.path.basename(sla_file)} is selected"
                    msg += " for the construction of all the sla files"
                    print(msg)

                    self.x_offset = float(root[0].find("PAGE").attrib["PAGEXPOS"])
                    self.y_offset = float(root[0].find("PAGE").attrib["PAGEYPOS"])
                    self.width = float(root[0].find("PAGE").attrib["PAGEWIDTH"])
                    self.height = float(root[0].find("PAGE").attrib["PAGEHEIGHT"])

                self.retrieve_all_objects(root, sla_file, len(files_list))
                self.creation_empty_root(root)

        self.start = datetime.datetime.today()

    def init_root(self):
        self.root = copy.deepcopy(self.empty_root)

    def sla_creation(self, n):
        tree = ET.ElementTree(self.root)
        tree.write(
            os.path.join(self.settings["sla_created_dir"], str(n) + ".sla"),
            encoding="UTF-8",
            xml_declaration=True,
        )

    def sla_end_creation(self):
        self.end = datetime.datetime.today()
        msg = f"creation of {self.number_of_files} sla files"
        msg += f" in {self.end-self.start} (hours,minutes,seconds)"
        print(msg)

        self.export()

    def export(self):
        # tempory directory creation
        temp_dir_list = []
        for instance_export in range(self.number_of_export_instances):
            temp_dir_list.append(
                os.path.join(
                    self.settings["sla_created_dir"],
                    f"temp{self.sla_instance_number}_{instance_export}",
                )
            )
            os.makedirs(temp_dir_list[-1], exist_ok=True)

        scribus_exe = select_scribus_exe()

        # compute per instance
        start = datetime.datetime.today()

        quantity_per_slice_list = slice_list(
            self.number_of_files,
            self.number_of_export_instances,
            cts.SCRIBUS_ITERATION_MAX,
        )

        first_number = self.first_number

        # launching of instances
        processus = []
        for index in range(
            0,
            len(quantity_per_slice_list),
            self.number_of_export_instances,
        ):
            sub_slice = quantity_per_slice_list[
                index : index + self.number_of_export_instances  # noqa: E203
            ]

            for i, files_quantity_per_export_instance in enumerate(sub_slice):
                processus.append(
                    subprocess.Popen(
                        [
                            scribus_exe,
                            "-g",
                            "-py",
                            "./unitary/unitary_scribus.py",
                            "--python-arg",
                            str(first_number),
                            str(files_quantity_per_export_instance),
                            "True" if self.settings["delete_sla"] else "",
                            "True" if self.settings["create_pdf"] else "",
                            "True" if self.settings["create_png"] else "",
                            temp_dir_list[i],
                            self.settings["sla_created_dir"],
                            self.settings["pdf_created_dir"],
                            self.settings["png_created_dir"],
                        ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                )
                first_number += files_quantity_per_export_instance

            for i, process in enumerate(processus):
                process.wait()
                process.stdout.read()  # to empty
                process.stderr.read()  # to empty

        if not self.settings["delete_sla"]:
            for temp_dir in temp_dir_list:
                shutil.rmtree(temp_dir)
        end = datetime.datetime.today()
        print(f"exported in {end-start} (hours,minutes,seconds)")

    def return_name_object(self, object):
        object_name = object
        if isinstance(object, ET.Element):
            object_name = object_name.get("ANNAME")

        if object_name not in self.objects:
            raise Exception(
                f"The object {object_name} does not exist in your source files"
            )

        return object_name

    def place(self, object, **args):
        object_name_init = self.return_name_object(object)
        object_name = "new_object"
        self.objects[object_name] = copy.deepcopy(self.objects[object_name_init])

        path = False
        if "WIDTH" in args or "HEIGHT" in args:
            path = True
        for key in ("ROT", "WIDTH", "HEIGHT"):
            if key in args:  # we must update before the process of XPOS and YPOS
                self.objects[object_name].set(key, str(args[key]))
                args.pop(key)

        # if width and/or height are modify ve have to modify the attribute path
        if path:
            H, L = self.get(object_name, "HEIGHT"), self.get(object_name, "WIDTH")
            self.objects[object_name].set(
                "path", "M0 0 L" + L + " 0 L" + L + " " + H + " L0 " + H + " L0 0 Z"
            )

        # we always proceed XPOS and YPOS
        for key in ["XPOS", "YPOS"]:
            args[key] = args.get(
                key, getattr(self.middle_of_objects[object_name_init], key)
            )
        for key, value in zip(
            ["XPOS", "YPOS"],
            self.workspace_coordinates(
                object_name, (float(args["XPOS"]), float(args["YPOS"]))
            ),
        ):
            self.objects[object_name].set(key, str(value))
            args.pop(key)

        for key, value in args.items():
            if isinstance(value, list):
                for dictionnary, obj in zip(
                    value, list(self.objects[object_name].iter(key))
                ):
                    for key, value in dictionnary.items():
                        obj.set(key, str(value))

            else:  # we presume that it is not text
                self.objects[object_name].set(key, str(value))

        self.root[0].append(self.objects[object_name])

    def workspace_coordinates(self, object_name, coordinates):
        """in = coordinates of the middle in user system
        out = coordinates of the top left corner in scribus system"""
        h, l, alpha = (
            float(self.get(object_name, "HEIGHT")),
            float(self.get(object_name, "WIDTH")),
            float(self.get(object_name, "ROT")),
        )
        x_middle, y_middle = self.middle(h, l, alpha)
        return (
            coordinates[0] + self.x_offset - x_middle,
            coordinates[1] + self.y_offset - y_middle,
        )

    def inv_workspace_coordinates(self, object_name, key, value):
        """in = coordinates of the top left corner in scribus system
        out = coordinates of the middle in user system"""
        h, l, alpha = (
            float(self.get(object_name, "HEIGHT")),
            float(self.get(object_name, "WIDTH")),
            float(self.get(object_name, "ROT")),
        )
        x_middle, y_middle = self.middle(h, l, alpha)
        if key == "XPOS":
            return value - self.x_offset + x_middle
        elif key == "YPOS":
            return value - self.y_offset + y_middle

    def middle(self, H, L, alpha):
        d = ((H**2 + L**2) / 4) ** 0.5
        teta = math.acos(L / 2 / d) + alpha * math.pi / 180
        x_middle = d * math.cos(teta)
        y_middle = d * math.sin(teta)
        return x_middle, y_middle

    def retrieve_all_objects(self, root, sla_file, files_number):
        sla_file_name = ""
        begin_index = 1
        if files_number > 1:
            sla_file_name = os.path.basename(sla_file)[: -len(".sla")]
            begin_index = 0
        # retrieve all the objects,named them (if not) and save them in a dictionnary
        for child in root.iter("PAGEOBJECT"):
            try:
                name = cts.NAME_SEPARATOR.join((sla_file_name, child.attrib["ANNAME"]))[
                    begin_index:
                ]
            except KeyError:
                name = cts.NAME_SEPARATOR.join(
                    (
                        sla_file_name,
                        cts.WITHOUTNAME_NAME,
                        str(self.withoutname_index),
                    )
                )[begin_index:]
                self.withoutname_index += 1
            child.set("ANNAME", name)
            self.objects[name] = child
            # recording of the middle of the object
            XPOS = self.inv_workspace_coordinates(
                name, "XPOS", float(self.get(name, "XPOS"))
            )
            YPOS = self.inv_workspace_coordinates(
                name, "YPOS", float(self.get(name, "YPOS"))
            )
            self.middle_of_objects[name] = self.Coordinates(*(XPOS, YPOS))

    def creation_empty_root(self, root):
        # creation of the empty root (that is to say without any objects)
        for child in root.findall(
            "./DOCUMENT/PAGEOBJECT"
        ):  # retrieve the objects of the first levels
            try:
                root[0].remove(child)
            except ValueError:
                pass
            self.empty_root = root

    def display_sla_colors(self):
        msg = "\nColors find in your sla file (the one selected for"
        msg += " the construction of all the sla files)\n"
        print(msg)
        colors_list = []
        for color in self.empty_root.findall("./DOCUMENT/COLOR"):
            colors_list.append(color.attrib["NAME"])
        print(colors_list)

    def get(self, object, attribute, default=0):
        object_name = self.return_name_object(object)
        value = self.objects[object_name].get(attribute)
        if value:
            return value
        else:
            return default

    def display_named_sla_objects(self):
        print("\nObjects find in your(s) sla files\n")
        for name_object in self.objects:
            if cts.WITHOUTNAME_NAME not in name_object:
                print(" - " + name_object)
        print()
