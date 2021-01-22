from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse

from .models import Cities

import csv
from django.utils import timezone
# import datetime
from datetime import date
from decimal import Decimal

from math import sin, cos, pi, radians, degrees, asin, atan


def index(request):
    a = 11
    return render(request, 'list.html', {'a': a})


# rows 60000

def db_create(request):
    with open('history_data_2.csv') as data:
        reader = csv.DictReader(data, delimiter=',')
        a = 0
        start = 52000
        stop = 56000

        for row in reader:
            if stop > a >= start:
                Cities.objects.create(Name=row["Name"],
                                      Wind_Direction=row["Wind Direction"],
                                      Date_Time=row["Date time"],
                                      Temperature=row["Temperature"],
                                      Temperature_Min=row["Minimum Temperature"],
                                      Temperature_Max=row["Maximum Temperature"],
                                      Precipitation=row["Precipitation"],
                                      Wind_Speed=row["Wind Speed"],
                                      Weather_Type=row["Weather Type"],
                                      Conditions=row["Conditions"])

            a += 1

    return HttpResponseRedirect(reverse('index'))


def db_clear(request):
    a = Cities.objects.all()
    a.delete()
    return HttpResponseRedirect(reverse('index'))




def out(request):
    year_start = request.GET['year_start']
    month_start = request.GET['month_start']
    day_start = request.GET['day_start']

    year_end = request.GET['year_end']
    month_end = request.GET['month_end']
    day_end = request.GET['day_end']

    city = request.GET['CitySelect']

    data_start = date(year=int(year_start), month=int(month_start), day=int(day_start))
    data_end = date(year=int(year_end), month=int(month_end), day=int(day_end))

    row_counter = 0

    first_row = Cities.objects.filter(Date_Time__lte=data_start, Name=city)[0]

    temperature_sum = 0
    temperature_min_abs = first_row.Temperature_Min
    temperature_max_abs = first_row.Temperature_Max

    years = []
    temperature_year_statistics = {}
    temperature_min_avg = first_row.Temperature_Min
    temperature_max_avg = first_row.Temperature_Max

    temperature_min_sum = 0
    temperature_max_sum = 0

    precipitation_days = 0

    precipitation = {"Light Rain": 0,
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
                     "Duststorm": 0}

    for row in Cities.objects.filter(Date_Time__range=[data_start, data_end], Name=city):
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

    temperature_average = temperature_sum / ((data_end - data_start).days + 1)
    precipitation_ratio = precipitation_days / ((data_end - data_start).days + 1) * 100

    data_delta = (data_end - data_start).days
    temperature_year_statistics_list = []

    precipitation_list = list(precipitation.items())
    precipitation_list.sort(key=lambda i: i[1], reverse=True)

    if data_delta >= 730:
        for row in Cities.objects.filter(Date_Time__range=[data_start, data_end], Name=city):
            if row.Date_Time.year not in temperature_year_statistics:
                temperature_year_statistics[row.Date_Time.year] = [row.Temperature_Min, row.Temperature_Max]
            else:
                temperature_year_statistics[row.Date_Time.year][0] += row.Temperature_Min
                temperature_year_statistics[row.Date_Time.year][1] += row.Temperature_Max

        for year in temperature_year_statistics:
            if year == int(year_start):
                data_delta = (date(year=int(year_start) + 1, month=1, day=1) - date(year=int(year_start),
                                                                                    month=int(month_start),
                                                                                    day=int(day_start))).days
                temperature_min_avg = temperature_year_statistics[year][0] / data_delta
                temperature_max_avg = temperature_year_statistics[year][1] / data_delta
                temperature_year_statistics_list.append([year, format(temperature_min_avg, '.1f'), format(temperature_max_avg, '.1f')])
            elif year == int(year_end):
                data_delta = (date(year=int(year_end), month=int(month_end), day=int(day_end)) - date(
                    year=int(year_end) - 1, month=12, day=31)).days
                temperature_min_avg = temperature_year_statistics[year][0] / data_delta
                temperature_max_avg = temperature_year_statistics[year][1] / data_delta
                temperature_year_statistics_list.append(
                    [year, format(temperature_min_avg, '.1f'), format(temperature_max_avg, '.1f')])
            else:
                temperature_min_avg = temperature_year_statistics[year][0] / 365
                temperature_max_avg = temperature_year_statistics[year][1] / 365
                temperature_year_statistics_list.append(
                    [year, format(temperature_min_avg, '.1f'), format(temperature_max_avg, '.1f')])





    # for year in temperature_year_statistics:
    #     temperature_year_statistics_list.append([year, temperature_year_statistics[year][0], temperature_year_statistics[year][1]])


        # else:
        #     # temperature_year_statistics_list.append(
        #     #     [year, temperature_year_statistics[year][0], temperature_year_statistics[year][1]])
        #     temperature_year_statistics_list.append(
        #         [year_start, 2, 2])








    # if Temperature_Min > row.Temperature_Min:
    # Temperature_Min = row.Temperature_Min
    #             Statistics_by_year_dict[row.Date_Time.year][0] = Temperature_Min
    #         if Temperature_Max < row.Temperature_Max:
    #             Temperature_Max = row.Temperature_Max
    #             Statistics_by_year_dict[row.Date_Time.year][1] = Temperature_Max




    # Temperature_Min_abs = first_row.Temperature_Min
    # Temperature_Max_abs = first_row.Temperature_Max

    Wind_Speed_average_sum = 0
    Wind_direction_x_sum = 0
    Wind_direction_y_sum = 0
    Precipitation_days = 0

    Precipitation = {"Light Rain": 0,
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
                     "Duststorm": 0}

    Statistics_by_year_dict = {}
    Statistics_by_year = []

    # Precipitation_List = []






    # for row in Cities.objects.filter(Date_Time__range=[data_start, data_end], Name=city):
    #     row_counter += 1
    #     Temperature_average_sum += row.Temperature
    #
    #     if row.Date_Time.year not in Statistics_by_year_dict:
    #         Temperature_Min = row.Temperature_Min
    #         Temperature_Max = row.Temperature_Max
    #         Statistics_by_year_dict[row.Date_Time.year] = [Temperature_Min, Temperature_Max]
    #     else:
    #         if Temperature_Min > row.Temperature_Min:
    #             Temperature_Min = row.Temperature_Min
    #             Statistics_by_year_dict[row.Date_Time.year][0] = Temperature_Min
    #         if Temperature_Max < row.Temperature_Max:
    #             Temperature_Max = row.Temperature_Max
    #             Statistics_by_year_dict[row.Date_Time.year][1] = Temperature_Max
    #
    #     if row.Precipitation > 0:
    #         Precipitation_days += 1
    #
    #     for Precipitation_Type in Precipitation:
    #         if Precipitation_Type in row.Weather_Type:
    #             Precipitation[Precipitation_Type] += 1
    #
    #     Wind_Speed_average_sum += row.Wind_Speed
    #
    #     Wind_direction_x_sum += sin(radians(row.Wind_Direction))
    #     Wind_direction_y_sum += cos(radians(row.Wind_Direction))


