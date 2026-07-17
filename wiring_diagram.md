# Wiring Diagram — Railway Track Crack Detection Robot

Final pinout. All GPIO numbers are BCM.

## Power Connections
- Battery → L298N VIN (12V input)
- LM2596 Input → Battery
- LM2596 Output (5V) → Breadboard + rail
- Raspberry Pi GND → Breadboard − rail (common ground)

---

## L298N Motor Driver
- OUT1 & OUT2 → Left Motor
- OUT3 & OUT4 → Right Motor
- GND → Breadboard GND

GPIO Connections:
- IN1 → GPIO17 (Pin 11)
- IN2 → GPIO27 (Pin 13)
- IN3 → GPIO22 (Pin 15)
- IN4 → GPIO5 (Pin 29)

---

## GPS (NEO-6M)
- VCC → Breadboard +5V
- GND → Breadboard GND
- TX → GPIO15 (Pin 10)
- RX → GPIO14 (Pin 8)

---

## GSM Module
- VCC → LM2596 set to 4.0–4.2V (not 5V if SIM800L)
- GND → Breadboard GND
- TX → Raspberry Pi RX
- RX → Raspberry Pi TX

> ⚠️ **Known conflict:** GPS and GSM are both wired to the Pi's single
> hardware UART (GPIO14/15). They cannot both talk over that line at
> the same time. Recommended fix: connect the GSM module through a
> USB-to-TTL adapter (appears as `/dev/ttyUSB0`) and leave GPS on the
> onboard UART (`/dev/serial0`). Update `GPS_PORT` / `GSM_PORT` in
> `config.py` to match whatever you land on.

---

## Ultrasonic Sensor (HC-SR04)
- VCC → Breadboard +5V
- GND → Breadboard GND (or any common GND)
- TRIG → GPIO23 (Pin 16)
- ECHO → GPIO24 (Pin 18) *(through a voltage divider — HC-SR04 ECHO is 5V, Pi GPIO is 3.3V-only)*

---

## Buzzer
- **+ → GPIO21 (Pin 40)** ✅ final choice
- **− → Breadboard GND**

---

## Raspberry Pi Camera
- Connect to the CSI camera connector on the Raspberry Pi.

---

## Common Ground
All of these share the same GND:
- Raspberry Pi
- L298N
- GPS
- GSM
- Ultrasonic
- Buzzer
- LM2596
