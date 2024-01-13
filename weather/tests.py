from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

from .models import City


class CityModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name='Симферополь', latitude=55.75, longitude=37.61)

    def test_city_creation(self):
        self.assertEqual(self.city.name, 'Симферополь')
        self.assertEqual(self.city.latitude, 55.75)
        self.assertEqual(self.city.longitude, 37.61)


class WeatherViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.weather_url = reverse('weather')
        self.city = City.objects.create(name='Москва', latitude=55.751244, longitude=37.618423)


    @patch('requests.get')
    def test_weather_view(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'fact': {
                'temp': 20,
                'pressure_mm': 760,
                'wind_speed': 5,
            }
        }

        response = self.client.get(self.weather_url, {'city': self.city.name})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'city': self.city.name, 'temp': 20, 'pressure': 760, 'wind_speed': 5}
        )


    def test_weather_view_no_city(self):
        response = self.client.get(self.weather_url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'the city parameter is missing'}
        )


    @patch('requests.get')
    def test_weather_caching(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'fact': {
            'temp': 20,
            'pressure_mm': 760,
            'wind_speed': 5,
        }
    }

        response = self.client.get(self.weather_url, {'city': self.city.name})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.weather_url, {'city': self.city.name})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(mock_get.call_count, 1)


    @patch('requests.get')
    def test_weather_api_error(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 500

        response = self.client.get(self.weather_url, {'city': self.city.name})

        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'service error'}
        )