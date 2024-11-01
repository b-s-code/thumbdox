# Wiring

This document details wiring:

- within each keyboard half
 - i.e. how rows/columns are connected to each MCU
- between the two keyboard halves
 - i.e. how each MCU is is wired to its respective TRRS jack

## Software support for split keyboards

Won't flesh this out fully here since it's a wiring doc.  But there is code required to set this up.  See:

- https://docs.qmk.fm/features/split_keyboard
- https://docs.qmk.fm/drivers/serial

## TRRS connections

### TRRS communication mode

Each MCU needs a TRRS jack wired to it.

The Raspberry Pi Pico cannot use I2C over the TRRS connection because it is not supported (either in QMK or at all, not sure which).

Thus, serial communication must be used instead.

Pull up resistors are not required since using serial rather than I2C.

Note: ThumbDox uses *full duplex* serial communication (2 wires) which is purportedly faster.  It's unclear whether this is really necessary in practice.

### Which MCU pins can be used for connecting to TRRS jacks?

Let's consider, from the primary MCU's perspective, the purpose of the 4 wires between the two keyboard halves.

1. wire for transmitting data to the secondary MCU 
2. wire for receiving data from the secondary MCU
3. wire for ground
4. wire for supplying power to the secondary MCU

1, 2, and 3 can be wired to GPIO/ground pins.  But which pin to use for 4 is less clear.

Some split keyboards using Pico MCUs have VSYS wired to VSYS.  Others have 3v3 wired to 3v3.

People online argue about what's "right".  Neither setup is unanimously considered "preferred" or even "unambiguously okay".

Somewhat arbitrarily, 3v3 to 3v3 has been selected as the wiring scheme for supplying ThumbDox's secondary MCU with power.

## MCU pin assignment scheme

| Pin number | Pin name | Use |
|----|-----|----|
| 38 | GND | TRRS - ground |
| 36 | 3V3(OUT) | TRRS - power transmission |
| 1  | GP0 | Serial TX |
| 2  | GP1 | Serial RX |
| 16 | GP12 | Top row |
| 17 | GP13 | Home row |
| 19 | GP14 | Below home row |
| 20 | GP15 | Bottom row |
| 15 | GP11 | Thumb row |
| A  | GPA | Pinky column |
| B  | GPB | Ring column |
| C  | GPC | Middle column |
| D  | GPD | Index home column |
| E  | GPE | Index centre-most column |
| F  | GPF | Thumb centre-most column |

TODO : assign pins for above purpose, sanity check the idea.
