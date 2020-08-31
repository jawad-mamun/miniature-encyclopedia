from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    #allows you to search for any entry
    path("wiki/<str:entry>", views.entry, name = "entry"),
    path("newpage/", views.newpage, name = "newpage"),
    path("editpage/<str:entry>", views.edit, name = "editpage"),
    path("randompage/", views.randompage, name = "randompage")
]
