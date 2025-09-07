# Setup API Keys and Environment Variables for Smart Crop Advisory

To ensure all features work correctly, you need to configure the required API keys and environment variables.

## Required API Keys

1. **OpenWeatherMap API Key**
   - Used for Weather Forecast feature.
   - Sign up at https://openweathermap.org/api to get a free API key.

## How to Configure

1. Create a `.env` file in the project root (if not already present).
2. Add the following lines with your actual API keys and database credentials:

```
WEATHER_API_KEY=your_openweathermap_api_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_db_password
DB_NAME=smartcrop
```

3. Save the `.env` file.

## Notes

- Make sure the `.env` file is included in `.gitignore` to avoid committing sensitive information.
- Restart the Flask application after updating `.env` to load new environment variables.

If you want, I can help you automate or verify this setup.
