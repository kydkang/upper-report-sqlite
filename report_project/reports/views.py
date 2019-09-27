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

    from django.core import serializers
    def get_initial(self):
        # initial = super(InformeCreateView, self).get_initial(**kwargs)
        area_set = serializers.deserialize("json", response.session('area_set'))
        return {
            'area_set':area_set,
        }

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

            # gets the list of areas and set it in session 
            from django.core import serializers
            event_id = request.POST.get('event')
            area_set = Area.objects.filter(event=event_id) 
            area_serialized = serializers.serialize('json', area_set)
            request.session['area_set'] = area_serialized 

            informe.save()
            return HttpResponseRedirect(reverse_lazy('informe_detail', kwargs={'pk': informe.pk}))
            # return render(request,'reports/informe_detail', {'pk': informe.pk, 'dummy': 'dummy' } )

        #  pass by session 
        #     request.session['bar'] = 'FooBar'
        #     return redirect('app:view')
        # in template, use it by: 
        # {{ request.session.bar }}


    # def get_context_data(self, **kwargs):
    #     context = super(InformeCreateView, self).get_context_data(**kwargs)
    #     context['areaset'] = Area.objects.filter(event=event.pk)
    #     return context





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

