from django.contrib import admin
from django.urls import path,include
from Auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name= "home"),
    path('login/',views.loginUser,name="login"),
    path('register/',views.registerUser,name = "register"),
    path('profile/',views.profileUser,name = "profile"),
    path('logout/',views.logoutUser,name = "logout")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
