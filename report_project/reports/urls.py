from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.InformeListView.as_view(), name='informe_list'),
    path('informe/<int:pk>/', views.InformeDetailView.as_view(), name='informe_detail'),
    path('informe/create/', views.InformeCreateView.as_view(), name='informe_create'), 
    path('informe/<int:pk>/update/', views.InformeUpdateView.as_view(), name='informe_update'),
    path('informe/<int:pk>/delete/', views.InformeDeleteView.as_view(), name='informe_delete'), 
    path('ajax/load-satimages/', views.load_satimages, name='ajax_load_satimages'), 
    path('ajax/load-satimages1/', views.load_satimages1, name='ajax_load_satimages1'), 
    path('ajax/load-satimages2/', views.load_satimages2, name='ajax_load_satimages2'), 
]
