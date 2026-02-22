from pydantic import BaseModel

class FlightInput(BaseModel):
    origin: str
    destination: str
    aircraft_type: str
    weather_factor: float = 1.0

class SimulationResult(BaseModel):
    route: list
    distance_km: float
    fuel_kg: float
    carbon_kg: float
    safety_score: int
