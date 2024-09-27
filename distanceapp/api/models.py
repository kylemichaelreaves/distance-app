from django.contrib.gis.db import models

# Create your models here.
class Address(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location = models.PointField(geography=True, null=True, blank=True)


class DistanceCache(models.Model):
    origin = models.ForeignKey(Address, related_name='distance_start', on_delete=models.CASCADE)
    destination = models.ForeignKey(Address, related_name='distance_end', on_delete=models.CASCADE)
    distance = models.FloatField()

    class Meta:
        unique_together = ('origin', 'destination')

    def __str__(self):
        return f"Distance from {self.origin} to {self.destination} is {self.distance} km"