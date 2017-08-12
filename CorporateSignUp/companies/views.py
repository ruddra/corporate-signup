"""
Company Details View
"""
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from companies.models import Company


class CompanyListView(ListView):
    model = Company
    template_name = 'companies/company_list.html'
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(is_active=True).order_by('-last_updated')


class CompanyDetailsView(DetailView):
    model = Company
    template_name = 'companies/company_details.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(is_active=True)
