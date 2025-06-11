The aim of this project is to create Pdf files or variable images. The programming language is Python, and the professional-quality files (with spot color and overprint management) are generated using Scribus. Once the files have been generated, we'll use the free online variable-data application (https://variable-data.graphics) to generate a Pdf file ready for printing.

Tested with win11 and ubuntu 22.04.1 LTS

# Clone of the repository

- git clone https://github.com/Herve-2476/Variable_Data_Printing.git

- cd Variable_Data_Printing

# Creation of the virtual environment (Python 3.10)

- python -m venv venv # or _python3 -m venv venv_

- source venv/bin/activate _# to launch your environment in linux / macOS_

- venv\Scripts\activate.bat _# to launch your environment in windows CMD_

- venv\Scripts\activate.ps1 _# to launch your environment in windows Powershell_

- pip install -r requirements.txt # to install the required libraries

# Installation of Scribus

You can download Scribus here : https://www.scribus.net/downloads/unstable-branch/

The examples were created with the version 1.5.8.  
After installation, for windows users only, you must define the path of the Scribus executable in the `constants.py` file in `./utils/`.
By default we have `SCRIBUS_EXE = ["C:/Program Files/Scribus 1.5.8",]` but if you have installed Scribus 1.5.3 in Program Files you need to change it with `SCRIBUS_EXE = ["C:/Program Files/Scribus 1.5.3","C:/Program Files/Scribus 1.5.8",]`

You can verify your installation (virtual environment + required libraries + Scribus + possibly the modification of `SCRIBUS_EXE`) by running pytest (just type the pytest command in your terminal).

```bash
pytest
```

Four tests must passed.

Note : If you are not interested with the generation of unit files with Scribus you can skip the part One and you don't have to install Scribus, however as we shall see in the part Two, Scribus can help you with complex impositions.

# Part One : GENERATION OF UNIT FILES

# Running your first project

To run a project you must define a working directory in the `app_settings.py` file in the `./hot_folder` directory with for example the line : `working_directory = r"./examples/hello_world"`.
By default if the file app_settings is not present in the `./hot_folder` directory, the program will create it with the line above.  
The command to run a project is :

```bash
python run_unitary.py
```

So in the two previous cases you will running the hello_world project with the previous command.  
Before you start your first project, the best way to understand how the program works is to run the following examples (in order) and read the explanations.

Note : When you'll run the following 'hello_world' examples, the unitary files created will be in the `pdf_created` sub-directory and you'll find the imposed file in the `imposition` sub-directory.

# Running hello_world

```py
working_directory = r"./examples/hello_world" # in the app_settings.py file in the `./hot_folder` directory
```

```bash
python run_unitary.py
```

When you run the above command, you are going to create 10 pdf files and 10 png files. Options are defined in the `default_settings.py` file in `./unitary`. You can redefine these options in the `app_settings.py` file in the the `./hot_folder` directory or in the file `settings_unitary.py` in the working_directory (`./examples/hello_world`). Options in `settings_unitary.py` overwrite options in `app_settings.py` which overwrite the options in `default_settings.py`. You also can define the number of files you want to create in the command :

```bash
python run_unitary.py 15
```

It overwrites the number of files option defined in `settings_unitary.py` and will create 15 pdf files and 15 png files (because `create_png = True` in the `settings_unitary.py` file).

The Scribus source file is in the directory `./examples/hello_world/sla_in`. A sla file is an xml file, you can open it with a text editor (with the right extension to have a nice presentation). The program parses the sla file with the library `xml.etree.ElementTree`. Scribus objects have a tag `"PAGEOBJECT"`. As you can see there are only two in `hello_world.sla` file. If you look at the attributes of the first tag `PAGEOBJECT`, you can find the `ANNAME` attribute (`"hello_world"` in this example). With this name we are going to manipulate the object in the `generator.py` file in the working_directory (`./examples/hello_world`).  
In the `generator.py` file you can write code into two sections. The first one will be executed only once and the second will be executed for the creation of each new file.  
In our hello world example we only change the text with a variable number and the color of the text. We can only use the colors of the sla file. You can find them at the beginning of the sla file with the `COLOR` tag and the attribute `NAME`. To place an object in the file we have to use the `place` method. The first argument is the name of the object or the object itself (see hello_world_2 example).
Examples :

