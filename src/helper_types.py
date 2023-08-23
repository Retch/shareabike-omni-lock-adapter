class LocationDM:
    def __init__(self, lat_ddmmmmmm, lat_hemi, lon_dddmmmmmm, lon_hemi):
        self.latitude_hemi = "N"
        self.longitude_hemi = "E"
        if lat_hemi == "S":
            self.latitude_hemi = "S"
        if lon_hemi == "W":
            self.longitude_hemi = "W"
        lat_dd = int(lat_ddmmmmmm[0:2])
        lon_ddd = int(lon_dddmmmmmm[0:3])
        lat_mmmmmm = float(lat_ddmmmmmm[2:])
        lon_mmmmmm = float(lon_dddmmmmmm[3:])
        self.latitude_d = lat_dd + round((lat_mmmmmm / 60), 7)
        self.longitude_d = lon_ddd + round((lon_mmmmmm / 60), 7)

    def __str__(self):
        return "Latitude: " + str(self.latitude_d) + " " + self.latitude_hemi + "\n" + "Longitude: " + str(self.longitude_d) + " " + self.longitude_hemi
