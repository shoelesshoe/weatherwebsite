from flask import Flask, render_template

from datetime import datetime, timedelta
import requests
import os

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

    ## forecast img
    if today_forecast['items'][0]['general']['forecast'] == "Thundery Showers":
        today_forecast_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thunderstorm.png')
    elif today_forecast['items'][0]['general']['forecast'] == "Partly Cloudy":
        today_forecast_path = os.path.join(app.config['UPLOAD_FOLDER'], 'partlycloudy.png')
    elif today_forecast['items'][0]['general']['forecast'] == "Sunny":  #! check if its "Sunny"
        today_forecast_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sunny.png')
    #TODO: check if theres more other forecasts

    kwargs = {
        "today_day": today_day,
        "today_month_date": today_month_date,
        "today_forecast_img": today_forecast_path,
        "today_high_temp": today_forecast['items'][0]['general']['temperature']['high'],
        "today_low_temp": today_forecast['items'][0]['general']['temperature']['low'],
        "humidity": f"{today_forecast['items'][0]['general']['relative_humidity']['low']}-{today_forecast['items'][0]['general']['relative_humidity']['high']}",
        "wind_speed": f"{today_forecast['items'][0]['general']['wind']['speed']['low']}-{today_forecast['items'][0]['general']['wind']['speed']['low']}",
        "wind_direction": today_forecast['items'][0]['general']['wind']['direction'],

        "day2": future_days[0],
        "day2_high_temp": next_4_days_forecast['items'][0]['forecasts'][0]['temperature']['high'],
        "day2_low_temp": next_4_days_forecast['items'][0]['forecasts'][0]['temperature']['low'],
        
        "day3": future_days[1],
        "day3_high_temp": next_4_days_forecast['items'][0]['forecasts'][1]['temperature']['high'],
        "day3_low_temp": next_4_days_forecast['items'][0]['forecasts'][1]['temperature']['low'],
        
        "day4": future_days[2],
        "day4_high_temp": next_4_days_forecast['items'][0]['forecasts'][2]['temperature']['high'],
        "day4_low_temp": next_4_days_forecast['items'][0]['forecasts'][2]['temperature']['low'],
        
        "day5": future_days[3],
        "day5_high_temp": next_4_days_forecast['items'][0]['forecasts'][3]['temperature']['high'],
        "day5_low_temp": next_4_days_forecast['items'][0]['forecasts'][3]['temperature']['low'],
    }
    
    return render_template("index.html", **kwargs)

if __name__ == '__main__':
    app.run(threaded=True)
