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
    form_class = InformeForm 
    template_name = 'reports/informe_form.html'

    # def get_context_data(self,  **kwargs):
    #     context = super(InformeCreateView, self).get_context_data(**kwargs)
    #     context['satimage_pk'] = request.POST.get('satimage1')
    #     return context 

    # def form_valid(self, form):
    # #     self.object = form.save(commit=False)
    # #     self.object.user = self.fields['satimage1']
    # #     self.object.save()
    # #     return HttpResponseRedirect(self.get_success_url())
    #     satimage_selected = request.POST['satimage1']  
    #     # satimage_selected_object = SatImage.objects.get(pk=satimage_selected)     # informe.id
    #     request.session['satimage1'] = satimage_selected 
    #     return HttpResponseRedirect(self.get_success_url())
    #     # return HttpResponseRedirect(reverse_lazy('informe_detail', kwargs={'pk': informe.pk}))

    def post(self, request, *args, **kwargs):
        form = InformeForm(request.POST)
        if form.is_valid():
            informe = form.save(commit=False)
            satimage1_id = request.POST.get('satimage1')
            informe.satimage1=SatImage.objects.get(pk=satimage1_id) 
            informe.save()
            return HttpResponseRedirect(reverse_lazy('informe_detail', kwargs={'pk': informe.pk}))


    # def get(self, request, *args, **kwargs):
    #     context = {'form': InformeForm()}
    #     return render(request, 'reports/informe_form.html', context)


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

