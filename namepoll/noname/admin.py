from noname.models import CompanyName, Voter, Vote
from django.contrib import admin


class VoterAdmin(admin.ModelAdmin):
    model = Voter

class VoteInline(admin.TabularInline):
    model=Vote


class NameAdmin(admin.ModelAdmin):
    fields=['name', 'explanation', 'image']
    inlines = [VoteInline]
    list_display = ('name',)

admin.site.register(CompanyName, NameAdmin)
admin.site.register(Voter, VoterAdmin)