# ------------------------




    # for Temperature in Statistics_by_year_dict:
    #     if Temperature_Min_abs > Statistics_by_year_dict[Temperature][0]:
    #         Temperature_Min_abs = Statistics_by_year_dict[Temperature][0]
    #     if Temperature_Max_abs < Statistics_by_year_dict[Temperature][1]:
    #         Temperature_Max_abs = Statistics_by_year_dict[Temperature][1]
    #
    #
    #     Statistics_by_year.append([[Temperature],
    #                                ['Temperature_Min', Statistics_by_year_dict[Temperature][0]],
    #                                ['Temperature_Max', Statistics_by_year_dict[Temperature][1]]])
    #
    #
    # if row_counter > 730:
    #     Statistics_by_year = [[['Start Period:', data_start, 'End Period:', data_end],
    #                            ['Temperature_Min_abs', Temperature_Min_abs],
    #                            ['Temperature_Max_abs', Temperature_Max_abs]],
    #                           *Statistics_by_year]
    # else:
    #     Statistics_by_year = [[['Start Period:', data_start, 'End Period:', data_end],
    #                            ['Temperature_Min_abs', Temperature_Min_abs],
    #                            ['Temperature_Max_abs', Temperature_Max_abs]]]
    #
    #
    # Precipitation_Ratio = Precipitation_days / row_counter * 100
    #
    #
    #
    # Precipitation_List = list(Precipitation.items())
    # Precipitation_List.sort(key=lambda i: i[1], reverse=True)
    # Temperature_average = Temperature_average_sum / row_counter
    # Wind_Speed_average = Wind_Speed_average_sum / row_counter
    # Wind_direction_x = Wind_direction_x_sum / row_counter
    # Wind_direction_y = Wind_direction_y_sum / row_counter
    # Wind_direction_average = degrees(atan(Wind_direction_x / Wind_direction_y))



    return render(request, 'list.html', {
                                                'temperature_average': format(temperature_average, '.1f'),
                                                'temperature_min_abs': temperature_min_abs,
                                                'temperature_max_abs': temperature_max_abs,
                                                'temperature_year_statistics_list': temperature_year_statistics_list,
                                                'precipitation_ratio': format(precipitation_ratio, '.1f'),
                                                'precipitation_list': precipitation_list





                                                 # 'Statistics_by_year': Statistics_by_year,
                                                 # 'Precipitation_Ratio': Precipitation_Ratio,
                                                 # 'Precipitation': Precipitation,
                                                 # 'Precipitation_List': Precipitation_List,
                                                 # 'Precipitation_List_1': Precipitation_List[0][0],
                                                 # 'Precipitation_List_2': Precipitation_List[1][0],


                                                 # 'Wind_Speed_average': Wind_Speed_average,
                                                 # 'Wind_direction_average': Wind_direction_average,
                                                 # 'Precipitation_days': Precipitation_days,



                                                 # 'Date_Time_list': Date_Time_list,



                                                 })










