#Source: https://levelup.gitconnected.com/python-sun-position-for-solar-energy-and-research-7a4ead801777

import math
from datetime import datetime
import geocoder


def into_range(x, range_min, range_max):
    shiftedx = x - range_min
    delta = range_max - range_min
    return (((shiftedx % delta) + delta) % delta) + range_min

def sunpos(wann, ort, brechung):
    
    #Defintion Variablen
    jahr,monat,tag,stunde,minute,sekunde,zeitzone = wann
    latitude, longitude = ort

    rad, deg = math.radians, math.degrees
    sin, cos, tan = math.sin, math.cos, math.tan
    asin, atan2 = math.asin, math.atan2

    rlat = rad(latitude)
    rlon = rad(longitude)

    utc = stunde - zeitzone + minute /60 + sekunde / 3600

    tagAlsZahl = (
        367 * jahr
        - 7 * (jahr + (monat + 9) // 12) // 4
        + 275 * monat // 9
        + tag
        - 730531.5
        + utc / 24
    )

    #Daten der Sonne
    mean_länge = tagAlsZahl * 0.01720279239 + 4.894967873
    mean_anom = tagAlsZahl * 0.01720197034 + 6.240040768

    eclip_long = (
        mean_länge
        + 0.03342305518 * sin(mean_anom)
        + 0.0003490658504 * sin(2 * mean_anom)
    )

    #Berechnung Position
    obliquity = 0.4090877234 - 0.000000006981317008 * tagAlsZahl
    rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))
    decl = asin(sin(obliquity) * sin(eclip_long))
    sidereal = 4.894961213 + 6.300388099 * tagAlsZahl + rlon
    hour_ang = sidereal - rasc
    elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat) * cos(hour_ang))
    azimuth = atan2(
        -cos(decl) * cos(rlat) * sin(hour_ang),
        sin(decl) - sin(rlat) * sin(elevation),
    )
    azimuth = into_range(deg(azimuth), 0, 360)
    elevation = into_range(deg(elevation), -180, 180)

    if brechung:
        targ = rad((elevation + (10.3 / (elevation + 5.11))))
        elevation += (1.02 / tan(targ)) / 60

    return (round(azimuth, 2), round(elevation, 2))

if __name__ == "__main__":
# Close Encounters latitude, longitude
    ort = geocoder.ip('me')
    ort = (ort.lat, ort.lng)

#Jahr,Monat,Tag,Stunde,Minute,Sekunde,Zeitzone (CET = +1)
    zeit = datetime.now()
    wann = (zeit.year, zeit.month, zeit.day, zeit.hour, zeit.minute, zeit.second, +1)
# Funktionsaufruf zur Bestimmung der Position
    azimuth, elevation = sunpos(wann, ort, True)
# Ausgabe
    print("\nWann: "+str(zeit.day)+'.'+str(zeit.month)+'.'+str(zeit.year)+'  '+str(zeit.hour)+':'+str(zeit.minute)+':'+str(zeit.second))
    print("Wo: ", ort)
    print("Azimut: ", azimuth)
    print("Höhe: ", elevation)
