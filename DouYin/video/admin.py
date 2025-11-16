from django.contrib import admin
from .models import VideoData,CommentData,User

admin.site.site_header = '彭于晏管理后台'
admin.site.site_title = '彭于晏管理后台'
admin.site.index_title = '彭于晏管理后台'

@admin.register(VideoData)
class VideoDataAdmin(admin.ModelAdmin):
    list_display = ('username','aweme_id','likeCount',
                    'collectCount','commentCount',
                    'shareCount','downloadCount')
    search_fields = ['username','aweme_id','likeCount']
    list_filter = ['aweme_id','likeCount']
    ordering = ('-likeCount',)

@admin.register(CommentData)
class CommentDataAdmin(admin.ModelAdmin):
    list_display = ('userid','username','commentTime','userIP','likeCount')
    search_fields = ['userid','username','commentTime']
    list_filter = ['userid','commentTime']
    ordering = ('-commentTime',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password','createTime')
    search_fields = ['username']
    list_filter = ['username']
    ordering = ('-createTime',)