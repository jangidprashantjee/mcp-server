from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="Weather MCP Server by Location Name")

OPENMETEO_URL = "https://api.open-meteo.com/v1"


    


async def fetch_weather(latitude: float, longitude: float, forecast_date: str = None):
    if forecast_date:
        url = (
            f"{OPENMETEO_URL}/forecast?"
            f"latitude={latitude}&longitude={longitude}&"
            f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum&"
            f"timezone=auto&start_date={forecast_date}&end_date={forecast_date}"
        )
    else:
        url = f"{OPENMETEO_URL}/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&timezone=auto"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def geocode_location(location_name: str):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={location_name}"
    headers = {
        "User-Agent": "WeatherMCPDemo/1.0 (ukvhkkl@gmail.com)"  # replace with your email or website
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        results = response.json()
        if not results:
            return None
        lat = float(results[0]["lat"])
        lon = float(results[0]["lon"])
        return lat, lon


@app.post("/listTools")
async def list_tools():
    tools = [
        {
            "name": "get_weather_by_location_name",
            "description": "Get current weather by location name",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "date": {"type": "string", "format": "date"}
                },
                "required": ["location"]
            }
        }
    ]
    return {"tools": tools}

@app.post("/callTool")
async def call_tool(request: Request):
    data = await request.json()
    tool_name = data.get("name")
    arguments = data.get("arguments", {})

    if tool_name == "get_weather_by_location_name":
        location = arguments.get("location")
        date_arg = arguments.get("date")
        if not location:
            return JSONResponse(status_code=400, content={"error": "location is required"})
        coords = await geocode_location(location)
        if not coords:
            return JSONResponse(status_code=404, content={"error": "Location not found"})
        lat, lon = coords
        weather_data = await fetch_weather(lat, lon,forecast_date=date_arg)
        return {"result": weather_data}

    return JSONResponse(status_code=400, content={"error": "Unknown tool"})

@app.get("/")
async def root():
    return {"message": "Weather MCP Server running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mcp-server:app", host="0.0.0.0", port=8000, reload=True)
