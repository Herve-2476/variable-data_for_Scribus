import os

marks = ("Pdf_file_2", "QR_image_2", "Text_2")
content = ("Pdf_file_1", "QR_image_1", "Text_1")
fonts = {
    "DIN-Regular": os.path.abspath("./examples/hello_world_2/DIN-Regular.ttf"),
}
__Pdf_file_1 = {
    "path": 'os.path.join(settings.pdf_source_dir, f"{number_file}.pdf")',
    "transformation": "0",
}
__QR_image_1 = {
    "value": 'f"hello {number_file:04}"',
    "x": 73,
    "y": 2,
    "w": 10,
    "h": 10,
}
__Text_1 = {
    "value": 'f"N° {number_file:04}"',
    "x": 83,
    "y": 30,
    "alpha": 90,
    "font": "DIN-Regular",
    "font_size": 15,
    "color_font": "CMYKColorSep(0.09, 0.22, 0.65, 0.02, 'IFOIL')",
    "center": 0,
    "overprint": 0,
}
__Pdf_file_2 = {
    "path": 'os.path.join(settings.working_directory, "fixed_marks.pdf")',
    "transformation": "0",
}
__QR_image_2 = {
    "value": 'f"{number_page:06}"',
    "x": 2,
    "y": 2,
    "w": 10,
    "h": 10,
}

__Text_2 = {
    "value": 'f"Page N° {number_page:06}"',
    "x": 12,
    "y": 20,
    "alpha": 90,
    "font": "Helvetica",
    "font_size": 9,
    "color_font": "CMYKColor(0, 1, 0, 0)",
}
