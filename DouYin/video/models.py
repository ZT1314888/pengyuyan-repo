from django.db import models

class VideoData(models.Model):

    """"
    视频信息表
    """
    username = models.TextField(verbose_name='用户名',null=True,blank=True)
    fansCount = models.BigIntegerField(verbose_name='粉丝数量',null=True,blank=True)
    description = models.TextField(verbose_name='视频描述',null=True,blank=True)
    aweme_id = models.TextField(verbose_name='视频id',null=True,blank=True)
    publishTime = models.TextField(verbose_name='发表时间',null=True,blank=True)
    duration = models.TextField(verbose_name='视频时长',null=True,blank=True)
    likeCount = models.BigIntegerField(verbose_name='点赞数量',null=True,blank=True)
    collectCount = models.BigIntegerField(verbose_name='收藏数量',null=True,blank=True)
    commentCount = models.BigIntegerField(verbose_name='评论数量',null=True,blank=True)
    shareCount = models.BigIntegerField(verbose_name='分享数量',null=True,blank=True)
    downloadCount = models.BigIntegerField(verbose_name='下载数量',null=True,blank=True)


    class Meta:
        verbose_name = '视频信息'
        db_table = 'videodata'
        verbose_name_plural = '视频数据'

class CommentData(models.Model):

    """"
    视频评论表
    """
    userid = models.BigIntegerField(verbose_name='用户id',null=True,blank=True)
    username = models.TextField(verbose_name='用户名',null=True,blank=True)
    commentTime = models.TextField(verbose_name='评论时间',null=True,blank=True)
    userIP = models.TextField(verbose_name='IP地址',null=True,blank=True)
    content = models.TextField(verbose_name='评论内容',null=True,blank=True)
    likeCount = models.BigIntegerField(verbose_name='点赞数量',null=True,blank=True)
    aweme_id = models.BigIntegerField(verbose_name='aweme_id',null=True,blank=True)

    class Meta:
        verbose_name = '评论信息'
        db_table = 'commentdata'
        verbose_name_plural = '评论数据'

class User(models.Model):
    objects = None
    username = models.CharField(max_length=255,verbose_name='用户名')
    password = models.CharField(max_length=255,verbose_name='密码')
    createTime = models.DateField(auto_now_add=True,verbose_name='注册时间')

    class Meta:
        db_table = 'user'
        verbose_name = '用户信息'
        verbose_name_plural = '用户数据'