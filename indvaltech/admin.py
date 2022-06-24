from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from .models import *


#ORM Titles
admin.site.site_header = "Indval Technologies"
admin.site.index_title = "Welcome to Indvaltech"
admin.site.site_title = "Indvaltech"

#Model Admins
UserAdmin.list_display = ('username', 'email')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Email', 'Phone')

    def Phone(self, obj):
        return obj.Ph


class EducationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Qualification', 'Board')

    def Name(self, obj):
        return obj.EID.Name

    def Qualification(self, obj):
        return obj.qualification

    def Board(self, obj):
        return obj.board


class FamilyAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Member', 'Relation')

    def Name(self, obj):
        return obj.EID.Name

    def Member(self, obj):
        return obj.name

    def Relation(self, obj):
        return obj.relation


class BankAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Bank', 'Branch')

    def Name(self, obj):
        return obj.name

    def Bank(self, obj):
        return obj.bank_name

    def Branch(self, obj):
        return obj.branch


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Organization', 'Designation')

    def Name(self, obj):
        return obj.EID.Name

    def Organization(self, obj):
        return obj.organization

    def Designation(self, obj):
        return obj.designation


class HRDAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Name', 'Designation', 'Department')

    def ID(self, obj):
        return obj.EID


# Register Models
admin.site.register(Project)
#admin.site.register(Team)
#admin.site.register(Timesheet)
#admin.site.register(Attendance)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(HRD_table, HRDAdmin)



#Removing Group
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
