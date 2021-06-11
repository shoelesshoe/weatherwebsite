from flask import Flask, render_template, request

from datetime import datetime
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    year = datetime.now().year

    month = datetime.now().month
    month = str(month).zfill(2)  # checks whether month is single digit or not and fills it with a 0 in front if it is

    date = datetime.now().day
    date = str(date).zfill(2)

    hours = datetime.now().hour
    hours = str(hours).zfill(2)

    minutes = datetime.now().minute
    minutes = str(minutes).zfill(2)

    seconds = datetime.now().second
    seconds = str(seconds).zfill(2)

    next_2_hour_forecast = requests.get(f"https://api.data.gov.sg/v1/environment/2-hour-weather-forecast?date_time={year}-{month}-{date}T{hours}-{minutes}-{seconds}").json()
    # this provides info for each location in sg (forecast only)
    today_forecast = requests.get(f"https://api.data.gov.sg/v1/environment/24-hour-weather-forecast?date_time={year}-{month}-{date}T{hours}-{minutes}-{seconds}").json()
    # this provides info for the whole day of sg (forecast, humidity, temp, wind direction and speed) and forecasts for each region of sg every 6h starting from 00:00
    next_4_days_forecast = requests.get(f"https://api.data.gov.sg/v1/environment/4-day-weather-forecast?date_time={year}-{month}-{date}T{hours}-{minutes}-{seconds}").json()
    # this provides info for the NEXT 4 days for the whole day of sg (forecast, humidity, temp, wind direction and speed)

    # kwargs = {
        # "forecast": response["items"]["general"]["forecast"]
    # }
    
    return render_template("home.html")
