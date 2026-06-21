from mcp.server.fastmcp import FastMCP

travel_mcp = FastMCP("travel_server")

@travel_mcp.tool()
def search_flights(origin: str, destination: str, date: str) -> list:
    """Search for flights between two cities on a given date"""
    return [
        {"flight": "AT601", "departure": "08:00", "arrival": "09:15", "airline": "Atlas Blue"},
        {"flight": "AT603", "departure": "14:30", "arrival": "15:45", "airline": "Atlas Blue"},
        {"flight": "AT605", "departure": "19:00", "arrival": "20:15", "airline": "Atlas Blue"},
    ]

@travel_mcp.tool()
def get_flight_price(flight_number: str) -> dict:
    """Get the price of a flight"""
    prices = {
        "AT601": {"price": 450, "currency": "MAD"},
        "AT603": {"price": 380, "currency": "MAD"},
        "AT605": {"price": 410, "currency": "MAD"},
    }
    return prices.get(flight_number, {"price": 0, "currency": "MAD"})

if __name__ == "__main__":
    travel_mcp.run(transport="streamable-http")