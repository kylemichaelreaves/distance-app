# views.py
from django.contrib.gis.geos import Point
from django.db import connection
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view

from .models import Address
from .models import DistanceCache
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    # TODO refactor to avoid using all() and opt for something more scalable
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


def parse_address(address_obj):
    components = address_obj['address'].split(',')
    street_address = components[0].strip()
    city = components[1].strip()
    state_zip = components[2].strip().split()
    state = state_zip[0]
    zip_code = state_zip[1]
    return street_address, city, state, zip_code


def get_or_create_address(address_data):
    street_address, city, state, zip_code = parse_address(address_data)

    address, created = Address.objects.get_or_create(
        street_address=street_address,
        city=city,
        state=state,
        zip_code=zip_code,
        defaults={
            'latitude': address_data['lat'],
            'longitude': address_data['lng'],
            'location': Point(address_data['lng'], address_data['lat'], srid=4326),
        }
    )

    if not created and (address.latitude is None or address.longitude is None):
        address.latitude = address_data['lat']
        address.longitude = address_data['lng']
        address.location = Point(address_data['lng'], address_data['lat'], srid=4326)
        address.save()

    return address


@api_view(['POST'])
def calculate_distance(request):
    data = request.data
    origin_data = data.get('origin')
    destination_data = data.get('destination')

    if not origin_data or not destination_data:
        return JsonResponse({'error': 'Both origin and destination coordinates are required.'}, status=400)

    origin_address = get_or_create_address(origin_data)
    destination_address = get_or_create_address(destination_data)

    cached_distance = DistanceCache.objects.filter(origin=origin_address, destination=destination_address).first()

    if cached_distance:
        return JsonResponse({'distance': round(cached_distance.distance, 2), 'cached': True})

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT ST_DistanceSphere(
                ST_GeomFromText(%s, 4326), 
                ST_GeomFromText(%s, 4326)
            )
            """,
            [origin_address.location.wkt, destination_address.location.wkt]
        )
        distance_meters = cursor.fetchone()[0]

    distance_miles = distance_meters / 1609.34

    DistanceCache.objects.create(origin=origin_address, destination=destination_address, distance=distance_miles)

    return JsonResponse({'distance': distance_miles, 'cached': False})
