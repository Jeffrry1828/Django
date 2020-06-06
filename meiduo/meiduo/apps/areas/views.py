from rest_framework.response import Response
from rest_framework import generics
from .models import Area
from .serializers import AreaSerializer, AreaSubSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.mixins import CacheResponseMixin


# 查多个list：返回所有的省信息
# 查一个retrieve：返回pk对应的地区，并包含它的子级地区
# class AreaListView(generics.ListAPIView):
#     queryset = Area.objects.filter(parent__isnull=True)
#     serializer_class = AreaSerializer
#     # get
#
#
# class AreaRetrieveView(generics.RetrieveAPIView):
#     queryset = Area.objects.all()
#     serializer_class = AreaSubSerializer
#     # get

class AreaViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    # action:指定请求方式与处理函数的对应关系
    # list===>get
    # retrieve==>get
    # queryset =
    # serializer_class =
    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent__isnull=True)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AreaSerializer
        else:
            return AreaSubSerializer
