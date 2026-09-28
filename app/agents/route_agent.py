import os
import pandas as pd

class RouteAgent:

    def __init__(self):
        current_file = os.path.abspath(__file__)

        project_root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(current_file)
            )
        )

        self.dataset_path = os.path.join(
            project_root,
            "app",
            "data",
            "routes.csv"
        )

        self.routes = pd.read_csv(self.dataset_path)

    def analyze_route(
        self,
        origin,
        destination,
        cargo_type,
        containers
    ):

        matching_routes = self.routes[
            (self.routes["origin"].str.lower() == origin.lower()) &
            (self.routes["destination"].str.lower() == destination.lower())
        ].copy()

        if matching_routes.empty:
            return {
                "status": "not_found",
                "message": f"No route found from {origin} to {destination}"
            }

        best_route = matching_routes.sort_values(
            "transit_days"
        ).iloc[0]

        return {
            "status": "success",
            "origin": origin,
            "destination": destination,
            "cargo_type": cargo_type,
            "containers": containers,
            "recommended_route": best_route["route_id"],
            "transit_time_days": int(best_route["transit_days"]),
            "distance_nm": int(best_route["distance_nm"]),
            "transshipments": int(best_route["transshipments"]),
            "route_type": best_route["route_type"],
            "base_freight_usd": float(best_route["base_freight_usd"]),
            "reason": "Route recommended based on shortest transit time."
        }