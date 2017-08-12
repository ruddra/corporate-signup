"""CorporateSignUp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _

from companies.views import CompanyListView, CompanyDetailsView
from users.views import UserSignUpView, ConfirmView, \
    BillingAddressView, ConfirmVerifyView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sign-up/(?P<company_id>[0-9]+)/',
        UserSignUpView.as_view(), name="sign-up"),
    url(r'^company-details/(?P<pk>[0-9]+)/',
        CompanyDetailsView.as_view(), name="company-details"),
    url(r'^confirm/', ConfirmVerifyView.as_view(), name='confirm'),
    url(r'^thank-you/', ConfirmView.as_view(), name='thank-you'),
    url(r'^billing-address/', BillingAddressView.as_view(),
        name='billing-address'),
    url(r'^$', CompanyListView.as_view(), name='main'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = _('Corporate SignUp Adminsite')
