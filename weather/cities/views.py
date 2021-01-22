from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse

from .models import Cities

import csv
from datetime import date

from math import sin, cos, radians, degrees, atan


def index(request):
    return render(request, "list.html")


def db_create(request):
    with open("history_data_2.csv") as data:
        reader = csv.DictReader(data, delimiter=",")

        for row in reader:
            if stop > a >= start:
                Cities.objects.create(
                    Name=row["Name"],
                    Wind_Direction=row["Wind Direction"],
                    Date_Time=row["Date time"],
                    Temperature=row["Temperature"],
                    Temperature_Min=row["Minimum Temperature"],
                    Temperature_Max=row["Maximum Temperature"],
                    Precipitation=row["Precipitation"],
                    Wind_Speed=row["Wind Speed"],
                    Weather_Type=row["Weather Type"],
                    Conditions=row["Conditions"],
                )

    return HttpResponseRedirect(reverse("index"))


def db_clear(request):
    a = Cities.objects.all()
    a.delete()
    return HttpResponseRedirect(reverse("index"))


def out(request):
    year_start = request.GET["year_start"]
    month_start = request.GET["month_start"]
    day_start = request.GET["day_start"]

    year_end = request.GET["year_end"]
    month_end = request.GET["month_end"]
    day_end = request.GET["day_end"]

    city = request.GET["CitySelect"]

    data_start = date(year=int(year_start), month=int(month_start), day=int(day_start))
    data_end = date(year=int(year_end), month=int(month_end), day=int(day_end))

    first_row = Cities.objects.filter(Date_Time__lte=data_start, Name=city)[0]

    temperature_sum = 0
    temperature_min_abs = first_row.Temperature_Min
    temperature_max_abs = first_row.Temperature_Max

    temperature_year_statistics = {}

    precipitation_days = 0

    precipitation = {
        "Light Rain": 0,
        "Drizzle": 0,
        "Light Drizzle/Rain": 0,
        "Light Snow": 0,
        "Light Rain And Snow": 0,
        "Snow": 0,
        "Rain Showers": 0,
        "Precipitation In Vicinity": 0,
        "Heavy Rain": 0,
        "Heavy Drizzle/Rain": 0,
        "Heavy Drizzle": 0,
        "Heavy Rain And Snow": 0,
        "Heavy Freezing Rain": 0,
        "Light Freezing Drizzle/Freezing Rain": 0,
        "Freezing Drizzle/Freezing Rain": 0,
        "Light Freezing Rain": 0,
        "Heavy Snow": 0,
        "Squalls": 0,
        "Snow And Rain Showers": 0,
        "Snow Showers": 0,
        "Diamond Dust": 0,
        "Blowing Or Drifting Snow": 0,
        "Hail Showers": 0,
        "Duststorm": 0,
    }

    conditions = 0
    wind_speed_sum = 0
    wind_direction_x_sum = 0
    wind_direction_y_sum = 0

    for row in Cities.objects.filter(
        Date_Time__range=[data_start, data_end], Name=city
    ):
        temperature_sum += row.Temperature

        if temperature_min_abs > row.Temperature_Min:
            temperature_min_abs = row.Temperature_Min
        if temperature_max_abs < row.Temperature_Max:
            temperature_max_abs = row.Temperature_Max

        if row.Precipitation > 0:
            precipitation_days += 1

        for precipitation_Type in precipitation:
            if precipitation_Type in row.Weather_Type:
                precipitation[precipitation_Type] += 1

        if "Rain" in row.Conditions:
            conditions += 1

        wind_speed_sum += row.Wind_Speed

        wind_direction_x_sum += sin(radians(row.Wind_Direction))
        wind_direction_y_sum += cos(radians(row.Wind_Direction))

    temperature_average = temperature_sum / ((data_end - data_start).days + 1)
    precipitation_ratio = precipitation_days / ((data_end - data_start).days + 1) * 100

    data_delta = (data_end - data_start).days
    temperature_year_statistics_list = []

    precipitation_list = list(precipitation.items())
    precipitation_list.sort(key=lambda i: i[1], reverse=True)

    if precipitation_list[0][1] == 0 and conditions > 0:
        precipitation_list = [precipitation_list[1], ("Rain", conditions)]
    elif precipitation_list[1][1] == 0 and conditions > 0:
        precipitation_list = [precipitation_list[0], ("Rain", conditions)]
    elif (
        precipitation_list[0][1] == 0
        and precipitation_list[1][1] == 0
        and conditions > 0
    ):
        precipitation_list = [("Rain", conditions)]
    elif (
        precipitation_list[0][1] == 0
        and precipitation_list[1][1] == 0
        and conditions == 0
    ):
        precipitation_list = [("No precipitation", conditions)]

    wind_speed_average = wind_speed_sum / ((data_end - data_start).days + 1)

    wind_direction_x_avg = wind_direction_x_sum / ((data_end - data_start).days + 1)
    wind_direction_y_avg = wind_direction_y_sum / ((data_end - data_start).days + 1)
    wind_direction_avg = degrees(atan(wind_direction_x_avg / wind_direction_y_avg))

    if data_delta >= 730:
        for row in Cities.objects.filter(
            Date_Time__range=[data_start, data_end], Name=city
        ):
            if row.Date_Time.year not in temperature_year_statistics:
                temperature_year_statistics[row.Date_Time.year] = [
                    row.Temperature_Min,
                    row.Temperature_Max,
                ]
            else:
                temperature_year_statistics[row.Date_Time.year][
                    0
                ] += row.Temperature_Min
                temperature_year_statistics[row.Date_Time.year][
                    1
                ] += row.Temperature_Max

        for year in temperature_year_statistics:
            if year == int(year_start):
                data_delta = (
                    date(year=int(year_start) + 1, month=1, day=1)
                    - date(
                        year=int(year_start), month=int(month_start), day=int(day_start)
                    )
                ).days
                temperature_min_avg = temperature_year_statistics[year][0] / data_delta
                temperature_max_avg = temperature_year_statistics[year][1] / data_delta
                temperature_year_statistics_list.append(
                    [
                        year,
                        format(temperature_min_avg, ".1f"),
                        format(temperature_max_avg, ".1f"),
                    ]
                )
            elif year == int(year_end):
                data_delta = (
                    date(year=int(year_end), month=int(month_end), day=int(day_end))
                    - date(year=int(year_end) - 1, month=12, day=31)
                ).days
                temperature_min_avg = temperature_year_statistics[year][0] / data_delta
                temperature_max_avg = temperature_year_statistics[year][1] / data_delta
                temperature_year_statistics_list.append(
                    [
                        year,
                        format(temperature_min_avg, ".1f"),
                        format(temperature_max_avg, ".1f"),
                    ]
                )
            else:
                temperature_min_avg = temperature_year_statistics[year][0] / 365
                temperature_max_avg = temperature_year_statistics[year][1] / 365
                temperature_year_statistics_list.append(
                    [
                        year,
                        format(temperature_min_avg, ".1f"),
                        format(temperature_max_avg, ".1f"),
                    ]
                )

    return render(
        request,
        "list.html",
        {
            "temperature_average": format(temperature_average, ".1f"),
            "temperature_min_abs": temperature_min_abs,
            "temperature_max_abs": temperature_max_abs,
            "temperature_year_statistics_list": temperature_year_statistics_list,
            "precipitation_ratio": format(precipitation_ratio, ".1f"),
            "precipitation_list": precipitation_list,
            "wind_speed_average": format(wind_speed_average, ".1f"),
            "wind_direction_avg": format(wind_direction_avg, ".1f"),
        },
    )
