from django.contrib import admin
from .models import Mchango, Contribution

@admin.register(Mchango)
class MchangoAdmin(admin.ModelAdmin):
    list_display = ('mchango_name', 'beneficiary_name', 'start_date', 'end_date')
    search_fields = ['mchango_name', 'beneficiary_name']


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('contributor_name', 'phone_number', 'contribution_amount', 'mchango')
    search_fields = ['contributor_name', 'phone_number', 'mchango__mchango_name']


