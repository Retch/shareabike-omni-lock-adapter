import time
from src.helper_types import LocationDM


class Packet:
    def __init__(self, data):
        self.manufacturer = data[1]
        self.imei = data[2]  # Lock unique ID number (lock communication module IMEI number (15 bits))
        self.time = data[3]  # Format yyMMddHHmmss (200318123020- > 2020-03-18 12:30:20)


class Q0Packet(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.voltage = float(data[5]) / 100

    def __str__(self):
        return "Q0 - Check-in Packet\n" + "IMEI: " + self.imei + "\nVoltage in V: " + str(self.voltage) + "\n"


class H0Packet(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.locked = bool(int(data[5]))  # 0 = unlocked, 1 = locked
        self.voltage = float(data[6]) / 100
        self.csq = int(data[7])  # Cellular Signal Quality (2-32)

    def __str__(self):
        return "H0 - Heartbeat Packet\n" + "IMEI: " + self.imei + "\nLocked: " + str(
            self.locked) + "\nVoltage in V: " + str(self.voltage) + "\n" + "CSQ: " + str(self.csq) + "\n"


class W0Packet(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.event = ""
        if data[5] == '1':
            self.event = "movement"
        elif data[5] == '2':
            self.event = "fall"  # Vehicle fell over
        elif data[5] == '6':
            self.event = "fall_recovery"  # Vehicle was put up

    def __str__(self):
        return "W0 - Alarm packet\n" + "Event: " + self.event + "\n"


class D0Packet(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.is_location_provided = False
        if data[7] == "A":  # A = valid, V = invalid
            self.is_location_provided = True
            self.dm = LocationDM(data[8], data[9], data[10], data[11])  # degrees and minutes to decimal degrees
            self.satellites = int(data[12])  # Number of satellites
            self.hdop = float(data[13])  # GPS accuracy HDOP (Horizontal Dilution of Precision)
            self.altitude = float(data[15])  # Altitude in meters

    def __str__(self):
        info = "D0 - Position packet\n"
        if self.is_location_provided:
            info += "GPS (DMS):\n" + str(self.dm) + "\n"
            info += "Altitude: " + str(self.altitude) + " m\n"
            info += "Satellites: " + str(self.satellites) + "\n"
            info += "HDOP: " + str(self.hdop) + "\n"
        else:
            info += "No location provided"
        return info + "\n"


class L1Packet(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.user_id = int(data[5])
        self.time = data[6]
        self.minutes_driven = int(data[7])

    def __str__(self):
        return "L1 - Lock report packet\n" + "User id: " + str(self.user_id) + "\nTime: " + self.time + "\nMinutes driven: " + str(self.minutes_driven) + "\n"


class S5Packet(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.voltage = float(data[5]) / 100
        self.csq = int(data[6])
        self.satellites = int(data[7])
        self.locked = bool(int(data[8]))

    def __str__(self):
        return "S5 - Lock info packet\n" + "Voltage: " + str(
            self.voltage) + "\nCSQ: " + str(self.csq) + "\nSatellites: " + str(self.satellites) + "\nLocked: " + str(
            self.locked) + "\n"


class S8Packet(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.ring_amount = int(data[5])

    def __str__(self):
        return "S8 - Ringing packet\n" + "Rings: " + str(self.ring_amount) + "\n"


class L0Packet(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.was_successful = False
        if data[5] == "0":
            self.was_successful = True
        self.user_id = int(data[6])
        self.timestamp = int(data[7])

    def __str__(self):
        return "L0 - Unlock packet\n" + "Was successful: " + str(
            self.was_successful) + "\nUser id: " + str(self.user_id) + "\nTime: " + time.ctime(self.timestamp) + "\n"


class M0Packet(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.bt_mac = data[5]

    def __str__(self):
        return "M0 - BT Mac info Packet\n" + "BT MAC Address: " + self.bt_mac


class U0Packet(Packet):
    def __init__(self, data):
        super().__init__(data)
        self.lock_sw_version = data[5]
        self.lock_hw_revision = data[6]
        self.lock_sw_date = data[7]

    def __str__(self):
        return "U0 - Version info packet\n" + "Software version: " + self.lock_sw_version + f"({self.lock_sw_date})\n" + "Hardware revision: " + self.lock_hw_revision + "\n"
