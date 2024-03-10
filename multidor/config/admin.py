from django.contrib import admin
from .models import Sites, Content, Bonus, Casino

# Register your models here.

admin.site.register(Sites)
admin.site.register(Content)
admin.site.register(Bonus)
admin.site.register(Casino)