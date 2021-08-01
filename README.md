# Open source controller for ArtNet / Lighting Desk

This project is a hardware / software combined project.

### Goals
Its goal is to create a lighting desk which is usable for concerts and/or theatre.

This is a personal project which I develop in my spare time and I have no final goals set.

### Dependencies
this project depends on Qt5 and the python3 implementation pyqt5

### Usage
* in the `Create_lamps.py` change what lamps you want to be accessible
* if you want to use arduinos for controlling faders / getting inputs run `serial_setup.py` from the setup dir
  * else set `serial_enable` in `GlobalVar.py` to `False`
* run `python3 main.py` in the `python` directory


If you have any Ideas on how to improve this project, feel free to let me know or contribute yourself.

Copyright (C) 2019 Tobias Teichmann <tobias@teichmann.top>
