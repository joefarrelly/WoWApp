from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Advertiser)
admin.site.register(Booster)
admin.site.register(Boost)
admin.site.register(Booking)
admin.site.register(Attendance)
admin.site.register(Transaction)
admin.site.register(BookingTransaction)