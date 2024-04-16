from django.urls import path
from .import views
urlpatterns = [
    path('login/', views.loginUser ,name="login"),
    path('logout/', views.logoutUser ,name="logout"),
    path('account/', views.account ,name="account"),
    path('',views.index,name='index'),
    path('createsession',views.createsession,name="add_session"),
    path('sessions',views.sessions,name="sessions"),
    path('update_session/<str:pk>',views.updatesession,name="update_session"),
    path('delete_session/<str:pk>',views.deletesession,name="delete_session"),
    path('inbox/',views.inbox,name="inbox"),
    path('message/<str:pk>',views.viewmessage,name="message"),
    path('create-message/<str:pk>',views.createmessage,name="create-message"),
    path('contact/',views.contact,name="contact"),
    path('session_student/',views.sessionsstudent,name="session_student"),
    path('signal_session/<str:pk>',views.signalsession,name="signal_session"),
    path('about/', views.about ,name="about"),
    path('student_attendance/',views.show_profiles,name="student_attendance"),
    path('create_profile/',views.create_profile,name="create_profile")
]