```py
sla.place("hello_world") # places the object "hello_world" without change

sla.place("hello_world",XPOS=sla.width/2,YPOS=sla.height/2,ROT=45) # places the middle of the object "hello_world" in the middle of the page with a 45 degrees rotation.
```

Note : The middle of a text object is not the middle of the text but the middle of the box where the text is written.

The previous examples modify attributes of the PAGEOBJECT tag in the sla file but in the hello world example we want to change the text and the color of the text. As you can see in the sla file these attributes are not with PAGEOBJECT tag but with ITEXT tag. Moreover we will see in the hello_world_1 example that we can have many ITEXT tags. That's why it is a little bit different to modify these arguments.  
Examples :

```py
sla.place("hello_world",ITEXT=[{"CH":"Hello"}]) # places the object "hello_world" with the text "Hello".

sla.place("hello_world",ITEXT=[{"FCOLOR":"Red"}]) # places the object "hello_world" with the text unchanged in red.

sla.place("hello_world",ITEXT=[{"FONTSIZE":14}]) # places the object "hello_world" with the text unchanged and with a font size of 14.

sla.place("hello_world",ROT=-45,ITEXT=[{"FONTSIZE":12,"FCOLOR":"Green"}]) # places the object "hello_world" with the text unchanged in green, with a font size of 12 and a 45 degrees counterclockwise rotation.

sla.place("hello_world",ITEXT=[{"CH": f"Hello World {file_number:04} !!!","FCOLOR": random.choice(colors)}]) # places the object "hello_world" with changed text and a random color from the list colors.
```

Note : You can place the same object as many times as you want, so you can test the examples above by copying and pasting each line in the generator.py file (With changing the position attributes otherwise the objects will be on the top of each other).

# Running hello_world_1

```py
working_directory = r"./examples/hello_world_1"
```

```bash
python run_unitary.py
```

In this example we use five objects. You can see in the `Document-1.sla` file that the two text objects have many `ITEXT` tags. Let's see how to modify their attributes.  
Examples :

```py
sla.place("text",ITEXT=[{},{},{"FCOLOR":"Blue"}]) # places the object `"text"` i.e. the text "!!! Hello World !!!" with the last three exclamation marks in Blue.

sla.place("text",ITEXT=[{},{"FCOLOR":"Cyan"}]) # places the object `"text"` i.e. the text "!!! Hello World !!!" with the world "Hello World" in Cyan.
```

The third object (the star) is placed 100 times with changes of positions, colors and size. You can retrieve the initial position of an object with the `sla.middle_of_object` dictionnary.

Example :

```py
sla.place("star") # places the star as in the Document-1.sla file
sla.place("star", XPOS=sla.middle_of_objects["star"].XPOS + 20 * 72 / 25.4) # places the star with an offset of 20 mm to the right
```

Note : The resolution of a Scribus file is the same as PDF file i.e. 72 pts per inch (25.4 mm).

You can use the `get` method to retrieve the value of an attribute of an object.The first argument is the name of the object or the object itself and the second argument is the name of the attribute. The method return 0 if the attribute is not defined. Be careful if you want to retrieve the position attributes with this method. In fact the coordinates in the sla file are the coordinates of the top left corner of the box that enclose the object and not the middle of this box. Moreover the origin of the reference frame of the sla file is not the origin of what you see in Scribus, there is an offset that we can see in the sla file in the tag `PAGE` with `PAGEXPOS` and `PAGEYPOS` attributes. The use of the dictionnary `middle_of_objects` solves these problems.

Example :

