from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Informe, Area
from .forms import InformeForm 
from django.http import HttpResponseRedirect

class InformeListView(ListView):
    model = Informe 
    template_name = 'reports/informe_list.html'
    ### default context name is ‘object_list’. To change it, enter  context_object_name = 'informe'
    
class InformeDetailView(DetailView): 
    model = Informe    ## Or, queryset = Informe.objects.all()
    template_name = 'reports/informe_detail.html' 

    # Initialize attributes shared by all view methods.
    def setup(self, request, *args, **kwargs): 
        super().setup(request, *args, **kwargs)
        # get the Area objects using object ids passed by session 
        # this list will be sent to the template by the get_context_data() below
        self.areas = [Area.objects.get(id=id) for id in request.session['affected_areas']] 

    # Insert the area list  into the context dict.
    def get_context_data(self, **kwargs):
        context = super(InformeDetailView, self).get_context_data(**kwargs)
        # areas = [Area.objects.get(id=id) for id in request.session['export_areas']] 
        context['areaset'] = self.areas
        return context

class InformeCreateView(CreateView): 
    form_class = InformeForm 
    template_name = 'reports/informe_form.html'

    def post(self, request, *args, **kwargs):
        form = InformeForm(request.POST)
        if form.is_valid():
            informe = form.save(commit=False)

            # gets the satimage id and assign the satimage object in the form, which will be passed to InformeDetailView template
            satimage1_id = request.POST.get('satimage1')
            satimage2_id = request.POST.get('satimage2') 
            informe.satimage1=SatImage.objects.get(pk=satimage1_id) 
            informe.satimage2=SatImage.objects.get(pk=satimage2_id)

            # gets the list of areas  (sending only the id list)
            event_id = request.POST.get('event')
            # get the Area object ids and save them in session
            areas = [area.id for area in Area.objects.filter(event=event_id)] 
            request.session['affected_areas'] = areas 

            informe.save()
            return HttpResponseRedirect(reverse_lazy('informe_detail', kwargs={'pk': informe.pk}))


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
