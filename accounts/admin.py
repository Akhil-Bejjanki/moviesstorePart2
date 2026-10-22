from django.contrib import admin
from .admin_views import top_customers
from .models import TopCustomer

class TopCustomerAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_content = None):
        return top_customers(request)

    def has_add_permission(self, request):
        return False

admin.site.register(TopCustomer, TopCustomerAdmin)

    