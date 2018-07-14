from datetime import datetime as dt
import datetime
import sqlite3
import configparser, os
import sys
from darksky import forecast

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/params.py'))

def send_data(conn, event_time, **kwargs):
   cur = conn.cursor()
   statement = 'INSERT INTO darksky (tdate, ttime, param, val) VALUES (date(\'now\',\'localtime\'), ?, ?, ?)'
   for key, value in kwargs.items():
     cur.execute(statement, (event_time, key, value))
   conn.commit()


def process_darksky():

    key = config['DARKSKY']['darksky_api_key']
    coord_lat = config ['OPEN_WEATHERMAP']['own_coord_lat']
    coord_long = config ['OPEN_WEATHERMAP']['own_coord_long']
    
    home_forecast = forecast(key, coord_lat, coord_long)
    for_summary = home_forecast.summary
    for_nearest_storm = home_forecast.nearestStormDistance
    for_precip_intensity = home_forecast.precipIntensity
    for_precip_probability = home_forecast.precipProbability
#    for_precip_type = home_forecast.precipType - the darkskylib doesn't seem to support this param - submitted issue
    for_temperature = home_forecast.temperature
    for_apparent_temperature = home_forecast.apparentTemperature
    for_dew_point = home_forecast.dewPoint
    for_humidity = home_forecast.humidity
    for_bar_pressure = home_forecast.pressure
    for_wind_speed = home_forecast.windSpeed
    for_wind_gust = home_forecast.windGust
    for_windBearing = home_forecast.windBearing
    for_cloud_cover = home_forecast.cloudCover
    for_uv_index = home_forecast.uvIndex
    for_visibility = home_forecast.visibility
    for_ozone = home_forecast.ozone

    print ("Ozone {0}".format(for_ozone))

    tm = dt.today()
    five_min = tm - datetime.timedelta(minutes=tm.minute % 5,
                                       seconds=tm.second,
                                       microseconds=tm.microsecond)
    event_time = str(tm.hour).rjust(2, '0') + ':' + str(five_min.minute).rjust(2, '0') + ':00'
    conn = sqlite3.connect(config['DARKSKY']['db_location'])
    send_data (conn, event_time, home_forecast = home_forecast,
      for_summary = for_summary, for_nearest_storm = for_nearest_storm,
      for_precip_intensity = for_precip_intensity,
      for_precip_probability = for_precip_probability,
      for_temperature = for_temperature,
      for_apparent_temperature = for_apparent_temperature,
      for_dew_point = for_dew_point, for_humidity = for_humidity,
      for_bar_pressure = for_bar_pressure, for_wind_speed = for_wind_speed,
      for_wind_gust = for_wind_gust, for_windBearing = for_windBearing,
      for_cloud_cover = for_cloud_cover, for_uv_index = for_uv_index,
      for_visibility = for_visibility, for_ozone = for_ozone)

if __name__ == "__main__":
    process_darksky()
