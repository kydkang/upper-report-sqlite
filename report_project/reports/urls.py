from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.InformeListView.as_view(), name='informe_list'),
    path('informe/<int:pk>/', views.InformeDetailView.as_view(), name='informe_detail'),
    path('informe/create/', views.InformeCreateView.as_view(), name='informe_create'), 
    path('informe/<int:pk>/update/', views.InformeUpdateView.as_view(), name='informe_update'),
    path('informe/<int:pk>/delete/', views.InformeDeleteView.as_view(), name='informe_delete'), 
    
]
