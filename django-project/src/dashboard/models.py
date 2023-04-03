from django.db import models

# Create your models here.
class Data(models.Model):
    team_name = models.CharField(max_length=100, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return (self.team_name + ", " + str(self.latitude) + ", " + str(self.longitude))

    class Meta:
        verbose_name_plural = "Data"