# Setting up the development environment for 3D modelling

The [solidpython2 library](https://github.com/jeff-dh/SolidPython) is used to generate OpenSCAD code.

OpenSCAD is used to define the 3D models.

## Setup steps

### Install OpenSCAD

I installed OpenSCAD version 2021.01 with:

```
$ sudo apt-get install openscad
```

### Set up Python environment for generating OpenSCAD code

```
# Create virtual environment to install 3D modelling Python dependencies.
$ python3 -m venv ./venv

# Actually install the dependencies.
# Note "python3 -m pip install -r requirements.txt" and
# Note "pip install -r requirements.txt" did not work on my machine.
$ ./venv/bin/python3 -m pip install -r requirements.txt
```

## Actual development steps

### Editing the 3D model source

The source code for the 3D model is `3D_model/model.py`.  Editing that Python file is necessary to change the model (it is not intended that this project's generated OpenSCAD code be manually edited).

### Compiling the 3D model source to OpenSCAD code

`$ ./venv/bin/python3 3D_model/model.py`

### Viewing the rendered OpenSCAD code

`$ openscad 3D_model/model.scad`
