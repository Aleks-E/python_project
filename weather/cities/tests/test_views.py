from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
# from products.views import product_detail
from cities.views import index, out
from mixer.backend.django import mixer
from django.test import TestCase, Client
import pytest
from datetime import date, timedelta



# @pytest.fixture()
# def test_data():







class Test_index_status_code(TestCase):
    def setUp(self):
        self.client = Client()


    def test_status_code(self):
        response = self.client.get('http://127.0.0.1:8000/')
        assert response.status_code == 200
        # assert response.context["a"] == 11



class Test_db_create_status_code(TestCase):
    def setUp(self):
        self.client = Client()

    def test_status_code(self):
        response = self.client.get('http://127.0.0.1:8000/db_create/')
        assert response.status_code == 302


class Test_db_clear_status_code(TestCase):
    def setUp(self):
        self.client = Client()


    def test_status_code(self):
        response = self.client.get('http://127.0.0.1:8000/db_clear/')
        assert response.status_code == 302


@pytest.mark.django_db
class Test_out_status_code(TestCase):
    def setUp(self):
        self.client = Client()


    def test_status_code(self):
        city_statistics = mixer.cycle(5).blend('cities.Cities',
                                               Name=(data for data in ('London', 'London', 'London', 'London', 'London')),
                                               Date_Time=(data for data in ('2010-01-01', '2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05')),
                                               Temperature=(data for data in (10, 20, 30, 40, 50)),
                                               Temperature_Min=(data for data in (10, 20, 30, 40, 50)),
                                               Temperature_Max=(data for data in (10, 20, 30, 40, 50)),
                                               Wind_Speed=10,
                                               Wind_Direction=10,
                                               Precipitation=10,
                                               Weather_Type='',
                                               Conditions='')



        response = self.client.get('http://127.0.0.1:8000/out/', {'year_start': '2010',
                                                                  'month_start': '1',
                                                                  'day_start': '2',
                                                                  'year_end': '2010',
                                                                  'month_end': '1',
                                                                  'day_end': '3',
                                                                  'CitySelect': 'London'})

        # assert response.context["year_start"] == '2010'
        assert response.status_code == 200
        # assert response.context["temperature_average"] == '10.0'


    def test_temperature_average(self):
        city_statistics = mixer.cycle(5).blend('cities.Cities',
                                               Name=(data for data in ('London', 'London', 'London', 'London', 'London')),
                                               Date_Time=(data for data in ('2010-01-01', '2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05')),
                                               Temperature=(data for data in (10, 20, 30, 40, 50)),
                                               Temperature_Min=(data for data in (1, 2, 3, 4, 5)),
                                               Temperature_Max=(data for data in (20, 21, 22, 23, 24)),
                                               Wind_Speed=10,
                                               Wind_Direction=10,
                                               Precipitation=10,
                                               Weather_Type='',
                                               Conditions='')

        response = self.client.get('http://127.0.0.1:8000/out/', {'year_start': '2010',
                                                                  'month_start': '1',
                                                                  'day_start': '1',
                                                                  'year_end': '2010',
                                                                  'month_end': '1',
                                                                  'day_end': '2',
                                                                  'CitySelect': 'London'})

        assert response.context["temperature_average"] == '15.0'


    def test_temperature_min_abs(self):
        city_statistics = mixer.cycle(5).blend('cities.Cities',
                                               Name=(data for data in ('London', 'London', 'London', 'London', 'London')),
                                               Date_Time=(data for data in ('2010-01-01', '2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05')),
                                               Temperature=(data for data in (10, 20, 30, 40, 50)),
                                               Temperature_Min=(data for data in (1, 2, 3, 4, 5)),
                                               Temperature_Max=(data for data in (20, 21, 22, 23, 24)),
                                               Wind_Speed=10,
                                               Wind_Direction=10,
                                               Precipitation=10,
                                               Weather_Type='',
                                               Conditions='')

        response = self.client.get('http://127.0.0.1:8000/out/', {'year_start': '2010',
                                                                  'month_start': '1',
                                                                  'day_start': '1',
                                                                  'year_end': '2010',
                                                                  'month_end': '1',
                                                                  'day_end': '2',
                                                                  'CitySelect': 'London'})

        assert response.context["temperature_min_abs"] == 1.0


    def test_temperature_max_abs(self):
        city_statistics = mixer.cycle(5).blend('cities.Cities',
                                               Name=(data for data in ('London', 'London', 'London', 'London', 'London')),
                                               Date_Time=(data for data in ('2010-01-01', '2010-01-02', '2010-01-03', '2010-01-04', '2010-01-05')),
                                               Temperature=(data for data in (10, 20, 30, 40, 50)),
                                               Temperature_Min=(data for data in (1, 2, 3, 4, 5)),
                                               Temperature_Max=(data for data in (20, 21, 22, 23, 24)),
                                               Wind_Speed=10,
                                               Wind_Direction=10,
                                               Precipitation=10,
                                               Weather_Type='',
                                               Conditions='')

        response = self.client.get('http://127.0.0.1:8000/out/', {'year_start': '2010',
                                                                  'month_start': '1',
                                                                  'day_start': '1',
                                                                  'year_end': '2010',
                                                                  'month_end': '1',
                                                                  'day_end': '2',
                                                                  'CitySelect': 'London'})

        assert response.context["temperature_max_abs"] == 21.0


    def test_temperature_min_avg(self):
        city_statistics = mixer.cycle(730).blend('cities.Cities',
                                               Name="London",
                                               Date_Time=(str(date(year=2010, month=1, day=1) + timedelta(days=day)) for day in range(735)),
                                               Temperature=1,
                                               Temperature_Min=(i for i in range(10) for j in range(73)),
                                               Temperature_Max=(i for i in range(10, 20) for j in range(73)),
                                               Wind_Speed=10,
                                               Wind_Direction=10,
                                               Precipitation=10,
                                               Weather_Type='',
                                               Conditions='')

        response = self.client.get('http://127.0.0.1:8000/out/', {'year_start': '2010',
                                                                  'month_start': '1',
                                                                  'day_start': '1',
                                                                  'year_end': '2012',
                                                                  'month_end': '1',
                                                                  'day_end': '1',
                                                                  'CitySelect': 'London'})

        assert response.context["temperature_year_statistics_list"] == [[2010, '2.0', '12.0'], [2011, '7.0', '17.0']]


    def test_precipitation_ratio(self):
        city_statistics = mixer.cycle(3).blend('cities.Cities',
                                                   Name=(data for data in
                                                         ('London', 'London', 'London')),
                                                   Date_Time=(data for data in ('2010-01-01', '2010-01-02', '2010-01-03')),
                                                   Temperature=1,
                                                   Temperature_Min=1,
                                                   Temperature_Max=1,
                                                   Wind_Speed=10,
                                                   Wind_Direction=10,
                                                   Precipitation=(data for data in (1, 1, 0)),
                                                   Weather_Type='',
                                                   Conditions='')

        response = self.client.get('http://127.0.0.1:8000/out/', {'year_start': '2010',
                                                                      'month_start': '1',
                                                                      'day_start': '1',
                                                                      'year_end': '2010',
                                                                      'month_end': '1',
                                                                      'day_end': '3',
                                                                      'CitySelect': 'London'})

        assert response.context["precipitation_ratio"] == '66.7'





































