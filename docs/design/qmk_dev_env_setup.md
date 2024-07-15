# Setting up the development environment for editing ThumbDox's firmware

ThumbDox runs [QMK firmware](https://qmk.fm/).

## Setup steps

Read this whole page before starting.

### Dependencies

Follow the instructions in QMK's documentation on [Setting Up Your QMK Environment](https://docs.qmk.fm/newbs_getting_started).  But ignore the step to install the QMK CLI with `$ python3 -m pip install --user qmk`.  Instead do this:

```
# cd to root of ThumbDox repo.

# Activate the virtual environment for the Thumbdox project.
$ source ./venv/bin/activate

# Install all dependencies of the ThumbDox project which can be installed with pip.
# This includes QMK.
$ pip install -r requirements.txt
```

## Actual development steps

### Editing the ThumbDox firmware

TODO : Want to set this up as what QMK docs call "External QMK Userspace".

### Compiling

TODO : I expect this will be `qmk compile -kb handwired/thumbdox -km default`.

### Flashing

TODO : I expect this will be a matter of copying .uf2 files to respective MCUs.
