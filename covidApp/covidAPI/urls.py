from django.urls import path, re_path
from covidAPI import views


urlpatterns = [
    re_path(r'^fetch/$', views.FetchCovidData.as_view()),
    # path('fetch/', views.FetchCovidData.as_view()),
    #path('^export/(?P<country>[\w\-\.]+)/(?P<startDate>[\w\-\.]+)/(?P<endDate>[\w\-\.]+)/$', views.ExportCovidData.as_view())
]