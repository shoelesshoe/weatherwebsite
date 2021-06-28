from flask import Flask, render_template

from datetime import datetime, timedelta
import requests
import os

def create_app():
    app = Flask(__name__)

    FORECAST_FOLDER = os.path.join('static', 'img', 'forecast_img')
    app.config['UPLOAD_FOLDER'] = FORECAST_FOLDER

    @app.route("/")
    def index():
        ## obtain data
        today_forecast = requests.get("https://api.data.gov.sg/v1/environment/24-hour-weather-forecast").json()
        next_4_days_forecast = requests.get("https://api.data.gov.sg/v1/environment/4-day-weather-forecast").json()

        ## today_day
        today_day_name = datetime.now().strftime("%A")  # today's day full name

        ## today_month_date
        month = datetime.now().month
        datetime_obj = datetime.strptime(str(month), "%m")
        today_month_name = datetime_obj.strftime("%b")  # in short form

        today_day = datetime.now().day

        today_month_date = f"{today_month_name} {today_day}"

        ## future days
        future_days = []
        for i in range(1, 5):
            future_days.append((datetime.today() + timedelta(i)).strftime("%A"))  # future days' name in short form

        ## today_forecast_img & dayx_forecast_img
        def get_forecast_img(path):
            if "thundery showers" in path.lower():
                return os.path.join(app.config['UPLOAD_FOLDER'], 'thunderstorm.png')
            elif "showers" in path.lower():
                return os.path.join(app.config['UPLOAD_FOLDER'], 'showers.png')
            elif "partly cloudy" in path.lower():
                return os.path.join(app.config['UPLOAD_FOLDER'], 'partlycloudy.png')
            elif "cloudy" in path.lower():
                return os.path.join(app.config['UPLOAD_FOLDER'], 'cloudy.png')
            elif "sunny" in path.lower():
                return os.path.join(app.config['UPLOAD_FOLDER'], 'sunny.png')
            else:
                return os.path.join(app.config['UPLOAD_FOLDER'], 'questionmark.png')

        kwargs = {
            "today_day": today_day_name,
            "today_month_date": today_month_date,
            "today_forecast_img": get_forecast_img(today_forecast['items'][0]['general']['forecast']),
            "today_high_temp": today_forecast['items'][0]['general']['temperature']['high'],
            "today_low_temp": today_forecast['items'][0]['general']['temperature']['low'],
            "humidity": f"{today_forecast['items'][0]['general']['relative_humidity']['low']}-{today_forecast['items'][0]['general']['relative_humidity']['high']}",
            "wind_speed": f"{today_forecast['items'][0]['general']['wind']['speed']['low']}-{today_forecast['items'][0]['general']['wind']['speed']['high']}",
            "wind_direction": today_forecast['items'][0]['general']['wind']['direction'],

            "day2": future_days[0],
            "day2_high_temp": next_4_days_forecast['items'][0]['forecasts'][0]['temperature']['high'],
            "day2_low_temp": next_4_days_forecast['items'][0]['forecasts'][0]['temperature']['low'],
            "day2_forecast_img": get_forecast_img(next_4_days_forecast['items'][0]['forecasts'][0]['forecast']),
            
            "day3": future_days[1],
            "day3_high_temp": next_4_days_forecast['items'][0]['forecasts'][1]['temperature']['high'],
            "day3_low_temp": next_4_days_forecast['items'][0]['forecasts'][1]['temperature']['low'],
            "day3_forecast_img": get_forecast_img(next_4_days_forecast['items'][0]['forecasts'][1]['forecast']),
            
            "day4": future_days[2],
            "day4_high_temp": next_4_days_forecast['items'][0]['forecasts'][2]['temperature']['high'],
            "day4_low_temp": next_4_days_forecast['items'][0]['forecasts'][2]['temperature']['low'],
            "day4_forecast_img": get_forecast_img(next_4_days_forecast['items'][0]['forecasts'][2]['forecast']),
            
            "day5": future_days[3],
            "day5_high_temp": next_4_days_forecast['items'][0]['forecasts'][3]['temperature']['high'],
            "day5_low_temp": next_4_days_forecast['items'][0]['forecasts'][3]['temperature']['low'],
            "day5_forecast_img": get_forecast_img(next_4_days_forecast['items'][0]['forecasts'][3]['forecast']),
        }
        
        return render_template("index.html", **kwargs)
    
    return app
