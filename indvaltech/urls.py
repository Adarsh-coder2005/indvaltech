from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    path('', views.login_user, name='login'),
    path('register/<str:name>/', views.register, name="register"),
    path('family/<str:name>/', views.family, name="family"),
    path('famdelete/<str:name>/<str:relation>/',views.family_delete, name='delete_fam'),
    path('hrDashboard/', views.hrDashboard, name="hrDashboard"),
    path('bank/<str:name>/', views.bank, name="bank"),
    path('AddProject/', AddProject.as_view(), name='AddProject'),
    path('AddProject/<pk>/', AddProject.as_view(), name='AddProject'),
    path('AttendForm/', views.AttendForm, name='AttendForm'),
    path('sheets/', views.timesheet, name='sheets'),
    path('DesignDashboard/', views.DesignDashboard, name='DesignDashboard'),
    path('education/<str:name>/', views.education, name='education'),
    path('edudelete/<str:name>/<str:qual>/',views.education_delete, name='delete_edu'),
    path('history/<str:name>/', views.history, name='history'),
    path('histdelete/<str:name>/<str:org>/',views.history_delete, name='delete_history'),
    path('AddActivity/', AddActivity.as_view(), name='AddActivity'),
    path('AddActivity/<pk>/', AddActivity.as_view(), name='AddActivity'),
    path('leave/', views.leave, name='leave'),
    path('payslip/<str:name>/', views.payslip, name="payslip"),
    path('hrd', views.hrd, name="hrd"),
    path('reset/', ResetPasswordView.as_view(), name="reset"),
    path('set_password/<uidb64>/<token>/',setpPasswordView.as_view(), name='set_password'),
    path('search/<str:name>/', views.search, name="search"),
    path('icons/<str:name>/', views.icons, name="icons"),
    path('result/', views.result, name='result'),
    path('bankedit/<str:name>/', views.bankedit, name='bankedit'),
    path('personaledit/<str:name>/', views.personaledit, name='personaledit'),
    path('chart/', views.get_chart, name='chart'),
    path('designer/<str:name>/', views.designer, name='designer'),
    path('searchbyproj/', views.searchbyproj, name='searchbyproj'),
    path('Emplisttable/', views.Emplist, name='EmpList'),
    path('elists/<str:name>/', views.elists , name='elists'),
]
