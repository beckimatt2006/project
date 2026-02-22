from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from models import FlightInput
from database import load_airports
from simulation import simulate_route_multi
from optimizer import choose_best_route
from visualization import plot_flight_metrics

app = FastAPI(title="Flight Optimization API")
airports = load_airports()

AIRCRAFT = {
    "A320": {"fuel_burn": 2.5},
    "B777": {"fuel_burn": 6.8},
    "A380": {"fuel_burn": 9.2},
}

@app.post("/api/optimize")
def optimize(data: FlightInput):
    origin_code = data.origin.upper().strip()
    dest_code = data.destination.upper().strip()
    aircraft_type = data.aircraft_type.upper().strip()

    origin = airports.get(origin_code)
    dest = airports.get(dest_code)
    if not origin or not dest:
        raise HTTPException(status_code=400, detail="Invalid airport code")

    aircraft = AIRCRAFT.get(aircraft_type)
    if not aircraft:
        raise HTTPException(status_code=400, detail="Invalid aircraft type")

    weather = float(data.weather_factor)
    
    candidates = []
    
    direct_metrics = simulate_route_multi([origin, dest], aircraft, weather)
    candidates.append({
        "route": [origin_code, dest_code],
        **direct_metrics
    })
    
    for stop_code, stop_coord in airports.items():
        if stop_code in (origin_code, dest_code):
            continue

        metrics = simulate_route_multi([origin, stop_coord, dest], aircraft, weather)
        candidates.append({
            "route": [origin_code, stop_code, dest_code],
            **metrics
        })

    best = choose_best_route(candidates)

   
    graph_path = plot_flight_metrics(
        best["distance_km"], best["fuel_kg"], best["carbon_kg"], best["safety_score"]
    )

    route_coords = []
    for code in best["route"]:
        latitude, longitude = airports[code]
        route_coords.append({"code": code, "latitude": latitude, "longitude": longitude})

    return {
        "best": best,
        "candidates_count": len(candidates),
        "route_coords": route_coords,
        "graph": graph_path.replace("\\", "/").replace("frontend/", "")  # "metrics.png"
    }

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")