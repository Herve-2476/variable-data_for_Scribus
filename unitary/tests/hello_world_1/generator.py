import sys  # mandatory
import os  # mandatory

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
rot = -45
# \\\\\\\\\\\\\\\//////////////

for file_number in range(
    sla.first_number, sla.first_number + sla.number_of_files
):  # mandatory
    sla.init_root()  # mandatory

    # //////////////\\\\\\\\\\\\\
    # put here the objects you want on your files with their variable attributes
    x, y, alpha, w, h = 0, 0, 0, 15, 15
    offset_y = 15
    mul = 1.2
    sla.place(
        "text",
        ROT=rot,
        ITEXT=[
            {"FCOLOR": colors[file_number % len(colors)]},
            {},
            {"FCOLOR": colors[(file_number + 1) % len(colors)]},
        ],
    )
    rot += 15
    sla.place(
        "number",
        ITEXT=[
            {},
            {"CH": f"{file_number:04}", "FCOLOR": colors[file_number % len(colors)]},
        ],
    )
    for i in range(10):
        sla.place(
            "star",
            XPOS=x + cut_origin,
            YPOS=y + cut_origin,
            WIDTH=w,
            HEIGHT=h,
            ROT=alpha,
            PCOLOR=colors[i % len(colors)],
            PCOLOR2=colors[(i + 1) % len(colors)],
        )
        sla.place(
            "star",
            XPOS=x + cut_origin,
            YPOS=y + cut_origin,
            WIDTH=w,
            HEIGHT=h,
            ROT=alpha + 45,
            PCOLOR=colors[(i + 2) % len(colors)],
            PCOLOR2=colors[(i + 3) % len(colors)],
        )
        y += offset_y
        x = y * y / 80
        alpha += 30
        w *= mul
        h *= mul

    sla.place("cut")

    # \\\\\\\\\\\\\\/////////////

    sla.sla_creation(file_number)  # mandatory
sla.sla_end_creation()  # mandatory
