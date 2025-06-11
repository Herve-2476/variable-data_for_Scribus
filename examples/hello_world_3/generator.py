import sys  # mandatory
import os  # mandatory

sys.path.insert(0, sys.argv[6])  # mandatory
sys.path.insert(0, os.path.abspath(os.path.join(sys.argv[6], "..")))  # mandatory
from sla_object import SLA  # noqa mandatory


sla = SLA(sys.argv)  # mandatory

# ///////////////\\\\\\\\\\\\\\
# write here the code that should not be repeated at each file creation

# \\\\\\\\\\\\\\\//////////////

for file_number in range(
    sla.first_number, sla.first_number + sla.number_of_files
):  # mandatory
    sla.init_root()  # mandatory

    # //////////////\\\\\\\\\\\\\
    # put here the objects you want on your files with their variable attributes

    # \\\\\\\\\\\\\\/////////////

    sla.sla_creation(file_number)  # mandatory
sla.sla_end_creation()  # mandatory
