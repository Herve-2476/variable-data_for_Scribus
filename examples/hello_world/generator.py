import sys  # mandatory
import os  # mandatory
import random


sys.path.insert(0, sys.argv[6])  # mandatory
sys.path.insert(0, os.path.abspath(os.path.join(sys.argv[6], "..")))  # mandatory
from sla_object import SLA  # noqa mandatory


sla = SLA(sys.argv)  # mandatory

# ///////////////\\\\\\\\\\\\\\
# write here the code that should not be repeated at each file creation
sla.display_named_sla_objects()
sla.display_sla_colors()
colors = ["Magenta", "Cyan", "Red", "Yellow"]

# \\\\\\\\\\\\\\\//////////////

for file_number in range(
    sla.first_number, sla.first_number + sla.number_of_files
):  # mandatory
    sla.init_root()  # mandatory

    # //////////////\\\\\\\\\\\\\
    # put here the objects you want on your files with their variable attributes

    sla.place(
        "hello_world",
        ITEXT=[
            {
                "CH": f"Hello World {file_number:04} !!!",
                "FCOLOR": random.choice(colors),
            },
        ],
    )
    sla.place("cut")

    # \\\\\\\\\\\\\\/////////////

    sla.sla_creation(file_number)  # mandatory
sla.sla_end_creation()  # mandatory
