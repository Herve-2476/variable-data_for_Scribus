# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 12:02:35 2016

@author: MonnierH
"""
import scribus
import sys
import os


def main(argv):

    first_number = int(argv[2])
    number_of_files = int(argv[3])
    delete_sla = argv[4]
    create_pdf = argv[5]
    create_png = argv[6]
    temp_dir = argv[7]
    sla_created = argv[8]
    pdf_created = argv[9]
    png_created = argv[10]

    for n in range(first_number, first_number + number_of_files):

        os.rename(
            os.path.join(sla_created, str(n) + ".sla"),
            os.path.join(temp_dir, str(n) + ".sla"),
        )
        scribus.openDoc(os.path.join(temp_dir, str(n) + ".sla"))

        if delete_sla:
            os.remove(os.path.join(temp_dir, str(n) + ".sla"))
        else:
            os.rename(
                os.path.join(temp_dir, str(n) + ".sla"),
                os.path.join(sla_created, str(n) + ".sla"),
            )

        if create_pdf:
            pdf = scribus.PDFfile()
            pdf.fontEmbedding = 1
            pdf.outdst = 1
            pdf.file = os.path.join(pdf_created, str(n) + ".pdf")
            pdf.save()

        if create_png:
            png = scribus.ImageExport()
            png.type = "png"
            png.dpi = 90
            png.name = os.path.join(png_created, str(n) + ".png")
            png.save()


if __name__ == "__main__":
    main(sys.argv)
