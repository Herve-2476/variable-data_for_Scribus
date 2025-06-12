import sys  # mandatory
import os  # mandatory
import random


sys.path.insert(0, sys.argv[6])  # mandatory
sys.path.insert(0, os.path.abspath(os.path.join(sys.argv[6], "..")))  # mandatory
from sla_object import SLA  # noqa mandatory


sla = SLA(sys.argv)  # mandatory

# ///////////////\\\\\\\\\\\\\\
# write here the code that should not be repeated at each file creation
# sla.display_sla_colors()
# sla.display_named_sla_objects()
colors = [
    "Blue",
    "Cyan",
    "Green",
    "Magenta",
    "Red",
    "Yellow",
    "black",
]
# \\\\\\\\\\\\\\\//////////////

for file_number in range(
    sla.first_number, sla.first_number + sla.number_of_files
):  # mandatory
    sla.init_root()  # mandatory

    # //////////////\\\\\\\\\\\\\
    # put here the objects you want on your files with their variable attributes
    sla.place("Document-1_sky")
    sla.place(f"Document-{file_number % 6+1}_text")
    sla.place(f"Document-{file_number % 6+1}_stars")
    # sla.place("Document-1_number", ITEXT=[{"CH": f"N° {file_number:04}"}])
    random.shuffle(colors)
    i = 0
    for obj in sla.objects["Document-1_earth"]:
        sla.place(
            obj,
            CSTOP=[
                {"NAME": colors[i % len(colors)]},
                {"NAME": colors[(i + 1) % len(colors)]},
            ],
        )
        i += 2
    sla.place("Document-1_cut")
    # \\\\\\\\\\\\\\/////////////

    sla.sla_creation(file_number)  # mandatory
sla.sla_end_creation()  # mandatory
