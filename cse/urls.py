from . import views
from django.urls import path

urlpatterns = [
    path('',views.login),
    path('register/',views.register),
    path('register/complete_registration/',views.complete_registration),
    path('forget/',views.forget),
    path('forget/forget_user/',views.forget_user),
    path('forget/forget_user/change_password/',views.change_password),
    path('project/',views.project,name="project"),
    path('projectdetails/',views.projectdetails,name="projectdetails"),
    path('addmentors/',views.addmentors,name="addmentors"),
    path('reviewdates/',views.reviewdates,name="reviewdates"),
]
