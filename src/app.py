from flask import Flask, render_template, request

from datetime import datetime, timedelta
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    ## obtain data
    next_2_hours_forecast = requests.get("https://api.data.gov.sg/v1/environment/2-hour-weather-forecast").json()
    # this provides info for each location in sg (forecast only)
    today_forecast = requests.get("https://api.data.gov.sg/v1/environment/24-hour-weather-forecast").json()
    # this provides info for the whole day of sg (forecast, humidity, temp, wind direction and speed) and forecasts for each region of sg every 6h starting from 00:00
    next_4_days_forecast = requests.get("https://api.data.gov.sg/v1/environment/4-day-weather-forecast").json()
    # this provides info for the NEXT 4 days for the whole day of sg (forecast, humidity, temp, wind direction and speed)

    ## today_day
    today_day_name = datetime.now().strftime("%A")  # today's day name

    ## today_month_date
    month = datetime.now().month
    datetime_obj = datetime.strptime(str(month), "%m")
    today_month_name = datetime_obj.strftime("%b")  # in short form

    today_day = datetime.now().day

    today_month_date = f"{today_month_name} {today_day}"

    ## future days
    future_days = []
    for i in range(1, 5):
        future_days.append((datetime.today() + timedelta(i)).strftime("%A"))

    kwargs = {
        "today_day": today_day,
        "today_month_date": today_month_date,
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
        "day5_low_temp": next_4_days_forecast['items'][0]['forecasts'][3]['temperature']['low']
    }
    
    return render_template("home.html", **kwargs)
