from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import AddressViewSet, calculate_distance, google_places_autocomplete, get_place_details

router = DefaultRouter()
router.register(r'addresses', AddressViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/get-place-details/', get_place_details, name='get_place_details'),
    path('api/places-autocomplete/', google_places_autocomplete, name='places_autocomplete'),
    path('api/calculate-distance/', calculate_distance, name='calculate_distance'),
]
