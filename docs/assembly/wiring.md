# Wiring

This doc exists in place of a full wiring diagram.

## TRRS

Each MCU needs a TRRS jack wired to it.

The Raspberry Pi Pico cannot use I2C over the TRRS connection because it is not supported (either in QMK or at all, not sure which).

Thus, serial communication must be used instead.

Pull up resistors are not required since using serial rather than I2C.

### Software support

Won't flesh this out fully here since it's a wiring doc.  But there is code required to set this up.  See:

- https://docs.qmk.fm/features/split_keyboard
- https://docs.qmk.fm/drivers/serial

### Full vs. half duplex serial comms.

Prefer full duplex for faster communication speeds over the TRRS link, just in case.

### Pins

Which pins on the MCU should be wired to the TRRS jacks?

Still need to determine this more definitely.

  - Whatever choice is made, it seems important that the selection is mirrored on the other side of the keyboard.
  - Someone on Reddit describes VSYS-VSYS GND-GND GPX-GPX GPY-GPY
    - It sounds like they may actually not have been using a Pico, but some other RP2040 board
  - Someone who built a split with Picos, but not QMK (KMK instead) provided a different recommendation (and also mentioned USART comms.).  They recommended 3V3-3V3 GND-GND GPX-GPX GPY-GPY