```py
sla.place("star",WIDTH=float(sla.get("star", "WIDTH")) * 2,HEIGHT=float(sla.get("star", "HEIGHT")) * 2) # places the star as in the Document-1.sla file with twice the initial size
```

The fourth object, the cut line is overprinting with a spot color named "CUT". It's interesting to place it on the file during development phase to place the objects correctly but don't forget to comment or erase the line when the generator file is ready if you don't use a professionnal press.
The fifth object is the background. It must be placed in first position otherwise it will hide the objects placed before.

# Running hello_world_2

```py
working_directory = r"./examples/hello_world_2"
```

```bash
python run_unitary.py
```

Don't forget to open the sla file (in an editor of text, not only in Scribus) to have a good understanding of the generator.py file. In this example we use several source sla files. We could have used only one file (by using layers) but in this case I find it easier with several files. Also sometimes you will import several pdf files or ai files to work on and again it will be easier to work on several sla files (after conversion). In this case, remember that you can use all the objects of all the sla files but the header of all the generated sla files will be the one of the first source sla file ( the name is displayed in the console ). To place an object you just have to prefix the name of the object with the name of the sla file.
Examples:

```py
sla.place("Document-1_stars") # places the object stars of the file Document-1.sla
sla.place("Document-5_stars") # places the object stars of the file Document-5.sla
```

In this example the object `stars` and the object `earth` are groups of objects. The first one is placed without change. With the second and with a for loop we can change the attributes of the objects that are in the group without knowing the name of each object.

Note 1 : The objects in the group object `earth` are not filled with one color but with gradient, that's why we use the tag `CSTOP` and the attribute `NAME to modify it. (see how the sla file is constructed)

