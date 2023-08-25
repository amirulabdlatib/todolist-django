from django.urls import path
from . import views

app_name = 'todoapp'

urlpatterns = [
    path('',views.render_login,name='render_login'),
    path('doLogin',views.doLogin,name='doLogin'),
    path('register/',views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('done/<int:id>',views.done,name='done'),
    path('undone/<int:id>',views.undone,name='undone'),
    path('update/<int:id>',views.update,name='update'),
    path('delete_item/<int:id>',views.delete_task,name='delete_task'),
    path('logout',views.doLogout,name='doLogout')
]
