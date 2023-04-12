"""nicesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import *
from . import view,adduser,login,controlpane

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^hello/', view.hello),
    url(r'^$', view.hello),
    url(r'^adduser/', adduser.adduser),
    # url(r'^lookup$', lookup.lookup),
    # url(r'^search-form$', search.search_form),
    # url(r'^search$', search.search), # 这个有问题
    # url(r'^search-post$', search2.search_post),
    # url(r'^login-form$', login.login_form),
    url(r'^login/', login.login),
    url(r'^change2log/', view.change2log),
    url(r'^change2adduser/', view.change2adduser),
    url(r'^controlpane/', controlpane.controlpane),
    url(r'^controlpane2up/', controlpane.up),
    url(r'^controlpane2down/', controlpane.down),
]

# from django.conf.urls import url
#
# from . import view
#
# urlpatterns = [
#     url(r'^$', view.hello),
# ]
