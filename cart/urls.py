from django.conf.urls import patterns, url

from .views import CartView


urlpatterns = patterns(
    '',
    url(r'^cart/$', CartView.as_view(), name='cart'),
)
