from django.urls import path
from .views import *

urlpatterns = [
    path('', ActualPrice.as_view(), name='home'),
    path('autos/', Autos.as_view(), name='autos'),
    path('spares/', Spares.as_view(), name='spares'),
    path('about/', about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('parsing/', parsing_prices, name='parsing'),
    path('spare/<slug:spare_id>/', ShowSpare.as_view(), name='spare'),
    path('add_spare/', AddSpare.as_view(), name='add_spare')
]
