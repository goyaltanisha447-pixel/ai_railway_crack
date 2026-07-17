"""
gps.py
NEO-6M GPS reader over UART, parses NMEA sentences with pynmea2.
"""

import serial
import pynmea2
import config


class GPSReader:
    def __init__(self):
        self.serial_conn = serial.Serial(
            config.GPS_PORT, baudrate=config.GPS_BAUDRATE, timeout=1
        )

    def get_location(self):
        """Returns (latitude, longitude) or None if no fix yet."""
        try:
            line = self.serial_conn.readline().decode("ascii", errors="replace").strip()
        except Exception:
            return None

        if line.startswith("$GPGGA") or line.startswith("$GNGGA"):
            try:
                msg = pynmea2.parse(line)
                if msg.latitude and msg.longitude:
                    return (msg.latitude, msg.longitude)
            except pynmea2.ParseError:
                return None
        return None

    def get_location_string(self):
        loc = self.get_location()
        if loc:
            return f"Lat: {loc[0]:.6f}, Lon: {loc[1]:.6f}"
        return "GPS fix not available"

    def close(self):
        self.serial_conn.close()