Note 2 : There are additional elements on the imposed file, it is because this example is also used to explain the imposition part which will be seen just below. In the meantime to have the normal imposition you can just rename the file `settings_imposition.py` in the working directory to old (don't delete it) and run again the command `python run_unitary.py`.

# Creation of a project

```py
working_directory = r"path_of_the_project" # in the app_settings.py file
```

```bash
python run_unitary.py
```

The command above will create all directories and files needed for the project (if they do not already exist). By default we will have :

- the directory `path_of_the_project`
- the directory `path_of_the_project/sla_in`
- the directory `path_of_the_project/sla_created` # created to generate sla files but then deleted if `delete_sla=True` (by default)
- the directory `path_of_the_project/png_created` # created only if create_png=True (False by default)
- the directory `path_of_the_project/pdf_created`
- the file generator.py in the directory `path_of_the_project`# it's a copy of the generator_init.py file in ./unitary
- the file settings_unitary.py in the directory `path_of_the_project` # it's a copy the app_settings.py file with mandatory options for imposition

You can change these directories by settings the variables `sla_in_dir`, `sla_created_dir`, `pdf_created_dir`, `png_created_dir` in the `app_settings.py` file.
After running the previous command you will raise the exception `Exception: There is no sla files to treat in the directory path_of_the_project\sla_in` because there is no sla file in the directory `sla_in`. Open Scribus, create a sla file, put it in the directory `sla_in`, fill the `generator.py` file and run the project.
Note : It's sometimes interesting during the development of your project to set `delete_sla` to False in order to edit the sla files generated to understand a bug.

# Running a project

```py
working_directory = r"path_of_the_project" # in the app_settings.py file
```

```bash
python run_unitary.py
```

To run a project we only need to set the `working_directory` in the `app_settings.py` file. All the others settings should be in the `settings_unitary.py` file in the working directory (unles you want to change the default directories).
The previous command can take three arguments that you can set in the `settings_unitary.py` file but these arguments overwrite those of the `settings_unitary.py` file.

```bash
python run_unitary.py number_of_files number_of_sla_instances number_of_export_instances
```

For example :

```bash
python run_unitary.py 10000 4 2
```

This command will create 10000 files with 4 instances python to create sla files and each instance python will launch 2 instances to export the sla files in pdf files or png files or both. We export with Scribus and my advice is not to exceed the number of the cores of your machine for the number of the scribus instances. In the example we have 4x2= 8 Scribus instances and indeed my machine have 8 cores. In fact for the speed it's better to run :

```bash
python run_unitary.py 10000 8
```

This command will create 10000 files with 8 instances python to create sla files and each instance python will launch 1 instance ( if number_of_export_instances is not set in settings.py file with another value ) to export the sla files. Normally it's better because the eight cores of the machine are always in use( 8 for generate sla files and 8 for export). In some cases you will have to launch only one instance Python ( if you control the unicity of each file for example ), thus you will be able to launch the command :

```bash
python run_unitary.py 10000 1 8
```

Of course these settings depend on the number of file you want to create and if you want to use your machine for anothers tasks during the creation.

# Methods of the SLA Class

## - display_named_sla_objects()

Syntax : `object_SLA.display_named_sla_objects()`

- This method display the name of all named objects found in the sla source files. Be careful in Scribus all the objects have generic names (like Text1, Polyline5, etc..) but these names are not in the sla file. You must name in Scribus the objects you want to place on your files.

## - display_sla_colors()

Syntax : `object_SLA.display_sla_colors()`

- This method display the list of all the colors of the sla source file. It's an easy way with a copy/paste to define a colors list in your `generator.py` file.

## - place()

Syntax : `object_SLA.place(element,attribute=attribute_value,tag=[{attribute_name_of_tag:attribute_value,},],)`

- place the element on the generated file
- element : the object name or the object itself
- attribute : it's an attribute of the tag PAGEOBJECT
- tag : it's a child tag of PAGEOBJECT tag. The value is a list of dictionnary because we can have the same tag several times

## - get()

Syntax : `object_SLA.get(element,attribute,default_value)`

- return the value of the attribute of the `PAGEOBJECT` tag of the element
- element : the object name or the object itself
- attribute : it's an attribute of the tag `PAGEOBJECT`
- default_value : value returned if the attribute is not found (0 by default)

# Part Two : GENERATION OF AN IMPOSITION

# Generate your first imposition

# Running hello_world

To generate an imposition you must define a working directory in the `app_settings.py` file in the `./hot_folder` directory with for example the line : `working_directory = r"./examples/hello_world"`.
By default if the file app_settings is not present in the `./hot_folder` directory, the program will create it with the line above.  
The command to generate an imposition is :

```bash
python run_imposition.py
```

The imposed file is in the `imposition` sub-directory. If you didn't run the `hello_world` example of the first part you will generate an error because you need unit files to generate an imposition. If your installation is complete, you can execute the command `python run_unitary.py` which will automatically generate the unit files and the imposition. Then you can use the command `python run_imposition.py` to only generate the imposition. If you don't have installed Scribus you can't use this example but it's important to understand how it works.
When you create a project with Scribus with the command `python run_unitary.py`, the program create the `settings_unitary.py` file and the `settings_imposition.py` file. The program of imposition retrieves in the first file the number of files to impose with the first number and the pdf_created_dir to know where are the files to be imposed. Let's take a look at the second file.

```py
content = "Pdf_file_1"
__Pdf_file_1 = {
    "path": 'os.path.join(settings.pdf_source_dir, f"{number_file+settings.first_number-1}.pdf")',
    "transformation": "0",
}
```

The content data indicates the object in each window of the imposition. To understand what is a window, we must first define the sheet and the page. Sheet and page dimensions are set in the `default_settings.py` file in the `./imposition` directory. All these parameters can be redefined in the `settings_imposition.py` file. The sheet is the paper area and the page is the printing area. The number of windows on the page is calculated with the trimmed dimensions of the first pdf file (`1.pdf` in this case). The trimmed dimensions of the file are calculated with the parameter `file_bleed`. The file dimensions are retrieved automatically.

The details of the pdf objects are defined with the data `__Pdf_file_1`.

- `"path"` defined the files to put in the windows. The value of `settings.pdf_source_dir` is here the value of `pdf_created_dir` retrieved in the `settings_unitary.py` file (as `first_number`).`number_of_files` is an automatic variable that is incremented by one for each iteration.
- `"transformation"` defined the position of the pdf file in the window.
  - `"0"` = the file is centered without rotation.
  - `"45"` = the file is centered with a rotation of 45 degrees.
  - `(5,5,30)` = The origin is left bottom corner of the window. The file is offset by 5 mm in x and y and rotated of 30 degrees.

Note : In a similar way you can define the position of the page on the sheet with the parameter `page_transformation`

# Create an automatic imposition

We will create a project of imposition in the directory `./examples/my_imposition`. To do that, just set the file `app_settings.py` in the `hot_folder` directory with this path and run the command :

```bash
python run_imposition.py
```

This command creates the directory `./examples/my_imposition`, the sub-directories `/imposition` and `/pdf_source` and the file `settings_imposition.py`. The directory `pdf_source` can be changed with the parameter `pdf_source_dir`. The program raise an error after the execution of the command because there is no file to impose. So just put some files in the source directory and run again the imposition. You can copy some files from the directories `hello_world`, `hello_world_1` and `hello_world_2`. You can have some files of different dimensions but remember, the number and the dimensions of windows on the page is calculated with the trimmed dimensions of the first pdf file.

Example: file dimensions = 105.0 mm x 75.0 mm with file_bleed = 10 mm so we have trimmed size retained = 85.0 mm x 55.0 mm

The dimensions of the windows are calculated with `space_cut_in_width` and `space_cut_in_height` parameters. In our examples, if we have `space_cut_in_width` = 4 mm and `space_cut_in_height` = 4 mm so we have windows dimensions = 89.0 mm x 59.0 mm.

The parameters `bleed_in_width` and `bleed_in_height` are only used if we have simple cut (`space_cut_in_width`= 0 and/or `space_cut_in_height` = 0).

The `Number of poses retained` is calculated automatically with cut dimensions, space cut dimensions, bleed dimensions and band marks dimensions. You can set them with the both parameters `poses_number_in_sheet_width` and `poses_number_in_sheet_height`.

By default there are crop marks on the imposition. You can delete them if you delete the parameter `marks` in the `settings_imposition.py` file or if you set it to `()`. You can move the marks with the `offset_crop_mark` parameter (offset to the Cut).

The poses of the imposition can be rotated with the parameter `poses_rotation`. The value must be in the list : `[0,90,-90,180]` (in degrees). (we will see below that in manually mode that the rotation of each pose can be set with any value)

Let's take a look at the `settings_imposition.py` file.

```py
marks = "Pdf_file_2"
content = ("Pdf_file_1",)
__Pdf_file_1 = {
    "path": "os.path.join(settings.pdf_source_dir, settings.files_list[number_file-1])",
    "transformation": "0",
}
__Pdf_file_2 = {
    "path": 'os.path.join(settings.working_directory, "fixed_marks.pdf")',
    "transformation": "0",
}
```

In the parameter `marks` we have only one pdf object, the file `fixed_marks.pdf` which is automatically created by the program.

In the parameter `content` we have only one pdf object that points the files of `pdf_source_dir` directory.

We can define the imposition more precisely. For example if you want to repeat the same file (the first of directory in this case) you can change the following lines.

```py
content = {"*": ("Pdf_file_1", 12)}
__Pdf_file_1 = {
    "path": "os.path.join(settings.pdf_source_dir, settings.files_list[0])",
    "transformation": "0",
}

```

In my example I have 4 poses in a row and 3 poses in a column. You can replace for the same result `settings.files_list[0]` by the real name of the file (`"path": "os.path.join(settings.pdf_source_dir, 'file_name.pdf')"`).

If you have 3 files to impose you can change the following lines.

```py
content = {
    "1-4": ("Pdf_file_1", 4),
    "5,9": ("Pdf_file_3", 2),
    "6-8,10-12": ("Pdf_file_4", 6),
}
__Pdf_file_1 = {
    "path": "os.path.join(settings.pdf_source_dir, settings.files_list[0])",
    "transformation": "0",
}
__Pdf_file_3 = {
    "path": "os.path.join(settings.pdf_source_dir, settings.files_list[1])",
    "transformation": "0",
}
__Pdf_file_4 = {
    "path": "os.path.join(settings.pdf_source_dir, settings.files_list[2])",
    "transformation": "0",
}

```

The directions for identifying poses are from right to left and from top to bottom.

# Running hello_world_2

Set the `app_settings.py` file to `./examples/hello_world_2` and run the command `run_imposition.py`.
Don't forget to use the good `settings_imposition` file if you changed it when you have run the command `run_unitary.py`.
We see in this example that we can add variable objects when imposing(pdf file, text, qrcode etc..). In fact if we have some fixed files it's much faster than using Scribus. Let's take a look at the `settings_imposition.py` file.

```py
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
```

We are still in an automatic imposition so the file `fixed_marks.pdf` in the marks parameter is automatically generated by the program. We have two new objects in the marks parameter, a qrcode object and a text object. Like the `number_file` variable you can adress the page with the variable `number_page`. The objects are positionned on the page (not on the sheet) with the origin at the bottom left. Units are millimeter, degrees and points (font). `Helvetica` is a font recognized by ReportLab, so we can use it directly.

In the content parameter we have also two more objects. These objects are positionned on the pose with the origin at the bottom left of the cut (before the possible rotation of the pose). `DIN-Regular` is not a font recognized by ReportLab, so we have to define it. We do that with the paramater fonts (only ttf fonts).

Note 1 : The spot color can take a last argument : the density between 0 and 1

Note 2 : Reportlab recognizes colors like 'white', 'green', 'black' etc...

Note 3 : In the object text the parameters `center` and `overprint` are by default set to 0.

# Running hello_world_3

Set the `app_settings.py` file to `./examples/hello_world_3` and run the command `run_imposition.py`.
In this example we make an manual imposition, i.e we give a template to define the fixed marks and the position and the orientation of the poses. The template is a Scribus file. Open the `template.sla` with Scribus in the working directory to see how it should be structured.

There are two layers. The `Marks` layer is to define the fixed marks of the imposition. The `Imposition` layer is to define the position and the orientation of the poses. Each pose must be name `window_n` with n between 1 and the total number of the poses. The number `n` is the number that we find in the content definition in the `settings_imposition.py` file. In Scribus you need the windows `Properties` (F2), `Outline` and `Layers` (F6) to work easily.
When you run the command `run_imposition.py` the program export the layer `Marks` in the `fixed_marks.pdf` file and retrieve the position and the orientation of all the poses of the `Imposition` layer.

Let's take a look at the `settings_imposition.py` file.

```py
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
    "path": 'os.path.abspath(r"./examples/hello_world_3/data1.csv")',
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
```

In the `marks` parameter we have two new objects. `"CSV_2,1"` means that we use the csv file defined in the `__CSV_2` object and in this file we begin to read the first record. We can use the value of this csv file in all the objects of `marks` or `content` with the variables `"CSV_2_column_1"` and `"CSV_2_column_2"`. `"number,4,-1"` means that we create a variable `number` that will take the value 4 for the first page, 3 for the second page etc... We can use this variable in all the objects of `marks`.

# Speed of imposition

To accelerate the imposition we use two parameters, `number_of_imposition_instances` and `final_number_of_files`.
Today a lot of machines have 4 cores so you can always set the first parameter to 4 (and more if your machine is stronger).
But if you create 4 instances you have to merge 4 files to have a `final_number_of_files` of 1 and the merger takes a little time. So for a small imposition set `final_number_of_files` to one but if the final file is big don't hesitate to increase the `final_number_of_files` especially since professionnal printing machines can handle easily multiple files and often are limited with the size of each file (to rip the file).

# Compliance with PEP 8 guidelines

- flake8
