from django.contrib import admin
from django.urls import path,include
from video import views

urlpatterns = [
    path('', views.login, name='home'),
    path('login/', views.login, name='login'),
    path('register/',views.register,name='register'),
    path('index/',views.index,name='index'),
    path('logout/', views.logout, name='logout'),
    path('video-rank/', views.video_rank, name='video_rank'),
    path('ai-analysis/', views.ai_analysis, name='ai_analysis'),
    path('fans-analysis/', views.fans_analysis, name='fans_analysis'),
    path('fans-distribution/', views.fans_distribution, name='fans_distribution'),
    path('comment-share/', views.comment_share, name='comment_share'),
    path('ip-analysis/', views.ip_analysis, name='ip_analysis'),
    path('video-wordcloud/', views.video_wordcloud, name='video_wordcloud'),
    path('comment-wordcloud/', views.comment_wordcloud, name='comment_wordcloud'),
    path('like-prediction/', views.like_prediction, name='like_prediction'),
    path('data-management/', views.data_management, name='data_management'),
]