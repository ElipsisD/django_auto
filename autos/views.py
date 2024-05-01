from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView
from django.views.generic.base import TemplateView

from autos.forms import AddSpareForm, LoginUserForm, RegisterUserForm
from autos.models import Auto, Request, Spare
from autos.services.making_querysets.querysets import get_actual_prices
from autos.tasks import do_add_spare, do_make_request
from autos.utils import DataMixin


class ActualPrice(DataMixin, TemplateView):
    template_name = "autos/index.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:  # noqa: ANN001, ARG002
        requests = get_actual_prices()
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title="Главная страница",
            requests=requests
        )
        return context | c_def


class Autos(DataMixin, ListView):
    model = Auto
    template_name = "autos/autos.html"
    context_object_name = "autos"

    def get_queryset(self) -> QuerySet:
        return Auto.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:  # noqa: ANN001, ARG002
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Автомобили")
        return context | c_def


class Spares(DataMixin, ListView):
    model = Spare
    template_name = "autos/spares.html"
    context_object_name = "spares"

    def get_queryset(self) -> QuerySet:
        return Spare.objects.all().select_related("car")

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:  # noqa: ANN001, ARG002
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Запчасти")
        return context | c_def


class ShowSpare(DataMixin, DetailView):
    model = Spare
    template_name = "autos/spare.html"
    slug_field = "partnumber"
    slug_url_kwarg = "spare_id"
    context_object_name = "spare"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:  # noqa: ANN001, ARG002
        context = super().get_context_data(**kwargs)
        page_request_objects = self.get_request_paginator()
        c_def = self.get_user_context(title="Запчасти", page_request_objects=page_request_objects)
        return context | c_def

    def get_request_paginator(self) -> Page:
        queryset = Request.objects.filter(spare=self.object)
        paginator = Paginator(queryset, 8)
        page_number = self.request.GET.get("page")
        return paginator.get_page(page_number)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "autos/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:  # noqa: ANN001, ARG002
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return context | c_def

    def form_valid(self, form: RegisterUserForm) -> HttpResponseRedirect:
        user = form.save()
        login(self.request, user)
        return redirect("home")


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "autos/login.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:  # noqa: ANN001, ARG002
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return context | c_def

    def get_success_url(self):  # noqa: ANN201
        return reverse_lazy("home")


def logout_user(request: WSGIRequest) -> HttpResponseRedirect:
    logout(request)
    return redirect("login")


class AddSpare(DataMixin, FormView):
    form_class = AddSpareForm
    template_name = "autos/add_spare.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:  # noqa: ANN001, ARG002
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Новая запчасть")
        return context | c_def

    def form_valid(self, form: AddSpareForm) -> HttpResponse:
        data = form.cleaned_data
        do_add_spare.delay(
            self.request.user.pk, data.get("autodoc_URL"), data.get("exist_URL"),
            data["car"].pk
        )
        return super().form_valid(form)


def about(request: WSGIRequest) -> HttpResponse:  # noqa: ARG001
    return HttpResponse("О сайте")


def parsing_prices(request: WSGIRequest) -> HttpResponseRedirect:
    do_make_request.delay(request.user.pk)
    return redirect("home")
