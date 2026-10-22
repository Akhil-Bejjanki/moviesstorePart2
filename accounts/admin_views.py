from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render

def top_customers(request):

    size = request.GET.get('size') or request.GET.get('limit')

    users = User.objects.annotate(total_purchases = Sum('order__item__quantity', default = 0)).order_by("-total_purchases", "username")

    if size and size.strip().isdigit() and int(size.strip()) > 0:
        users  = users[: int(size.strip())]

    
    context = {
        "title": "Top Customers",
        "users": users,
        "size": size or ''
    }

    return render(request, "admin/top_customers.html", context)