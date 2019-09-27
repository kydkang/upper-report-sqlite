from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Informe
from .forms import InformeForm 

class InformeListView(ListView):
    model = Informe 
    template_name = 'reports/informe_list.html'
    ### default context name is ‘object_list’. To change it, enter  context_object_name = 'informe'
    
class InformeDetailView(DetailView): 
    model = Informe    ## Or, queryset = Informe.objects.all()
    template_name = 'reports/informe_detail.html' 

from django.http import HttpResponseRedirect
class InformeCreateView(CreateView): 
    # form_class = InformeForm 
    # template_name = 'reports/informe_form.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print (context)
    #     print (self)
    #     satimage_selected = self.fields['satimage_id']
    #     satimage_selected_object = SatImage.objects.get(pk=satimage_selected) 
    #     context['satimage_object'] = satimage_selected_object
    #     return context 

    def post(self, request, *args, **kwargs):
        form = InformeForm(request.POST)
        if form.is_valid():
            informe = form.save()
            informe.save()
            satimage_selected = form.fields['satimage']
            # satimage_selected_object = SatImage.objects.get(pk=satimage_selected)     # informe.id
            return HttpResponseRedirect(reverse_lazy('informe_detail', '1', kwargs={'satimage': satimage_selected}))
        return render(request, 'reports/informe_form.html', {'form': form})


    def get(self, request, *args, **kwargs):
        context = {'form': InformeForm()}
        return render(request, 'reports/informe_form.html', context)


class InformeUpdateView(UpdateView):
    model = Informe
    fields = ['informe_code', 'event', 'fecha']
    template_name = 'reports/informe_update.html' 

class InformeDeleteView(DeleteView):
    model = Informe
    template_name = 'reports/informe_delete.html'
    success_url = reverse_lazy('informe_list')

from .models import SatImage 
from django.shortcuts import render

def load_satimages(request):
    event_id = request.GET.get('event') 
    satimages = SatImage.objects.filter(event_id=event_id).order_by('fecha')
    return render(request, 'reports/satimage_dropdown_list_options.html', {'satimages':satimages}) 

