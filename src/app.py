from flask import Flask, render_template, request

from datetime import datetime
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

    kwargs = {
        "today_day": today_day,
        "today_month_date": today_month_date,
        "today_high_temp": today_forecast['items'][0]['general']['temperature']['high'],
        "today_low_temp": today_forecast['items'][0]['general']['temperature']['low'],
        
    }
    
    return render_template("home.html", **kwargs)
