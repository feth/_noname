from noname.models import Evaluation, CompanyName, Voter
from django.contrib import admin


class EvaluationAdmin(admin.StackedInline):
    model = Evaluation


class VoterAdmin(admin.ModelAdmin):
    model = Voter
    inlines = [EvaluationAdmin]


class NameAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {
             'fields': ('name',)
             }
            ),
            ('Availability', {
             'fields': ('free_brand', 'free_dotnet', 'free_dotcom', 'free_dotfr')
             }
            ),
            ('Optional info', {
            'fields': ('explanation', 'image')
            }
            )
            )
    inlines = [EvaluationAdmin]
    list_display = ('name',)

admin.site.register(CompanyName, NameAdmin)
admin.site.register(Voter, VoterAdmin)
