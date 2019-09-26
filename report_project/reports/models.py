from django.db import models
from django.urls import reverse

class Event(models.Model): 
    dmeva_code  = models.CharField(max_length=20) 
    dmeva_fecha = models.DateField()
    grafico     = models.ImageField()
    mapa        = models.ImageField()
    # mapa        = models.PolygonField()
    def __str__(self): 
        return self.dmeva_code  

class Informe(models.Model):
    event       = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    satimage    = models.ManyToManyField('SatImage')
    informe_code= models.CharField(max_length=20)
    title       = models.CharField(max_length=200)
    fecha       = models.DateField()
    def __str__(self): 
        return self.informe_code  
    def get_absolute_url(self):
        return reverse('informe_detail', args=[str(self.id)])


class SatImage(models.Model):
    event       = models.ForeignKey(Event, on_delete=models.CASCADE)
    fuente      = models.CharField(max_length=50)
    banda       = models.CharField(max_length=50)
    fecha       = models.DateField()
    antes       = models.BooleanField()
    image       = models.ImageField()  
    def __str__(self): 
        return str(self.id)  

class Area(models.Model): 
    event       = models.ForeignKey(Event, on_delete=models.CASCADE)
    distrito    = models.CharField(max_length=6)  
    superficie  = models.DecimalField(max_digits=8, decimal_places=2)
    hectarea    = models.DecimalField(max_digits=8, decimal_places=2)
    percentage  = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self): 
        return str(self.id)

class Distrito(models.Model):  
    distritoID  = models.CharField(max_length=6) 
    province    = models.CharField(max_length=50)
    canton      = models.CharField(max_length=50)
    parroquia   = models.CharField(max_length=50)
    def __str__(self): 
        return self.distritoID

# class Provincia(models.Model): 
#     name        = models.CharField(max_length=30)

# class Canton(models.Model): 
#     name        = models.CharField(max_length=30)
#     provincia   = models.ForeignKey(Provincia, on_delete=models.SET_NULL) 

# class Parroquia(models.Model): 
#     name        = models.CharField(max_length=30)
#     canton      = models.ForeignKey(Canton, on_delete=models.SET_NULL) 

