"""
gsm.py
SMS alert sending via AT commands (SIM800L-style GSM module).
"""

import time
import serial
import config


class GSMModule:
    def __init__(self):
        self.serial_conn = serial.Serial(
            config.GSM_PORT, baudrate=config.GSM_BAUDRATE, timeout=1
        )
        time.sleep(1)
        self._send_command("AT")          # check module responds
        self._send_command("AT+CMGF=1")   # set SMS text mode

    def _send_command(self, cmd, delay=0.5):
        self.serial_conn.write((cmd + "\r\n").encode())
        time.sleep(delay)
        response = self.serial_conn.read(self.serial_conn.in_waiting or 1)
        return response.decode(errors="replace")

    def send_sms(self, message, number=None):
        number = number or config.ALERT_PHONE_NUMBER
        self.serial_conn.write(f'AT+CMGS="{number}"\r'.encode())
        time.sleep(0.5)
        self.serial_conn.write(message.encode())
        time.sleep(0.5)
        self.serial_conn.write(bytes([26]))  # Ctrl+Z sends the message
        time.sleep(3)
        response = self.serial_conn.read(self.serial_conn.in_waiting or 1)
        return response.decode(errors="replace")

    def send_crack_alert(self, location_str):
        message = f"CRACK DETECTED on railway track.\nLocation: {location_str}"
        return self.send_sms(message)

    def close(self):
        self.serial_conn.close()
