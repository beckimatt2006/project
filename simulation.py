import math

def haversine(latitude1, longitude1, latitude2, longitude2):
    R = 6371
    d_lat = math.radians(latitude2 - latitude1)
    d_lon = math.radians(longitude2 - longitude1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(latitude1)) * \
        math.cos(math.radians(latitude2)) * math.sin(d_lon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def simulate_route(origin, destination, aircraft, weather):
    latitude1, longitude1 = origin
    latitude2, longitude2 = destination

    distance = haversine(latitude1, longitude1, latitude2, longitude2)
    fuel = distance * aircraft["fuel_burn"] * weather
    carbon = fuel * 3.16

    safety = max(60, 100 - int(weather * 12))

    return {
        "distance_km": round(distance, 2),
        "fuel_kg": round(fuel, 2),
        "carbon_kg": round(carbon, 2),
        "safety_score": safety
    }
def simulate_route_multi(points, aircraft, weather):
    total_distance = 0.0
    for i in range(len(points) - 1):
        latitude1, longitude1 = points[i]
        latitude2, longitude2 = points[i + 1]
        total_distance += haversine(latitude1, longitude1, latitude2, longitude2)

    fuel = total_distance * aircraft["fuel_burn"] * weather
    carbon = fuel * 3.16
    safety = max(60, 100 - int(weather * 12))
    return {
        "distance_km": round(total_distance, 2),
        "fuel_kg": round(fuel, 2),
        "carbon_kg": round(carbon, 2),
        "safety_score": safety
    }
