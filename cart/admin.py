from django.contrib import admin
from .models import Order, Item, MostFrequentBuyer

from django.db.models import Sum
from django.shortcuts import render

class MostFreqBuyerAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_content=None):
        biggest_buyer = (Item.objects.values('order__user__username').annotate(m_count = Sum('quantity')).order_by('-m_count').first())
        context = {**self.admin_site.each_context(request), 'title' : 'Most Frequent Movie Buyer', 'biggest_buyer' : biggest_buyer}
        return render(request, 'admin/most_freq_buyer.html', context)
    
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(MostFrequentBuyer, MostFreqBuyerAdmin)
