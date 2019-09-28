from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Informe, Area
from .forms import InformeForm 

class InformeListView(ListView):
    model = Informe 
    template_name = 'reports/informe_list.html'
    ### default context name is ‘object_list’. To change it, enter  context_object_name = 'informe'
    
class InformeDetailView(DetailView): 
    model = Informe    ## Or, queryset = Informe.objects.all()
    template_name = 'reports/informe_detail.html' 

    def setup(self, request, *args, **kwargs): 
        super().setup(request, *args, **kwargs)
        # self.areaset = request.session['areaset']
        self.areas = [Area.objects.get(id=id) for id in request.session['export_areas']] 

    def get_context_data(self, **kwargs):
        context = super(InformeDetailView, self).get_context_data(**kwargs)
        # areas = [Area.objects.get(id=id) for id in request.session['export_areas']] 
        context['areaset'] = self.areas
        return context


from django.http import HttpResponseRedirect
class InformeCreateView(CreateView): 
    form_class = InformeForm 
    template_name = 'reports/informe_form.html'

    def post(self, request, *args, **kwargs):
        form = InformeForm(request.POST)
        if form.is_valid():
            informe = form.save(commit=False)

            # gets the satimage1
            satimage1_id = request.POST.get('satimage1')
            informe.satimage1=SatImage.objects.get(pk=satimage1_id) 

            # gets the list of areas  (sending only the id list)
            event_id = request.POST.get('event')
            areas = [area.id for area in Area.objects.filter(event=event_id)] 
            request.session['export_areas'] = areas 

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

