from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^process$', views.process),
    url(r'^main$', views.main),    
    url(r'^add$', views.add),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^list/(?P<id>\d+)$', views.list),
    url(r'^remove/(?P<id>\d+)$', views.remove)
]
