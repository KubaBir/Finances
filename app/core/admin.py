from django.contrib import admin

from .models import Transaction, User

admin.site.register(User)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('debtor_name', 'info', 'transaction_amount')

    def get_ordering(self, request):
        return ['-value_date']


admin.site.register(Transaction, TransactionAdmin)
