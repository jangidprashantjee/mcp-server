MCP Server weather api
Deployed on render 
https://mcp-server-r967.onrender.com/listTools
Response
{
    "tools": [
        {
            "name": "get_weather_by_location_name",
            "description": "Get current weather by location name",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string"
                    }
                },
                "required": [
                    "location"
              ]
            }
        }
    ]
}

https://mcp-server-r967.onrender.com/callTool
payload
{
  "name": "get_weather_by_location_name",
  "arguments": {
    "location": "Sector 126 Noida"
  }
}

Response
{
    "result": {
        "latitude": 28.5,
        "longitude": 77.375,
        "generationtime_ms": 0.049948692321777344,
        "utc_offset_seconds": 19800,
        "timezone": "Asia/Kolkata",
        "timezone_abbreviation": "GMT+5:30",
        "elevation": 204.0,
        "current_weather_units": {
            "time": "iso8601",
            "interval": "seconds",
            "temperature": "°C",
            "windspeed": "km/h",
            "winddirection": "°",
            "is_day": "",
            "weathercode": "wmo code"
        },
        "current_weather": {
            "time": "2025-08-09T00:00",
            "interval": 900,
            "temperature": 27.9,
            "windspeed": 8.3,
            "winddirection": 88,
            "is_day": 0,
            "weathercode": 80
        }
    }
}
