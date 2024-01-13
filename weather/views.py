from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache
from django.conf import settings

import requests

from .models import City


@require_GET
def weather(request: HttpRequest) -> JsonResponse:
    city = request.GET.get('city')
    if not city:
        return JsonResponse({'error': 'the city parameter is missing'}, status=400)
    
    query = City.objects.get(name=city)
    lat = query.latitude
    lon = query.longitude

    weather_data = cache.get(city)
    cache_time = 1800
    if not weather_data:
        url = f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}'
        headers = settings.YANDEX_API_KEY
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            temp = data['fact']['temp']
            pressure = data['fact']['pressure_mm']
            wind_speed = data['fact']['wind_speed']
            
            weather_data = {
                'city': city,
                'temp': temp,
                'pressure': pressure,
                'wind_speed': wind_speed,
            }
            cache.set(city, weather_data, cache_time)
        else:
            return JsonResponse({'error': 'service error'}, status=500)
    return JsonResponse(weather_data)