# ------------------------------------------------------

# @pytest.mark.django_db
# class Test_1(TestCase):
#     # def test_1(self):
#     #     path = reverse('index')
#
#     def setUp(self):
#         # Every test needs a client.
#         self.client = Client()
#
#
#     #     # request = self.factory.get(path)
#     #     request = self.get(path)
#     #     response = index(request)
#     #     assert response.status_code == 200
#
#     def test_1(self):
#         # path = reverse('index')
#         # request = self.ge
#         # response = index(request)
#         # response = self.client.get('http://127.0.0.1:8000/out')     # assert 301 == 200
#         response = self.client.get('http://127.0.0.1:8000/out/')  # assert 301 == 200
#
#
#         assert response.status_code == 200      # Тест прошел
#         # assert response.context["Temperature_average"] == ''
#
#
#
#
#
#         # q = Client()
#         # response = q.post('127.0.0.1:8000/out')
#         # assert response.status_code == 404
#         # assert response.content == 1
#         # assert response.template == 1
#         # assert response.context == 1
#
#
#
#         # response = self.client.get('127.0.0.1:8000')
#         # self.assertEqual(response.status_code, 404)
#         # self.assertEqual(response.status_code, 200)
#         # assert response.status_code == 404
#         # assert response.templates == 1
#
#
#     #     response.





# @pytest.mark.django_db
# class TestViews(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         super(TestViews, cls).setUpClass()
#         mixer.blend('products.Product')
#         cls.factory = RequestFactory()
#
#     def test_product_detail_authenticated(self):
#
#         path = reverse('detail', kwargs={'pk': 1})
#         request = self.factory.get(path)
#         request.user = mixer.blend(User)
#
#         response = product_detail(request, pk=1)
#         assert response.status_code == 200
#
#     def test_product_detail_unauthenticated(self):
#
#         path = reverse('detail', kwargs={'pk': 1})
#         request = self.factory.get(path)
#         request.user = AnonymousUser()
#
#         response = product_detail(request, pk=1)
#         assert 'accounts/login' in response.url














