marks = ("Pdf_file_4", "QR_image_4", "Text_5", "CSV_2,1", "number,4,-1")
content = {
    "1-2,5": ("Pdf_file_1", "Text_1", "QR_image_1", "CSV_1,10", 9),
    "3-4,6": ("Pdf_file_2", "Pdf_file_5", "Text_1", "QR_image_1", "CSV_1,19", 9),
    "7-9": (
        "Pdf_file_3",
        "QR_image_2",
        "QR_image_3",
        "Text_2",
        "Text_3",
        "Text_4",
        "CSV_1,1",
        "CSV_2,9",
        "number,9,-1",
        9,
    ),
}


__QR_image_4 = {
    "value": 'f"{number_page:06}"',
    "x": 0,
    "y": 0,
    "w": 10,
    "h": 10,
}

__Text_5 = {
    "value": 'f"Page N° {number_page:04}--{CSV_2_column_1}--Page N° {number:04} en décroissant"',
    "x": 10,
    "y": 20,
    "alpha": 90,
    "font": "Helvetica",
    "font_size": 9,
    "color_font": "black",
}


__QR_image_1 = {
    "value": "CSV_1_column_1",
    "x": 73,
    "y": 2,
    "w": 10,
    "h": 10,
}
__QR_image_2 = {
    "value": "CSV_1_column_1",
    "x": 15,
    "y": 85,
    "w": 10,
    "h": 10,
}
__QR_image_3 = {
    "value": "CSV_2_column_1",
    "x": 99,
    "y": 11,
    "w": 10,
    "h": 10,
}
__CSV_1 = {
    "path": 'os.path.join(settings.working_directory,"data1.csv")',
    "sep": ",",
}
__CSV_2 = {
    "path": 'os.path.abspath(r"./examples/hello_world_3/data2.csv")',
    "sep": ",",
}
__Pdf_file_1 = {
    "path": 'os.path.join(r"./examples/hello_world_2/pdf_created_source", f"{number_file}.pdf")',
    "transformation": "0",
}
__Pdf_file_2 = {
    "path": 'os.path.join(r"./examples/hello_world_1/pdf_created_source", f"{number_file}.pdf")',
    "transformation": "0",
}
__Pdf_file_3 = {
    "path": 'os.path.join(settings.working_directory, "pdf_source","collerette.pdf")',
    "transformation": "0",
}
__Pdf_file_4 = {
    "path": 'os.path.join(settings.working_directory, "fixed_marks.pdf")',
    "transformation": "0",
}
__Pdf_file_5 = {
    "path": 'os.path.join(settings.working_directory, "pdf_source","background.pdf")',
    "transformation": "0",
}
__Text_1 = {
    "value": "CSV_1_column_2",
    "x": 83,
    "y": 15,
    "alpha": 90,
    "font": "Helvetica",
    "font_size": 12,
    "color_font": "white",
}
__Text_2 = {
    "value": 'f"Collerette N° {number:04}"',
    "x": 34,
    "y": 76,
    "alpha": -33,
    "font": "Helvetica",
    "font_size": 12,
    "color_font": "white",
}
__Text_3 = {
    "value": "CSV_1_column_2",
    "x": 23,
    "y": 103,
    "alpha": -55,
    "font": "Helvetica",
    "font_size": 9,
    "color_font": "white",
}
__Text_4 = {
    "value": "CSV_2_column_2",
    "x": 92,
    "y": 17,
    "alpha": 45,
    "font": "Helvetica",
    "font_size": 9,
    "color_font": "white",
}
