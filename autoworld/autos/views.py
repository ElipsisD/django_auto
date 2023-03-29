from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView

from autos.forms import RegisterUserForm, LoginUserForm, AddSpareForm
from autos.models import Spare, Auto, Request
from autos.tasks import do_make_request
from autos.utils import DataMixin

menu = [{'title': 'Главная страница', 'url_name': 'home'},
        {'title': 'Автомобили', 'url_name': 'autos'},
        {'title': 'Запчасти', 'url_name': 'spares'},
        ]


class ActualPrice(DataMixin, ListView):
    model = Request
    template_name = 'autos/index.html'
    context_object_name = 'requests'

    def get_queryset(self):
        actual_dates = Request.objects.values('spare_id').annotate(date=Max('time_create'))
        actual_dates = [el['date'] for el in actual_dates]
        return Request.objects.filter(time_create__in=actual_dates).order_by('spare__name').select_related('spare')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return context | c_def


class Autos(DataMixin, ListView):
    model = Auto
    template_name = 'autos/autos.html'
    context_object_name = 'autos'

    def get_queryset(self):
        return Auto.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Автомобили')
        return context | c_def


class Spares(DataMixin, ListView):
    model = Spare
    template_name = 'autos/spares.html'
    context_object_name = 'spares'

    def get_queryset(self):
        return Spare.objects.all().select_related('car')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Запчасти')
        return context | c_def


class ShowSpare(DataMixin, DetailView):
    model = Spare
    template_name = 'autos/spare.html'
    slug_field = 'partnumber'
    slug_url_kwarg = 'spare_id'
    context_object_name = 'spare'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='Запчасти')
        return context | c_def


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'autos/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'autos/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class AddSpare(DataMixin, CreateView, FormView):
    form_class = AddSpareForm
    template_name = 'autos/add_spare.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Новая запчасть')
        return context | c_def


def about(request):
    return HttpResponse("О сайте")


def parsing_prices(request):
    do_make_request.delay(request.user.pk)
    return redirect('home')
