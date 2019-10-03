from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Informe, Area, SatImage
from .forms import InformeForm, InformeUpdateForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

class InformeListView(ListView):
    model = Informe 
    template_name = 'reports/informe_list.html'
    ### default context name is ‘object_list’. To change it, enter  context_object_name = 'informe'
    
class InformeDetailView(DetailView): 
    model = Informe    ## Or, queryset = Informe.objects.all()
    template_name = 'reports/informe_detail.html' 

    def get_context_data(self, **kwargs):
        context = super(InformeDetailView, self).get_context_data(**kwargs)
        informe_selected = Informe.objects.get(id=self.kwargs['pk'])   # pk is from the url 
        areaset = Area.objects.filter(event__id=informe_selected.event.id) 
        context['areaset'] = areaset
        return context

    # # Initialize attributes shared by all view methods.
    # def setup(self, request, *args, **kwargs): 
    #     super().setup(request, *args, **kwargs)
    #     # get the Area objects using object ids passed by SESSION
    #     # this list will be sent to the template by the get_context_data() below
    #     if request.session._session:
    #         self.areas = [Area.objects.get(id=id) for id in request.session['affected_areas']] 

    # # Insert the area list  into the context dict.
    # def get_context_data(self, **kwargs):
    #     context = super(InformeDetailView, self).get_context_data(**kwargs)
    #     if request.session._session:
    #         context['areaset'] = self.areas
    #     return context

class InformeCreateView(CreateView): 
    form_class = InformeForm 
    template_name = 'reports/informe_form.html'

    # def post(self, request, *args, **kwargs):
    #     form = InformeForm(request.POST)
    #     if form.is_valid():
    #         informe = form.save(commit=False)

    #         # gets the satimage id and assign the satimage object in the form, which will be passed to InformeDetailView template
    #         # not needed because the CreateView automatically handle this.... 
    #         # satimage1_id = request.POST.get('satimage1')
    #         # satimage2_id = request.POST.get('satimage2') 
    #         # informe.satimage1=SatImage.objects.get(pk=satimage1_id) 
    #         # informe.satimage2=SatImage.objects.get(pk=satimage2_id)

    #         # gets the list of areas  (sending only the id list) << not needed because get_context_data in DetailView handles this
    #         event_id = request.POST.get('event')
    #         areaset = Area.objects.filter(event=event_id) 
    #         informe.save() 
    #         return render(request, 'reports/informe_detail.html', {'form': form, 'areaset':areaset, 'informe':informe})   
    #  
    #         Or, you can use SESSION...no good... use session only for direct and temporary delivery of value... 
    #         get the Area object ids and save them in SESSION,  then get them in InformeDetailView
    #         areas = [area.id for area in Area.objects.filter(event=event_id)] 
    #         request.session['affected_areas'] = areas
    #         informe.save()
    #         return HttpResponseRedirect(reverse_lazy('informe_detail', kwargs={'pk': informe.pk}))
    #     return render(request, 'reports/informe_form.html', {'form': form, })

    # def get(self, request, *args, **kwargs):
    #     context = {'form': InformeForm()}
    #     return render(request, 'reports/informe_form.html', context)

class InformeUpdateView(UpdateView):
    model = Informe      ## for UpdateView, this line is needed. 
    form_class = InformeUpdateForm
    template_name = 'reports/informe_update_form.html'

    # def post(self, request, *args, **kwargs):
    #     object = Informe.objects.get(pk=self.kwargs['pk'])     ## get the existing object to update 
    #     form = InformeForm(request.POST, instance=object)
    #     if form.is_valid():
    #         informe = form.save(commit=False)

    #         # gets the satimage id and assign the satimage object in the form, 
    #         # which will be passed to InformeDetailView template  << not needed, as UpdateView is handling this already.
    #         # satimage1_id = request.POST.get('satimage1')
    #         # satimage2_id = request.POST.get('satimage2') 
    #         # informe.satimage1=SatImage.objects.get(pk=satimage1_id) 
    #         # informe.satimage2=SatImage.objects.get(pk=satimage2_id)

    #         # gets the list of areas  (sending only the id list)
    #         event_id = request.POST.get('event')
    #         areaset = Area.objects.filter(event=event_id)    # areas of the event 
    #         informe.save()
    #         return render(request, 'reports/informe_detail.html', {'form': form, 'areaset':areaset, 'informe':informe})
    #         # get the Area object ids and save them in session,  then get them in InformeDetailView

    #         # Or , use SESSION...not recommended... use session only for direct and temporary delivery of value... 
    #         # areas = [area.id for area in Area.objects.filter(event=event_id)] 
    #         # request.session['affected_areas'] = areas 
    #         # informe.save()
    #         # return HttpResponseRedirect(reverse_lazy('informe_detail', kwargs={'pk': informe.pk}))
    #     return render(request, 'reports/informe_update_form.html', {'form': form})

class InformeDeleteView(DeleteView):
    model = Informe
    template_name = 'reports/informe_delete.html'
    success_url = reverse_lazy('informe_list')

def load_satimages(request):
    event_id = request.GET.get('event') 
    satimages = SatImage.objects.filter(event__id=event_id).order_by('fecha')
    return render(request, 'reports/satimage_dropdown_list_options.html', {'satimages':satimages}) 

def load_satimages1(request):
    event_id = request.GET.get('event') 
    satimage1_id = request.GET.get('satimage1')
    if satimage1_id: 
        satimage1_id = int(satimage1_id)
    satimages = SatImage.objects.filter(event__id=event_id).order_by('fecha')
    return render(request, 'reports/satimage_dropdown_list_options1.html', {'satimages':satimages, 'satimage1_id':satimage1_id }) 

def load_satimages2(request):
    event_id = request.GET.get('event') 
    satimage2_id = request.GET.get('satimage2')
    if satimage2_id: 
        satimage2_id = int(satimage2_id)
    satimages = SatImage.objects.filter(event__id=event_id).order_by('fecha')
    return render(request, 'reports/satimage_dropdown_list_options2.html', {'satimages':satimages, 'satimage2_id':satimage2_id }) 