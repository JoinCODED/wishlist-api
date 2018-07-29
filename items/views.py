from django.shortcuts import render, redirect
from items.models import Item
from .forms import ItemModelForm

# Create your views here.
def item_list(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, 'item_list.html', context)

def item_detail(request, item_id):
    context = {
        "item": Item.objects.get(id=item_id)
    }
    return render(request, 'item_detail.html', context)

def item_create(request):
    new_item_form = ItemModelForm()
    if request.method == "POST":
        new_item_form = ItemModelForm(request.POST, request.FILES)
        if new_item_form.is_valid():
            new_item_form.save()
            return redirect('item-list')
    context = {
        "new_item_form": new_item_form
    }
    return render(request, 'item_create.html', context)