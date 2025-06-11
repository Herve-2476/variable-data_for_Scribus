import sys  # mandatory
import os  # mandatory
import random
import math

sys.path.insert(0, sys.argv[6])  # mandatory
sys.path.insert(0, os.path.abspath(os.path.join(sys.argv[6], "..")))  # mandatory
from sla_object import SLA  # noqa mandatory


sla = SLA(sys.argv)  # mandatory

# ///////////////\\\\\\\\\\\\\\
# write here the code that should not be repeated at each file creation
colors = [
    "Blue",
    "Cyan",
    "Green",
    "Magenta",
    "Red",
    "Yellow",
]
cut_origin = 28.57
# \\\\\\\\\\\\\\\//////////////

for file_number in range(
    sla.first_number, sla.first_number + sla.number_of_files
):  # mandatory
    sla.init_root()  # mandatory

    # //////////////\\\\\\\\\\\\\
    # put here the objects you want on your files with their variable attributes
    sla.place("background")
    teta = 0
    for j in range(10):
        x, y, alpha, w, h = 0, 0, 0, 15, 15
        offset_y = 15
        mul = 1.2
        r = 0
        pas = 35

        for i in range(10):
            random.shuffle(colors)
            sla.place(
                "star",
                XPOS=x + cut_origin,
                YPOS=y + cut_origin,
                WIDTH=w,
                HEIGHT=h,
                ROT=alpha,
                PCOLOR=colors[0],
                PCOLOR2=colors[1],
            )

            x = r * math.cos(teta * math.pi / 180)
            y = r * math.sin(teta * math.pi / 180)
            alpha += 30
            w *= mul
            h *= mul
            r += pas
        teta += 10

    sla.place(
        "number",
        ITEXT=[{}, {"CH": f"{file_number:04}"}],
    )
    sla.place(
        "text",
        ITEXT=[{"FCOLOR": colors[0]}, {}, {"FCOLOR": colors[0]}],
    )
    sla.place("cut")

    # \\\\\\\\\\\\\\/////////////

    sla.sla_creation(file_number)  # mandatory
sla.sla_end_creation()  # mandatory
