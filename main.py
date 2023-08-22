from datetime import datetime, timezone

from klein import Klein
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols.basic import LineReceiver
from twisted.web.server import Site

from omni_packet import Command, Response
from receive_packets import Q0Packet, W0Packet, D0Packet, H0Packet, L0Packet, L1Packet, S5Packet, S8Packet, M0Packet, U0Packet

lock_not_connected_message = "No packet received from lock since program is running"
http = Klein()
known_locks = dict()


class OmniProtocol(LineReceiver):
    def __init__(self):
        self.command = Command()
        self.response = Response()
        self.manufacturer_code = ""  # will be "OM" for OmniLocks
        self.imei = ""

    def dataReceived(self, data):
        decoded = data.decode('utf-8').split("#")[0]
        data_array = decoded.split(",")
        if data_array[0] == "*CMDR":
            known_locks[data_array[2]] = self
            self.manufacturer_code = data_array[1]
            self.imei = data_array[2]
            command = data_array[4]
            if command == "Q0":
                packet = Q0Packet(data_array)
            elif command == "H0":
                packet = H0Packet(data_array)
            elif command == "S8":
                packet = S8Packet(data_array)
            elif command == "M0":
                packet = M0Packet(data_array)
            elif command == "S5":
                packet = S5Packet(data_array)
            elif command == "U0":
                packet = U0Packet(data_array)
            elif command == "W0":
                packet = W0Packet(data_array)
                self.send_basic_response(command)
            elif command == "D0":
                packet = D0Packet(data_array)
                self.send_basic_response(command)
            elif command == "L1":
                packet = L1Packet(data_array)
                self.send_basic_response(command)
            elif command == "L0":
                packet = L0Packet(data_array)
                self.send_basic_response(command)
            else:
                packet = "Lock command " + command + " not implemented"
                print(data_array)
            print(packet)
        else:
            print("Unknown data received: " + data_array[0])

    def write(self, data):
        self.transport.write(data)

    def send_basic_response(self, command):
        print("Sending response for command " + command + "\n")
        resp = self.response.build(
            dict(
                devicecode=self.manufacturer_code,
                imei=self.imei,
                datetime=datetime.now(),
                data=command,
            )
        )
        self.write(resp)

    def send_request_position(self):
        resp = self.command.build(
            dict(
                devicecode=self.manufacturer_code,
                imei=self.imei,
                datetime=datetime.now(),
                cmd="D0",
            )
        )
        self.write(resp)

    def send_request_info(self):
        resp = self.command.build(
            dict(
                devicecode=self.manufacturer_code,
                imei=self.imei,
                datetime=datetime.now(),
                cmd="S5",
            )
        )
        self.write(resp)

    def send_request_unlock(self):
        ts = datetime.now(tz=timezone.utc).timestamp()
        user = 0
        cmd = self.command.build(
            dict(
                devicecode=self.manufacturer_code,
                imei=self.imei,
                datetime=datetime.now(),
                cmd=f"L0,0,{user},{ts}",
            )
        )
        self.write(cmd)

    def send_request_ring(self, amount):
        ts = datetime.now(tz=timezone.utc).timestamp()
        cmd = self.command.build(
            dict(
                devicecode=self.manufacturer_code,
                imei=self.imei,
                datetime=datetime.now(),
                cmd=f"S8,{amount},0",
            )
        )
        self.write(cmd)


class OmniFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return OmniProtocol()


# Only checks whether the lock has at least contacted this program once. In this case, commands can be sent to the lock
@http.route("/<device_id>", methods=["GET"])
def lock_exist(request, device_id):
    print("Request if lock is connected to adapter IMEI: %s\n" % (device_id,))
    lock = known_locks.get(device_id)
    if lock is None:
        print(lock_not_connected_message + "\n")
        request.setResponseCode(502)
        return lock_not_connected_message.encode("utf-8")
    else:
        request.setResponseCode(200)
        return "Lock connected".encode("utf-8")


@http.route("/<device_id>/unlock", methods=["GET"])
def lock_unlock(request, device_id):
    print("Request unlock of IMEI: %s\n" % (device_id,))
    lock = known_locks.get(device_id)
    if lock is None:
        print(lock_not_connected_message + "\n")
        request.setResponseCode(502)
        return lock_not_connected_message.encode("utf-8")
    else:
        lock.send_request_unlock()
        request.setResponseCode(200)
        return b''


@http.route("/<device_id>/position", methods=["GET"])
def lock_position(request, device_id):
    print("Request position of IMEI: %s\n" % (device_id,))
    lock = known_locks.get(device_id)
    if lock is None:
        print(lock_not_connected_message + "\n")
        request.setResponseCode(502)
        return lock_not_connected_message.encode("utf-8")
    else:
        lock.send_request_position()
        request.setResponseCode(200)
        return b''


@http.route("/<device_id>/info", methods=["GET"])
def lock_info(request, device_id):
    print("Request info of IMEI: %s\n" % (device_id,))
    lock = known_locks.get(device_id)
    if lock is None:
        print(lock_not_connected_message + "\n")
        request.setResponseCode(502)
        return lock_not_connected_message.encode("utf-8")
    else:
        lock.send_request_info()
        request.setResponseCode(200)
        return b''


@http.route("/<device_id>/ring/<amount>", methods=["GET"])     # amount is 0-255
def lock_ring(request, device_id, amount):
    print("Request ring beep from IMEI: %s\n" % (device_id,))
    lock = known_locks.get(device_id)
    if lock is None:
        print(lock_not_connected_message + "\n")
        request.setResponseCode(502)
        return lock_not_connected_message.encode("utf-8")
    else:
        lock.send_request_ring(amount)
        request.setResponseCode(200)
        return b''


omniendpoint = endpoints.TCP4ServerEndpoint(reactor, 9679)
omniendpoint.listen(OmniFactory())
httpendpoint = endpoints.TCP4ServerEndpoint(reactor, 8079)
httpendpoint.listen(Site(http.resource()))

print("Listening for lock and http traffic\n")

reactor.run()
