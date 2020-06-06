from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # url('^areas/$', views.AreaListView.as_view()),
    # url(r'^areas/(?P<pk>\d+)/$', views.AreaRetrieveView.as_view()),
]

router = DefaultRouter()
router.register('areas', views.AreaViewSet, base_name='areas')
urlpatterns += router.urls
