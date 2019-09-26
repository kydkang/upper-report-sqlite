from django import forms
from .models import Informe, SatImage

class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = '__all__'
        # template_name = 'reports/informe_form.html' 

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['satimage'].queryset=SatImage.objects.none()
