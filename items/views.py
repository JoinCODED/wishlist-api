from django.shortcuts import render, redirect
from items.models import Item, FavoriteItem
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse

# Create your views here.
def item_list(request):
    items = Item.objects.all()
    if request.user.is_authenticated:
        favorite_list = request.user.favoriteitem_set.all().values_list('item', flat=True)
    context = {
        "items": items,
        "favorite_list": favorite_list
    }
    return render(request, 'item_list.html', context)

def item_detail(request, item_id):
    context = {
        "item": Item.objects.get(id=item_id)
    }
    return render(request, 'item_detail.html', context)

def user_register(request):
    register_form = UserRegisterForm()
    if request.method == "POST":
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('item-list')
    context = {
        "register_form": register_form
    }
    return render(request, 'user_register.html', context)

def user_login(request):
    login_form = UserLoginForm()
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('item-list')
    context = {
        "login_form": login_form
    }
    return render(request, 'user_login.html', context)

def user_logout(request):
    logout(request)

    return redirect('item-list')

def item_favorite(request, item_id):
    item_object = Item.objects.get(id=item_id)
    if request.user.is_anonymous:
        return redirent('user-login')
    
    favorite, created = FavoriteItem.objects.get_or_create(user=request.user, item=item_object)
    if created:
        action = "favorite"
    else:
        favorite.delete()
        action="unfavorite"
    
    response = {
        "action": action,
    }
    return JsonResponse(response, safe=False)

def wishlist(request):
    wishlist = []
    items = Item.objects.all()
    if request.user.is_authenticated:
        favorite_objects = request.user.favoriteitem_set.all()
    for item in items:
        for favorite in favorite_objects:
            if item.id == favorite.item_id:
                wishlist.append(item)
    context = {
        "wishlist": wishlist
    }
    return render(request, 'wishlist.html', context)
