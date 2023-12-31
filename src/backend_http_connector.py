import os
import requests
from src.receive_packets import Q0Packet, W0Packet, D0Packet, H0Packet, L0Packet, L1Packet, S5Packet, S8Packet, M0Packet, U0Packet, C0Packet, I0Packet

url = os.environ.get("BACKEND_HOST_URL", "")
username = os.environ.get("BACKEND_USERNAME", "")
password = os.environ.get("BACKEND_PASSWORD", "")


def send_to_backend(packet):
    print(type(packet))
    data = {'packetType': type(packet).__name__}

    if isinstance(packet, (Q0Packet, H0Packet, S5Packet)):
        data['voltage'] = packet.voltage

    if isinstance(packet, (H0Packet, S5Packet)):
        data['isLocked'] = packet.locked
        data['csq'] = packet.csq

    if isinstance(packet, S5Packet):
        data['satellites'] = packet.satellites

    if isinstance(packet, W0Packet):
        data['event'] = packet.event

    if isinstance(packet, D0Packet):
        if packet.is_location_provided:
            data['latitudeDegrees'] = packet.dm.latitude_d
            data['longitudeDegrees'] = packet.dm.longitude_d
            data['latitudeHemisphere'] = packet.dm.latitude_hemi
            data['longitudeHemisphere'] = packet.dm.longitude_hemi
            data['altitude'] = packet.altitude
            data['satellites'] = packet.satellites
            data['hdop'] = packet.hdop
        else:
            data['noGps'] = True

    if isinstance(packet, L1Packet):
        data['isLocked'] = True
        data['minutesDriven'] = packet.minutes_driven

    if isinstance(packet, L0Packet):
        data['isLocked'] = True
        if packet.was_successful:
            data['isLocked'] = False
        data['userId'] = packet.user_id
        data['timeStamp'] = packet.timestamp

    if isinstance(packet, C0Packet):
        data['isLocked'] = packet.locked
        data['lockBikedNumber'] = packet.lock_biked_number

    if isinstance(packet, S8Packet):
        data['wasRingRequestReceived'] = True
        data['ringAmount'] = packet.ring_amount

    if isinstance(packet, M0Packet):
        data['btMac'] = packet.bt_mac

    if isinstance(packet, U0Packet):
        data['lockSwVersion'] = packet.lock_sw_version
        data['lockSwDate'] = packet.lock_sw_date
        data['lockHwRevision'] = packet.lock_hw_revision

    if isinstance(packet, I0Packet):
        data['simIccid'] = packet.sim_iccid

    response = requests.post(url + "/adapter/" + packet.imei + "/updatestatus", json=data, auth=(username, password))

    if response.status_code == 200:
        print('Package was forwarded to backend')
    else:
        print('Backend has not received package, Error ', response.status_code)
