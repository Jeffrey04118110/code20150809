# file: user/urls.py

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^reg$', views.reg_view),
    url(r'^reg2$', views.reg2_view),
    url(r'^login', views.login_view),
    url(r'^logout', views.logout_view),
    url(r'^mod_passwd', views.mod_passwd_view),
    url(r'\S*\s*', views.failed_view),
]