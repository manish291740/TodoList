from django.urls import path
from .views import TaskList,TaskDetail,TaskCreation,TaskUpdate,TaskDelete,CustomLogin,Register
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('login/',CustomLogin.as_view(),name='Login'),
    path('logout/',LogoutView.as_view(next_page='Login'),name='Logout'),
    path('Register/',Register.as_view(),name='Register'),
    path('',TaskList.as_view(),name='tasklist'),
    path('Task-creation',TaskCreation.as_view(),name='TaskCreation'),
    path('Task-updation/<int:pk>/',TaskUpdate.as_view(),name='taskUpdate'),
    path('Task-delete/<int:pk>/',TaskDelete.as_view(),name='taskDelete'),
    path('Task/<int:pk>/',TaskDetail.as_view(),name='taskdetail')
]