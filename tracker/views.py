from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ApplicationForm
from .models import Application


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("tracker:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class OwnedMixin(LoginRequiredMixin):
    """Every query is scoped to the logged-in user, so nobody can see or edit another user's data."""

    def get_queryset(self):
        return Application.objects.filter(owner=self.request.user)


class ApplicationList(OwnedMixin, ListView):
    template_name = "tracker/list.html"
    context_object_name = "applications"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get("status")
        q = self.request.GET.get("q", "").strip()
        if status in Application.Status.values:
            qs = qs.filter(status=status)
        if q:
            qs = qs.filter(Q(company__icontains=q) | Q(role__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        counts = dict(
            super().get_queryset().values_list("status").annotate(n=Count("id")).order_by()
        )
        ctx["stats"] = [(value, label, counts.get(value, 0)) for value, label in Application.Status.choices]
        ctx["current_status"] = self.request.GET.get("status", "")
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class ApplicationCreate(LoginRequiredMixin, CreateView):
    form_class = ApplicationForm
    template_name = "tracker/form.html"
    success_url = reverse_lazy("tracker:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Application added.")
        return super().form_valid(form)


class ApplicationUpdate(OwnedMixin, UpdateView):
    form_class = ApplicationForm
    template_name = "tracker/form.html"
    success_url = reverse_lazy("tracker:list")

    def form_valid(self, form):
        messages.success(self.request, "Changes saved.")
        return super().form_valid(form)


class ApplicationDelete(OwnedMixin, DeleteView):
    template_name = "tracker/confirm_delete.html"
    success_url = reverse_lazy("tracker:list")

    def form_valid(self, form):
        messages.success(self.request, "Application deleted.")
        return super().form_valid(form)
