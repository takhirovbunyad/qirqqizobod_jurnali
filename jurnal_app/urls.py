from django.urls import path
from . import views

app_name = 'jurnal_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('dash/', views.DashListView.as_view(), name='dash_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.dash_detail, name='dash_detail'),
    path('dash/create/', views.dash_create, name='dash_create'),
    path('maqola/create/', views.maqola_create, name='maqola_create'),
    path('maqola/' , views.MaqolaListView.as_view(), name='maqola_list'),
    path('maqola/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.MaqolaDetailView.as_view(), name='maqola_detail'),
]
