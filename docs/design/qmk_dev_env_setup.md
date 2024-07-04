# Setting up the development environment for editing ThumbDox's firmware

[QMK firmware](https://qmk.fm/) is used by ThumbDox.

## Setup steps

### Dependencies

Follow the instructions in QMK's documentation on [Setting Up Your QMK Environment](https://docs.qmk.fm/newbs_getting_started).  But ignore the step to install the QMK CLI with `$ python3 -m pip install --user qmk`.  Instead do this:

```
# cd to root of ThumbDox repo.

# Activate the virtual environment for the Thumbdox project.
$ source ./venv/bin/activate

# Install all dependencies of the ThumbDox project which can be installed with pip.
$ pip install -r requirements.txt
```

## Actual development steps

### Editing the ThumbDox firmware

TODO

### Compiling

TODO

### Flashing

TODO
