from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from .models import Job

TokenAdmin.raw_id_fields = ('user',)


class JobAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['command', 'owner']
        else:
            return []


admin.site.register(Job, JobAdmin)
