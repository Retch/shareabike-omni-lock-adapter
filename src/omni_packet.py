import datetime

from construct import (
    Adapter,
    Const,
    FixedSized,
    GreedyString,
    MappingError,
    NullTerminated,
    Struct,
)


class CommaTerminated(NullTerminated):
    def __init__(self, subcon, require=True):
        super(CommaTerminated, self).__init__(
            subcon, term=b",", include=False, consume=True, require=require
        )


class DateTimeAdapter(Adapter):
    def _decode(self, obj, context, path):
        if obj.year == "00" and obj.month == "00" and obj.day == "00":
            return None
        century = datetime.datetime.now().year // 100
        year = century * 100 + int(obj.year)
        return datetime.datetime(
            year,
            int(obj.month),
            int(obj.day),
            hour=int(obj.hour),
            minute=int(obj.minute),
            second=int(obj.second),
        )

    def _encode(self, obj, context, path):
        if not isinstance(obj, datetime.datetime):
            raise MappingError("cannot convert %r into datetime" % (obj,))
        d = dict(
            year=str(obj.year)[2:],
            month=str(obj.month),
            day=str(obj.day),
            hour=str(obj.hour),
            minute=str(obj.minute),
            second=str(obj.second),
        )
        for k in d:
            if len(d[k]) == 1:
                d[k] = f"0{d[k]}"
        return d


class Command:
    dt = Struct(
        "year" / FixedSized(2, GreedyString("ascii")),
        "month" / FixedSized(2, GreedyString("ascii")),
        "day" / FixedSized(2, GreedyString("ascii")),
        "hour" / FixedSized(2, GreedyString("ascii")),
        "minute" / FixedSized(2, GreedyString("ascii")),
        "second" / FixedSized(2, GreedyString("ascii")),
    )

    def __init__(self):
        self.protocol = Struct(
            Const(b"\xFF\xFF*CMDS,"),
            "devicecode" / CommaTerminated(GreedyString("ascii")),
            "imei" / CommaTerminated(GreedyString("ascii")),
            "datetime" / CommaTerminated(DateTimeAdapter(self.dt)),
            "cmd" / NullTerminated(GreedyString("ascii"), term=b"#"),
        )

    def build(self, packetdata):
        return self.protocol.build(packetdata)


class Response:
    dt = Struct(
        "year" / FixedSized(2, GreedyString("ascii")),
        "month" / FixedSized(2, GreedyString("ascii")),
        "day" / FixedSized(2, GreedyString("ascii")),
        "hour" / FixedSized(2, GreedyString("ascii")),
        "minute" / FixedSized(2, GreedyString("ascii")),
        "second" / FixedSized(2, GreedyString("ascii")),
    )

    def __init__(self):
        self.protocol = Struct(
            Const(b"\xFF\xFF*CMDS,"),
            "devicecode" / CommaTerminated(GreedyString("ascii")),
            "imei" / CommaTerminated(GreedyString("ascii")),
            "datetime" / CommaTerminated(DateTimeAdapter(self.dt)),
            Const(b"Re"),
            Const(b","),
            "data" / NullTerminated(GreedyString("ascii"), term=b"#"),
        )

    def build(self, packetdata):
        return self.protocol.build(packetdata)
