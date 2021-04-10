from django.contrib import admin

from .models import Person, ScheduledTransaction, Transaction


admin.site.register(Person)
admin.site.register(Transaction)
admin.site.register(ScheduledTransaction)
