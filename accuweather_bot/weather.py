import requests
import time
from django.conf import settings


HOURS12_URL = (
    'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/'
    )
ONEDAY_URL = (
    'http://dataservice.accuweather.com/forecasts/v1/daily/1day/'
    )
LOCATION_KEY = "28580"
API_KEY = settings.API_KEY_ACCUWEATHER
CELCIUM = u'\U00002103'
RAIN = u'\U00002614'
SNOWFLAKE = u'\U00002744'


def get_weather_12h():
    """
    12 Hours of Hourly Forecasts from accuweather.com

    Returns a list of hourly forecasts for the next 12 hours
    for a specific location or string "Exception". Forecast searches
    require a location key. Please use the Locations API to obtain
    the location key for your desired location.
    By default, a truncated version of the hourly forecast data
    is returned. The full object can be obtained by passing
    "details=true" into the url string.
    """

    params = {
        'apikey': API_KEY,
        'language': 'ru',
        'metric': True
    }
    try:
        res = requests.get(f'{HOURS12_URL}{LOCATION_KEY}',
                           params=params).json()
    except ValueError:
        return "error"
    else:
        if isinstance(res, list):
            try:
                values_hour = []
                for element in res:
                    value_hour = {}
                    hours = element['DateTime']
                    hour = time.strptime(hours, '%Y-%m-%dT%H:%M:%S+03:00')

                    value_hour['date_time'] = str(hour.tm_hour) + ":00"
                    value_hour['phrase_hour'] = element['IconPhrase']
                    value_hour['temp_hour'] =\
                        str(element['Temperature']['Value']) + CELCIUM

                    if (
                        element['HasPrecipitation'] and
                        value_hour['temp_hour'].startswith('-')
                    ):
                        value_hour['precipitation_hour'] = (
                            SNOWFLAKE + " Ожидаются осадки"
                        )
                        value_hour['value_probability'] = (
                            element['PrecipitationProbability'])

                    elif element['HasPrecipitation']:
                        value_hour['precipitation_hour'] = (
                                RAIN + " Ожидаются осадки!")
                        value_hour['value_probability'] = (
                            element['PrecipitationProbability'])

                    else:
                        value_hour['precipitation_hour'] = "Без осадков"

                    values_hour.append(value_hour)

                return values_hour
            except (KeyError, TypeError):
                return "error"
        elif isinstance(res, dict):
            return "error"
        else:
            return "error"


def get_weather_1day():
    """
    1 Day of Daily Forecasts from accuweather.com.

    Returns daily forecast data for a specific location.
    Forecast searches require a location key.
    Please use the Locations API to obtain the location key
    for your desired location. By default, a truncated version
    of the hourly forecast data is returned.
    The full object can be obtained by passing
    "details=true" into the url string.
    """

    params = {
        'apikey': API_KEY,
        'language': 'ru',
        'details': True,
        'metric': True
    }

    try:
        res = requests.get(f'{ONEDAY_URL}{LOCATION_KEY}',
                           params=params).json()
    except ValueError:
        return "error"
    else:

        try:
            values_day = {}
    # weather forecast date
            date_now = res['DailyForecasts'][-1]['Date']
            today = time.strptime(date_now, '%Y-%m-%dT%H:%M:%S+03:00')
            values_day['today'] = str(today.tm_mday) + "." + str(today.tm_mon)

            values_day['d_temp'] = str(
                res['DailyForecasts'][-1]['Temperature']['Maximum']['Value']
                ) + CELCIUM

    # var may be NULL
            d_temp_real = (
                res['DailyForecasts'][-1]['RealFeelTemperature']
                ['Maximum']['Value']
                )
            if d_temp_real is not None:
                values_day['d_temp_real'] = str(d_temp_real) + CELCIUM
            else:
                values_day['d_temp_real'] = values_day['d_temp']

            values_day['d_long_phrase'] = (
                res['DailyForecasts'][-1]['Day']['LongPhrase']
                )

            values_day['n_temp'] = str(
                res['DailyForecasts'][-1]['Temperature']['Minimum']['Value']
                ) + CELCIUM

    # var may be NULL
            n_temp_real = (
                res['DailyForecasts'][-1]['RealFeelTemperature']
                ['Minimum']['Value']
                )
            if n_temp_real is not None:
                values_day['n_temp_real'] = str(n_temp_real) + CELCIUM
            else:
                values_day['n_temp_real'] = values_day['n_temp']

            values_day['n_long_phrase'] = (
                    res['DailyForecasts'][-1]['Night']['LongPhrase']
                    )

    # wind speed and gusts (m/s)
            values_day['d_wind'] = int(float(
                    res['DailyForecasts'][-1]['Day']['Wind']['Speed']['Value']
                    ) / 3.6)
            values_day['d_wind_gust'] = int(float(
                    res['DailyForecasts'][-1]['Day']
                    ['WindGust']['Speed']['Value']
                    ) / 3.6)

            values_day['n_wind'] = int(float(
                res['DailyForecasts'][-1]['Night']['Wind']['Speed']['Value']
                ) / 3.6)

            values_day['n_wind_gust'] = int(float(
                res['DailyForecasts'][-1]['Night']
                ['WindGust']['Speed']['Value']
                ) / 3.6)

    # wind direction
            values_day['d_wind_dir'] = (
                res['DailyForecasts'][-1]['Day']
                ['Wind']['Direction']['Localized']
                )

            values_day['n_wind_dir'] = (
                res['DailyForecasts'][-1]['Night']
                ['Wind']['Direction']['Localized']
                )
    # ice mm
            day_ice = res['DailyForecasts'][-1]['Day']['Ice']['Value']
            if day_ice > 0:
                values_day['d_ice'] = day_ice

            night_ice = res['DailyForecasts'][-1]['Night']['Ice']['Value']
            if night_ice > 0:
                values_day['n_ice'] = night_ice

    # rain mm
            day_rain = res['DailyForecasts'][-1]['Day']['Rain']['Value']
            if day_rain > 0:
                values_day['d_rain'] = RAIN + " " + str(day_rain)

            night_rain = res['DailyForecasts'][-1]['Night']['Rain']['Value']
            if night_rain > 0:
                values_day['n_rain'] = RAIN + " " + str(night_rain)

    # snow sm
            day_snow = res['DailyForecasts'][-1]['Day']['Snow']['Value']
            if day_snow > 0:
                values_day['d_snow'] = SNOWFLAKE + " " + str(day_snow)

            night_snow = res['DailyForecasts'][-1]['Night']['Snow']['Value']
            if night_snow > 0:
                values_day['n_snow'] = SNOWFLAKE + " " + str(night_snow)

    # day precipitation (hours)
            day_precipitation = float(
                res['DailyForecasts'][-1]['Day']['HoursOfRain']
                    ) + float(
                res["DailyForecasts"][-1]['Day']['HoursOfSnow']
                )
            if day_precipitation > 0:
                values_day['d_precipitation'] = day_precipitation

    # precipitation at night (hours)
            night_precipitation = float(
                res['DailyForecasts'][-1]['Night']['HoursOfRain']
                    ) + float(
                res['DailyForecasts'][-1]['Night']['HoursOfSnow']
                )

            if night_precipitation > 0:
                values_day['n_precipitation'] = night_precipitation

            return values_day
        except (TypeError, KeyError):
            return "error"