"""
    # a_1 = Cities.objects.filter(Date_Time__lte=datetime.date(year=2010, month=1, day=1))
    # a_1 = Cities.objects.filter(Date_Time__lte=datetime.date(year=year_start, month=month_start, day=day_start))

    # a_1 = Cities.objects.filter(Date_Time__lte=str(datetime.date(year=year_start, month=month_start, day=day_start)))
    # a_1 = Cities.objects.filter(Date_Time__lte='2010-01-04')

    # a_1 = Cities.objects.filter(Date_Time__date__lte=datetime.date(2010, 1, 1))

    # a_1 = Cities.objects.filter(Date_Time__range=["2010-01-01", "2010-01-04"])
    # a_1 = Cities.objects.filter(Date_Time__range=[datetime.date(2010, 1, 1), datetime.date(2010, 1, 2)])



# a = 123

    # a = Cities.objects.all()

    # a = Cities.objects.get(id=11722)

    # a = Cities.objects.filter(id=11722)
    # a = Cities.objects.filter(Name='London')
    # a = Cities.objects.filter(Date_Time='2010-01-08')

    # a = Cities.objects.filter(Name__contains='Lo')
    # a = Cities.objects.filter(id__contains='1171')
    # a = Cities.objects.filter(id__contains='718')

    # a = Cities.objects.filter(Date_Time__lte=timezone.now())

    # a = Cities.objects.filter(Date_Time__lte=datetime.datetime(year=2010, month=1, day=1))

    # a = Cities.objects.filter(Date_Time__year=2010, Date_Time__month=1, Date_Time__day=3)

    # a = Cities.objects.filter(Date_Time__gte=3)

    # 'a': a[0].Wind_Direction      #--------

    # a_1 = Cities.objects.filter(Date_Time__lte='2010-01-06')
    # a_2 = Cities.objects.filter(Date_Time__lte='2010-01-04')
    # a = list(set(a_1) - set(a_2))

    # b = request.POST['select']

    # city = request.GET['CitySelect']

    # YearStart = request.GET['YearStart']

    # YearStart = 20


"""















