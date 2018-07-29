from django.shortcuts import render
from items.models import Item

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
    pass

def item_update(request):
    pass

def item_delete(request):
    pass