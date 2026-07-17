# Railway Track Crack Detection Robot

A Raspberry Pi–based rover that drives along a railway track, uses a
camera + CNN to detect surface cracks, avoids obstacles with an
ultrasonic sensor, and sends an SMS alert with GPS coordinates when a
crack is found.

## Hardware
- Raspberry Pi (with CSI camera)
- L298N motor driver + 2 DC motors
- HC-SR04 ultrasonic sensor
- NEO-6M GPS module
- SIM800L (or similar) GSM module
- Buzzer
- LM2596 buck converter
- 12V battery pack

Full pin mapping: [`wiring_diagram.md`](wiring_diagram.md)

## Project Structure
```
railway_track_crack_detection_robot/
├── main.py                     # main control loop
├── config.py                   # pins, thresholds, ports
├── motor.py                    # L298N motor control
├── ultrasonic.py                # HC-SR04 obstacle sensing
├── gps.py                       # NEO-6M location reading
├── gsm.py                       # SMS alerts via AT commands
├── camera.py                    # Pi camera capture
├── ai_detection.py              # crack inference wrapper
├── utils.py                     # logging + buzzer
├── requirements.txt
├── wiring_diagram.md
├── models/
│   └── crack_detection_model.py # CNN architecture + loader
├── images/                      # saved crack detection frames
└── logs/                        # robot.log
```

## Setup
```bash
cd railway_track_crack_detection_robot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Enable the camera and serial interfaces:
```bash
sudo raspi-config
# Interface Options → Camera → Enable
# Interface Options → Serial Port → login shell: No, hardware: Yes
```

Set your alert phone number in `config.py`:
```python
ALERT_PHONE_NUMBER = "+91XXXXXXXXXX"
```

Drop your trained model weights at `models/crack_detection_model.h5`
(train separately — `crack_detection_model.py` defines the CNN
architecture used at inference time). Without weights, the robot
still runs end-to-end but predictions are meaningless.

## ⚠️ GPS/GSM UART Conflict
Both GPS and GSM are wired to the Pi's single hardware UART
(GPIO14/15) per the original wiring notes. They can't share it live.
Fix by moving the GSM module to a USB-to-TTL adapter and updating
`GSM_PORT` in `config.py` to `/dev/ttyUSB0` (keep GPS on
`/dev/serial0`).

## Run
```bash
python3 main.py
```
Logs go to `logs/robot.log`. Crack-detection frames are saved to
`images/`.

Stop with `Ctrl+C` — GPIO is cleaned up automatically on exit.
