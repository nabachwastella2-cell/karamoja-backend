# Weather Dashboard

A beautiful, responsive weather dashboard that fetches real-time weather data from OpenWeatherMap API.

## Features

✨ **Current Weather Display**
- Real-time temperature, humidity, wind speed, and pressure
- Weather description with icons
- Min/Max temperatures
- Sunrise and sunset times
- Cloudiness and visibility

📅 **5-Day Forecast**
- Weather predictions for the next 5 days
- Hourly data with temperatures and conditions
- Visual weather icons

🔍 **City Search**
- Search for any city worldwide
- Preset quick-access cities
- Keyboard support (Enter to search)

📱 **Responsive Design**
- Beautiful gradient UI
- Works on desktop, tablet, and mobile
- Smooth animations and transitions

## Setup Instructions

### 1. Get OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Go to API keys section
4. Copy your API key

### 2. Install Dependencies

```bash
pip install -r requirements_weather.txt
```

### 3. Set Environment Variables

**Option A: Using .env file**
```bash
cp .env.example .env
# Edit .env and add your OpenWeatherMap API key
```

**Option B: Export directly**
```bash
export OPEN_WEATHER_API_KEY="your_api_key_here"
```

**Option C: On Windows (Command Prompt)**
```cmd
set OPEN_WEATHER_API_KEY=your_api_key_here
```

**Option D: On Windows (PowerShell)**
```powershell
$env:OPEN_WEATHER_API_KEY="your_api_key_here"
```

### 4. Run the Application

```bash
python weather_app.py
```

The dashboard will be available at `http://localhost:5000`

## Deployment

### Deploy to Render

1. Push to GitHub
2. Create new Web Service on [Render](https://render.com)
3. Connect your repository
4. Set environment variable:
   - Key: `OPEN_WEATHER_API_KEY`
   - Value: Your OpenWeatherMap API key
5. Deploy with this command:
   ```
   gunicorn weather_app:app
   ```

### Deploy to Heroku

1. Install Heroku CLI
2. Run:
   ```bash
   heroku login
   heroku create your-app-name
   heroku config:set OPEN_WEATHER_API_KEY="your_api_key"
   git push heroku main
   ```

## API Endpoints

### Get Current Weather
```
GET /api/weather?city=London
```

Response:
```json
{
  "city": "London",
  "country": "GB",
  "temperature": 15.5,
  "feels_like": 14.2,
  "temp_min": 13.1,
  "temp_max": 17.3,
  "humidity": 72,
  "pressure": 1013,
  "weather": "Clouds",
  "description": "overcast clouds",
  "icon": "04d",
  "wind_speed": 4.5,
  "clouds": 90,
  "visibility": 10000,
  "sunrise": "06:45:32",
  "sunset": "20:15:48"
}
```

### Get 5-Day Forecast
```
GET /api/forecast?city=London
```

### Get Multiple Cities Weather
```
POST /api/weather/multiple
Content-Type: application/json

{
  "cities": ["London", "New York", "Tokyo"]
}
```

## Files Structure

```
.
├── weather_app.py           # Main Flask application
├── templates/
│   └── index.html          # Frontend dashboard
├── requirements_weather.txt # Python dependencies
├── .env.example           # Environment variables template
├── Procfile              # Heroku/Render deployment config
└── README_WEATHER.md     # This file
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API**: OpenWeatherMap API
- **Deployment**: Render, Heroku, or any Python-capable platform

## Free vs Paid Plans

The **free plan** includes:
- Current weather for any city
- 5-day forecast
- ~1000 API calls per day
- All essential weather data

More info: [OpenWeatherMap Pricing](https://openweathermap.org/price)

## Troubleshooting

### "API key not configured"
- Make sure your API key is set in the environment variables
- Restart the application after setting the key

### "City not found"
- Check spelling of the city name
- Use city name in English
- Try with country code (e.g., "London, UK")

### No weather data loads
- Verify your OpenWeatherMap API key is valid
- Check if you've exceeded API rate limits
- Ensure internet connection is working

## License

MIT License - Feel free to use and modify!
