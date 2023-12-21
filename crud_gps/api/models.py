from django.db import models

# Create your models here.
#Creación del modelo ORM para la tabla Posición en la BD
class Posicion(models.Model):
    imei=models.CharField(max_length=20)
    lat=models.FloatField()
    lon=models.FloatField()
    alt=models.FloatField()
    speed=models.FloatField()
    orientation=models.FloatField()
    acc=models.IntegerField()
    dil=models.IntegerField()
    towing=models.IntegerField()
    
    def __str__(self):
        return f'Pocision #{self.id} - IMEI: {self.imei}'

    class Meta:
        verbose_name='Posicion'
        verbose_name_plural='Posciones'
        db_table='posicion'    
    