from rest_framework import serializers
from items.models import Item, FavoriteItem
from django.contrib.auth.models import User
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer


class DjoserUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        # pass
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        

class DjoserUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        # pass
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=[ 'first_name', 'last_name']

# class FavSerializer(serializers.ModelSerializer):
#     fav = serializers.Field(source='get_fav')
#     class Meta:
#         model= Item
#         fields = ['favoriteitem_set'
#             # 'request.user.favoriteitem_set.all()'
#             ]
#         def get_fav(self):
#             return self.favoriteitem_set

class ItemListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(view_name="api-detail")
    added_by = UserSerializer()
    favourited = serializers.SerializerMethodField(method_name='get_fav_count')


    class Meta:
        model = Item
        fields=['id','name','detail', 'added_by','favourited']
    
    def get_fav_count(self, item):
        # print(len(item.favoriteitem_set.all()))
        return len(item.favoriteitem_set.all())

class ItemDetailSerializer(serializers.ModelSerializer):
    added_by = UserSerializer()
    favourited_by = serializers.SerializerMethodField(method_name='get_fav_by')
    class Meta:
        model = Item
        fields=['id','name', 'description', 'image', 'added_by', 'favourited_by']

    def get_fav_by(self, item):
        by = []
        for item in item.favoriteitem_set.all():
            by.append(item.user.username)
        return by
