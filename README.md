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

##Photos
<img width="1600" height="1204" alt="WhatsApp Image 2026-07-17 at 6 30 36 PM" src="https://github.com/user-attachments/assets/d55b5a9e-a4f3-4df9-85e0-d941730d3227" />
<img width="1600" height="1204" alt="492cd2ac-e834-49c2-8ff2-875cf5657f22" src="https://github.com/user-attachments/assets/cb15481d-3b9f-4ce1-b252-243712e23dc0" />
<img width="1204" height="1600" alt="7fc91433-dbc7-4f1e-a6a4-65f4e17c7b94" src="https://github.com/user-attachments/assets/21a0b194-5970-4b40-8636-9c74c68c8b48" />



