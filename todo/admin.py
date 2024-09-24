from django.contrib import admin
from .models import todo
# Register your models here.

# admin.py file is for controlling the admin page interface and functions 

# for customizing the admin interface we can do this.
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('createdDate', )  # this will only read the createdDate field which we defined it in models file


admin.site.register(todo, TodoAdmin)