The aim of this project is to create Pdf files or variable images. The programming language is Python, and the professional-quality files (with spot color and overprint management) are generated using Scribus. Once the files have been generated, we'll use the online VariableData application (https://variable-data.graphics) to generate a Pdf file ready for printing.

Tested with win11 and ubuntu 22.04.1 LTS

# Clone of the repository

- git clone https://github.com/Herve-2476/variable-data_for_Scribus.git

- cd variable-data_for_Scribus

# Creation of the virtual environment (Python 3.13)

- python -m venv venv # or _python3 -m venv venv_

- source venv/bin/activate _# to launch your environment in linux / macOS_

- venv\Scripts\activate.bat _# to launch your environment in windows CMD_

- venv\Scripts\activate.ps1 _# to launch your environment in windows Powershell_

- pip install -r requirements.txt # to install the required libraries

# Installation of Scribus

You can download Scribus here : https://www.scribus.net/downloads/

The examples were created with the version 1.6.4.  
After installation, for windows users only, you must define the path of the Scribus executable in the `constants.py` file in `./utils/`.
By default we have `SCRIBUS_EXE = ["C:/Program Files/Scribus 1.6.4",]` but if you have installed Scribus 1.5.3 in Program Files you need to change it with `SCRIBUS_EXE = ["C:/Program Files/Scribus 1.5.3","C:/Program Files/Scribus 1.6.4",]`

You can verify your installation (virtual environment + required libraries + Scribus + possibly the modification of `SCRIBUS_EXE`) by running pytest (just type the pytest command in your terminal).

```bash
pytest
```

Three tests must passed.

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

Note : When you'll run the following 'hello_world' examples, the unitary files created will be in the `pdf_created` sub-directory.

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

Note : The objects in the group object `earth` are not filled with one color but with gradient, that's why we use the tag `CSTOP` and the attribute `NAME` to modify it. (see how the sla file is constructed)

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
- the file settings_unitary.py in the directory `path_of_the_project` # it's a copy of the app_settings.py file with mandatory options for imposition

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

To run a project we only need to set the `working_directory` in the `app_settings.py` file. All the others settings should be in the `settings_unitary.py` file in the working directory (unless you want to change the default directories).
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

This command will create 10000 files with 8 instances python to create sla files and each instance python will launch 1 instance ( if number_of_export_instances is not set in settings.py file with another value ) to export the sla files. Normally it's better because the eight cores of the machine are always in use( 8 for generate sla files and 8 for export). In some cases you will have to launch only one instance Python ( if you want to control the unicity of each file for example ), thus you will be able to launch the command :

```bash
python run_unitary.py 10000 1 8
```

Of course these settings depend on the number of file you want to create and if you want to use your machine for anothers tasks during the creation.

# Methods of the SLA Class

## - display_named_sla_objects()

Syntax : `object_SLA.display_named_sla_objects()`

- This method display the name of all named objects found in the sla source files. Be careful in Scribus all the objects have generic names (like Text1, Polyline5, etc..) but these names are not in the sla file. You must rename in Scribus the objects you want to place on your files.

## - display_sla_colors()

Syntax : `object_SLA.display_sla_colors()`

- This method display the list of all the colors of the sla source file. It's an easy way with a copy/paste to define a colors list in your `generator.py` file.

## - place()

Syntax : `object_SLA.place(element,attribute=attribute_value,tag=[{attribute_name_of_tag:attribute_value,},],)`

- place the element on the generated file.
- element : the object name or the object itself.
- attribute : it's an attribute of the tag PAGEOBJECT.
- tag : it's a child tag of PAGEOBJECT tag. The value is a list of dictionnary (see how the sla file is built).

## - get()

Syntax : `object_SLA.get(element,attribute,default_value)`

- return the value of the attribute of the `PAGEOBJECT` tag of the element
- element : the object name or the object itself
- attribute : it's an attribute of the tag `PAGEOBJECT`
- default_value : value returned if the attribute is not found (0 by default)

# Part Two : GENERATION OF A PDF FILE WITH ALL UNIT FILES

# Running hello_world_2

in the `app_settings.py` file in the `./hot_folder` :

```py
working_directory = r"./examples/hello_world_2"
```

We will create 16 files so we run :

```bash
python run_unitary.py 16
```

Now, we'll use the online VariableData application (https://variable-data.graphics).

Click on the `Get started without account` button.

For the following actions, use the application image below.

Add a reference in the `REFERENCES` area with the `+` button.

In the `quantity` field, enter `16`.

Drag and drop the 16 Pdf files from the directory `./examples/hello_world_2/pdf_created` in the `Upload object files` area. After that the counter is `16/500`.

Add a Pdf object with the button `Add object`.

Click on the `no variable`field and select `number:01` and enter `.pdf` in the field just after.

Check that your entry is correct with the following image.
![screenshot](/examples/hello_world_2/image.png)
If ok, click on the button `Create`.

The application generates the pdf file and displays the first page.
If you like, you can download the 4-page pdf file by clicking on the button `PDF/CSV n°1/1`.

When you quit the application or click on the reset button, all files downloaded and created on the server are deleted.
If you just want to put variable text on a Pdf file or an image, the VariableData application can do this directly (using an Excel or Csv data file) and more quickly than creating unit files, but for more complex data such as color gradients, Scribus is a must.
