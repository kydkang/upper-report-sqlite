from django.db import models
from django.urls import reverse

class Event(models.Model): 
    dmeva_code  = models.CharField(max_length=20) 
    dmeva_fecha = models.DateField()
    mapa        = models.ImageField(upload_to='mapa/')     ### models.PolygonField(upload_to='mapa/')
    grafico     = models.ImageField(upload_to='grafico/')
    def __str__(self): 
        return self.dmeva_code  

class Informe(models.Model):
    event       = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    satimage1   = models.ForeignKey('SatImage', null=True, on_delete=models.SET_NULL, related_name='informe1', verbose_name='Imagen Satelital 1')
    satimage2   = models.ForeignKey('SatImage', null=True, on_delete=models.SET_NULL, related_name='informe2', verbose_name='Imagen Satelital 2') 
    informe_code= models.CharField(max_length=20)
    title       = models.CharField(max_length=200, verbose_name='Titulo')
    fecha       = models.DateField()
    def __str__(self): 
        return self.informe_code  
    def get_absolute_url(self):
        return reverse('informe_detail', args=[str(self.id)])


class SatImage(models.Model): 
    event       = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Evento')
    fuente      = models.CharField(max_length=50)
    banda       = models.CharField(max_length=50)
    fecha       = models.DateField()
    # antes       = models.BooleanField()
    image       = models.ImageField(upload_to='satimages', verbose_name='Imagen')  
    def __str__(self): 
        return str(self.id)  

class Area(models.Model):   
    event       = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Evento')
    location    = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name='Localización')  
    superficie  = models.DecimalField(max_digits=8, decimal_places=2)
    hectarea    = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Hectáreas')
    percentage  = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Porcentaje')

    def __str__(self): 
        return str(self.id)

class Location(models.Model):  
    location_code  = models.CharField(max_length=6, primary_key=True, verbose_name='Localización Código') 
    province    = models.CharField(max_length=50)
    canton      = models.CharField(max_length=50)
    parroquia   = models.CharField(max_length=50)
    def __str__(self): 
        return self.location_code

# class Provincia(models.Model): 
#     name        = models.CharField(max_length=30)

# class Canton(models.Model): 
#     name        = models.CharField(max_length=30)
#     provincia   = models.ForeignKey(Provincia, on_delete=models.SET_NULL) 

# class Parroquia(models.Model): 
#     name        = models.CharField(max_length=30)
#     canton      = models.ForeignKey(Canton, on_delete=models.SET_NULL) 

