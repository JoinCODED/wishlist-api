from django.urls import URLPattern, path, include
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [

    path('register/', UserViewSet.as_view({'post': 'create'}), name="api-register"),
    path("login/", TokenObtainPairView.as_view(), name="api-login"),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    

    path('itemList/', views.ItemListView.as_view(), name="api-list"),
    path('itemDetail/<int:pk>', views.ItemDetialView.as_view(), name="api-detail")
]