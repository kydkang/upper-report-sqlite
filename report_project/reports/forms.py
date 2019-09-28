from django import forms
from .models import Informe, SatImage

class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = '__all__'
        # template_name = 'reports/informe_form.html' 

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['satimage'].widget.attrs['size']='40'
        self.fields['satimage1'].queryset=SatImage.objects.none()
        self.fields['satimage2'].queryset=SatImage.objects.none() 

        if 'event' in self.data: 
            try:
                event_id = int(self.data.get('event'))
                self.fields['satimage1'].queryset = SatImage.objects.filter(event_id=event_id).order_by('fecha')
                self.fields['satimage2'].queryset = SatImage.objects.filter(event_id=event_id).order_by('fecha')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:    # if there is an instance in the form
            self.fields['satimage1'].queryset = self.instance.event.satimage_set.order_by('fecha')
            self.fields['satimage2'].queryset = self.instance.event.satimage_set.order_by('fecha') 



