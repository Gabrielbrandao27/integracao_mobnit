import math

DIST_TOLERANCE = 0.002 # km

def distance_between_coordinates(lat1, lon1, lat2, lon2):
    earthRadiusKm = 6371

    dLat = (lat2-lat1) * math.pi / 180
    dLon = (lon2-lon1) * math.pi / 180

    lat1 = (lat1) * math.pi / 180
    lat2 = (lat2) * math.pi / 180

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2) 
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
    return earthRadiusKm * c


def in_route(lat, lon, route):
    min_distance = None # minimum distance from route
    for r_coord in route:
        r_lat, r_lon = r_coord
        distance = distance_between_coordinates(lat, lon, r_lat, r_lon)
        if distance <= DIST_TOLERANCE:
            return True
        
        if min_distance is None or min_distance > distance:
            min_distance = distance
    
    return min_distance