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

  - Whatever choice is made, it seems important that the selection is mirrored on the other side of the keyboard.
  - Someone on Reddit describes VSYS-VSYS GND-GND GPX-GPX GPY-GPY
    - It sounds like they may actually not have been using a Pico, but some other RP2040 board
  - Someone who built a split with Picos, but not QMK (KMK instead) provided a different recommendation (and also mentioned USART comms.).  They recommended 3V3-3V3 GND-GND GPX-GPX GPY-GPY

A more definite schema needs to be organised.

Let's consider the purpose of the 4 wires between the two keyboard halves.

- 1 pin for transmitting data to other side
- 1 pin for receiving data from other side
- 1 pin for ground
- 1 pin for power

Originally, I did not consider fully that "for power" did not mean "for powering serial communication over TRRS".  That wire has got to be the only way that the controllee half of the keyboard gets power.  The controller half gets power in over a micro USB connection.  But the controllee half gets power from the controller half over the TRRS cable.

We can be reasonably confident that 3 of the controller pin to controllee pin connections can be wired like 

```
GND-GND GPX-GPX GPY-GPY
```

but the question of the power pins remains.

It looks like the Piantor, which uses QMK on Picos, has VSYS wired to VSYS.

https://github.com/beekeeb/piantor/blob/main/docs/left-front.png

https://github.com/beekeeb/piantor/blob/main/docs/keyboard_right.png

It looks like someone else built a handwired dactyl using Picos and QMK, wiring 3V3 to 3V3.

https://www.reddit.com/r/ErgoMechKeyboards/comments/15hx3r7/handwired_dactylmanuform_with_raspberry_pi_picos/

It's possible this is a cat-skinning problem.