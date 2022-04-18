
import requests
from datetime import datetime
import time

CITY = 'Saint Petersburg,RU'
API_KEY = ''
DELTA = 86400  # 1 dqy
CURRENT_DAY = time.time()
LAT = 59.8944
LON = 30.2642
SUNSET_SUNRISE_DEL = {}
FEELS_LIKE_TEMP = {}


def get_current_weather(CITY, API_KEY):
    url = f"https://api.openweathermap.org/data/2.5/weather?q=" \
          f"{CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    cur_date = datetime.fromtimestamp(response['dt']).date().strftime('%d-%m-%Y')
    del_sun = response['sys']['sunset'] - response['sys']['sunrise']
    abs_del = abs(response['main']['feels_like'] - response['main']['temp_min'])
    SUNSET_SUNRISE_DEL[del_sun] = [cur_date]
    FEELS_LIKE_TEMP[abs_del] = [cur_date]
    return SUNSET_SUNRISE_DEL, FEELS_LIKE_TEMP


def get_weather_previous_days(LAT, LON, API_KEY):
    for i in range(1, 5):
        DAY = int(CURRENT_DAY - i * DELTA)
        url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?" \
              f"lat={LAT}&lon={LON}&dt={DAY}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        prev_day = datetime.fromtimestamp(response['current']['dt']).date().strftime('%d-%m-%Y')
        del_sun = response['current']['sunset'] - response['current']['sunrise']
        abs_del = abs(response['current']['feels_like'] - response['current']['temp'])
        SUNSET_SUNRISE_DEL[del_sun] = [prev_day]
        FEELS_LIKE_TEMP[abs_del] = [prev_day]
    return SUNSET_SUNRISE_DEL, FEELS_LIKE_TEMP


def return_results(SUNSET_SUNRISE_DEL, FEELS_LIKE_TEMP):
    sun_day = str(SUNSET_SUNRISE_DEL[max(SUNSET_SUNRISE_DEL)]).replace("['", '').replace("']", '')
    sun_time = datetime.fromtimestamp(max(SUNSET_SUNRISE_DEL)).time().strftime('%H hours, %M minutes and %S seconds')
    min_del_temp_day = str(FEELS_LIKE_TEMP[min(FEELS_LIKE_TEMP)]).replace("['", '').replace("']", '')
    min_del_temp = round(min(FEELS_LIKE_TEMP), 2)
    return f"Date, with the maximum length of daylight hours {sun_day}: {sun_time}. \n" \
           f"Date, with the minimum difference between the 'feels like' " \
           f"and actual temperature {min_del_temp_day}: {min_del_temp} ℃."


get_current_weather(CITY, API_KEY)
get_weather_previous_days(LAT, LON, API_KEY)
print(return_results(SUNSET_SUNRISE_DEL, FEELS_LIKE_TEMP))
