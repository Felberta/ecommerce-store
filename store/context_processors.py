from .models import OrderItem

def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(order__user=request.user, order__complete=False)
        count = sum(item.quantity for item in items)
    return {'cart_item_count': count}
