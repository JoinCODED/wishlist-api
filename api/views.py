from django.shortcuts import render
from requests import request
from rest_framework.generics import  RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import ItemDetailSerializer, ItemListSerializer
from items.models import Item
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsAdminOrReadOnly, IsAdminOrOwnerCanView

class ItemDetialView(RetrieveUpdateDestroyAPIView):
    queryset=Item.objects.all()
    serializer_class=ItemDetailSerializer
    permission_classes=[IsAdminOrOwnerCanView]


class ItemListView(ListCreateAPIView):
    queryset=Item.objects.all()
    serializer_class=ItemListSerializer
    permission_classes=[IsAdminOrReadOnly]
    def get_serializer_context(self):
        return {'request':self.request}
        
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['description', 'name']