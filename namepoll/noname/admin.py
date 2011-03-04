from noname.models import CompanyName, Voter, Vote
from django.contrib import admin


class VoterAdmin(admin.ModelAdmin):
    model = Voter

class VoteInline(admin.TabularInline):
    model=Vote


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
    inlines = [VoteInline]
    list_display = ('name',)

admin.site.register(CompanyName, NameAdmin)
admin.site.register(Voter, VoterAdmin)

