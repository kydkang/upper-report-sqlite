from django import forms
from .models import Informe, SatImage, Event

class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        # template_name = 'reports/informe_form.html' 
        fields = ['informe_code', 'title', 'fecha', 'event', 'satimage1', 'satimage2' ]
        ### also need change as follows in settings.py to change the order to 25-Enero-2019
        ###  USE_L10N = False    DATE_FORMAT = 'd-m-Y'  LANGUAGE_CODE = 'es-EC'
        widgets = {
            'fecha': forms.SelectDateWidget
        }

        labels = {
            'event': 'Evento',
            'satimage1': 'Imagen Satelital 1', 
            'satimage2': 'Imagen Satelital 2',
            'informe_code': 'Informe Code',
            'title': 'Titulo',
            'fecha': 'Fecha',
        }
        # help_texts = {    'name': _('Some useful help text.'),      }
        # error_messages = {       'name': {   'max_length': _("This writer's name is too long."),    },  }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['satimage'].widget.attrs['size']='40'
        self.fields['satimage1'].queryset=SatImage.objects.none()
        self.fields['satimage2'].queryset=SatImage.objects.none() 
        print(self.data) 

        if 'event' in self.data:     ## handling ajax request 
            try:
                event_id = int(self.data.get('event'))
                self.fields['satimage1'].queryset = SatImage.objects.filter(event_id=event_id).order_by('fecha')
                self.fields['satimage2'].queryset = SatImage.objects.filter(event_id=event_id).order_by('fecha')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:    # if there is an form intance (to update).  satimage_set is the reverse set for SatImage
            self.fields['satimage1'].queryset = self.instance.event.satimage_set.order_by('fecha')
            self.fields['satimage2'].queryset = self.instance.event.satimage_set.order_by('fecha') 


class InformeUpdateForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = ['informe_code', 'title', 'fecha', 'event', 'satimage1', 'satimage2', 'id']
        widgets = {
            'fecha': forms.SelectDateWidget
        }

        labels = {
            'event': 'Evento',
            'satimage1': 'Imagen Satelital 1', 
            'satimage2': 'Imagen Satelital 2',
            'informe_code': 'Informe Code',
            'title': 'Titulo',
            'fecha': 'Fecha',
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['satimage1'].queryset = SatImage.objects.filter(event_id=self.instance.event.id).order_by('fecha')
        self.fields['satimage2'].queryset = SatImage.objects.filter(event__dmeva_code=self.instance.event.dmeva_code).order_by('fecha')






