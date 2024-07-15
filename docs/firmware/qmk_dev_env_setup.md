# Setting up the development environment for editing ThumbDox's firmware

ThumbDox runs [QMK firmware](https://qmk.fm/).

## Setup steps

Read this whole page before starting.

TODO : test whole process on a separate computer with a fresh clone of the ThumbDox repo.

### Dependencies

Install git and python3-pip if not already present on your system.

Then...

```
# cd to root of ThumbDox repo.

# Create a virtual environment to install dependencies.
$ python3 -m venv ./venv

# Activate the virtual environment.
$ source ./venv/bin/activate

# Actually install the dependencies.  This installs both packages needed
# for 3D modelling and packages needed for building the firmware to the
# virtual environment, including QMK.
$ pip install -r requirements.txt
```

Export an environment variable that configures QMK to work within **this** repo.

`$ export QMK_HOME='./qmk_firmware'`

Then you can run setup.

`$ qmk setup`

TODO : check whether above steps may be unnecessary once I set up QMK within this repo and decide what makes sense to check in.

## Actual development steps

### Editing the ThumbDox firmware

TODO : add a brief note on which files to edit to change the keymap, and which files represent the rest of the source specific to this keyboard.

### Compiling

Normally QMK keyboards and keymaps are stored in a fork or clone of the QMK repo itself.  The setup for ThumbDox is a bit inside out, because I want to keep the firmware and the 3D model source in the same repo.  Specifically, in the ThumbDox repo.

As such, to compile the ThumbDox firmware from inside the ThumbDox repo we need to perform the unconventional step of exporting an environment variable whose value is a path **inside this repo**.

This tells QMK where to look for firmware source (inside this repo), and where to deploy build output (inside this repo). 

```
$ export QMK_HOME='./qmk_firmware' # Optional, set the location for qmk_firmware
```

TODO : I expect the compilation command will be something like `qmk compile -kb handwired/thumbdox -km default`.  Can maybe automate this command + env var + remembering to activate venv with a build script?  Or maybe the venv will not play nice with the env var being activated either before or after it by a shell script...

### Flashing

TODO : This will be a matter of copying .uf2 files to respective MCUs.  Will there be two distinct .uf2 files or is the same file used for each MCU?
