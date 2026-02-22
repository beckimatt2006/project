def choose_best_route(routes):
    return min(routes, key=lambda r: r["carbon_kg"])
