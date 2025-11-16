from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from video.models import User, VideoData, CommentData
from django.db.models import Max, Count
from functools import wraps

# Create your views here.

def login_required(view_func):
    """
    登录验证装饰器
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('username'):
            messages.warning(request, '请先登录')
            return redirect('/home/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

def login(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=uname,password=password)
            request.session['username'] = uname
            request.session['uid'] = user.id
            return redirect('/home/index/')
        except:
            messages.error(request, '请输入正确的用户名或密码')
            return HttpResponseRedirect('/home/login/')
    else:
        return render(request, "login.html")

def register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        password = request.POST.get("password")
        try:
            User.objects.get(username=uname)
            messages.error(request,"用户已存在")
            return HttpResponseRedirect("/home/register/")
        except:
            User.objects.create(username=uname,password=password)
            messages.success(request,"注册成功")
            return HttpResponseRedirect("/home/login/")
    else:
        return render(request, "register.html")


@login_required
def index(request):
    # 获取统计数据
    video_stats = VideoData.objects.aggregate(
        max_videos=Count('id'),
        max_like=Max('likeCount'),
        max_comment=Max('commentCount'),
        max_collect=Max('collectCount')
    )
    
    # 获取视频排行数据（前10条）
    top_videos = VideoData.objects.order_by('-likeCount')[:10].values(
        'description', 'likeCount', 'collectCount', 'commentCount', 'shareCount'
    )
    
    context = {
        'max_videos': video_stats['max_videos'] or 0,
        'max_like': video_stats['max_like'] or 0,
        'max_comment': video_stats['max_comment'] or 0,
        'max_collect': video_stats['max_collect'] or 0,
        'top_videos': list(top_videos)
    }
    
    return render(request, "index.html", context)


@login_required
def video_rank(request):
    """
    视频排行榜页面
    """
    # 获取排序参数，默认按点赞数排序
    sort_by = request.GET.get('sort', 'like')
    
    # 根据不同排序方式获取数据
    if sort_by == 'like':
        videos = VideoData.objects.order_by('-likeCount')[:50]
        title = '点赞排行榜'
    elif sort_by == 'comment':
        videos = VideoData.objects.order_by('-commentCount')[:50]
        title = '评论排行榜'
    elif sort_by == 'collect':
        videos = VideoData.objects.order_by('-collectCount')[:50]
        title = '收藏排行榜'
    elif sort_by == 'share':
        videos = VideoData.objects.order_by('-shareCount')[:50]
        title = '分享排行榜'
    else:
        videos = VideoData.objects.order_by('-likeCount')[:50]
        title = '点赞排行榜'
    
    context = {
        'videos': videos,
        'title': title,
        'sort_by': sort_by
    }
    
    return render(request, "video_rank.html", context)


@login_required
def ai_analysis(request):
    """
    分析建议页面
    """
    from django.db.models import Avg, Sum
    
    # 获取整体数据统计
    overall_stats = VideoData.objects.aggregate(
        avg_like=Avg('likeCount'),
        avg_comment=Avg('commentCount'),
        avg_collect=Avg('collectCount'),
        avg_share=Avg('shareCount'),
        total_videos=Count('id')
    )
    
    # 获取高表现视频（点赞数前10%）
    total_count = overall_stats['total_videos'] or 0
    if total_count > 10:
        top_count = max(1, int(total_count * 0.1))
        top_videos = VideoData.objects.order_by('-likeCount')[:top_count]
        
        high_performance = {
            'avg_like': sum(v.likeCount or 0 for v in top_videos) / top_count,
            'avg_comment': sum(v.commentCount or 0 for v in top_videos) / top_count,
            'avg_collect': sum(v.collectCount or 0 for v in top_videos) / top_count,
            'avg_share': sum(v.shareCount or 0 for v in top_videos) / top_count,
            'avg_fans': sum(v.fansCount or 0 for v in top_videos) / top_count,
        }
    else:
        high_performance = {
            'avg_like': overall_stats['avg_like'] or 0,
            'avg_comment': overall_stats['avg_comment'] or 0,
            'avg_collect': overall_stats['avg_collect'] or 0,
            'avg_share': overall_stats['avg_share'] or 0,
            'avg_fans': 0,
        }
    
    # 计算差值
    comparison_data = {
        'like_diff': int(high_performance['avg_like'] - (overall_stats['avg_like'] or 0)),
        'comment_diff': int(high_performance['avg_comment'] - (overall_stats['avg_comment'] or 0)),
        'collect_diff': int(high_performance['avg_collect'] - (overall_stats['avg_collect'] or 0)),
        'share_diff': int(high_performance['avg_share'] - (overall_stats['avg_share'] or 0)),
    }
    
    # 获取样本视频用于分析
    sample_videos = VideoData.objects.order_by('-likeCount')[:5]
    
    # 生成AI建议
    suggestions = generate_ai_suggestions(overall_stats, high_performance, sample_videos)
    
    context = {
        'overall_stats': overall_stats,
        'high_performance': high_performance,
        'comparison_data': comparison_data,
        'suggestions': suggestions,
        'sample_videos': sample_videos
    }
    
    return render(request, "ai_analysis.html", context)


def generate_ai_suggestions(overall_stats, high_performance, sample_videos):
    """
    生成AI分析建议
    """
    suggestions = []
    
    # 1. 互动率分析
    if overall_stats['avg_like'] and overall_stats['avg_comment']:
        engagement_rate = (overall_stats['avg_comment'] / overall_stats['avg_like']) * 100
        if engagement_rate < 5:
            suggestions.append({
                'type': 'warning',
                'icon': 'fa-exclamation-triangle',
                'title': '互动率偏低',
                'description': f'当前评论/点赞比率为 {engagement_rate:.2f}%，建议在视频中增加互动引导，如提问、投票等。',
                'priority': 'high'
            })
        else:
            suggestions.append({
                'type': 'success',
                'icon': 'fa-check-circle',
                'title': '互动率良好',
                'description': f'当前评论/点赞比率为 {engagement_rate:.2f}%，保持当前的互动策略。',
                'priority': 'low'
            })
    
    # 2. 收藏率分析
    if overall_stats['avg_like'] and overall_stats['avg_collect']:
        collect_rate = (overall_stats['avg_collect'] / overall_stats['avg_like']) * 100
        if collect_rate < 10:
            suggestions.append({
                'type': 'info',
                'icon': 'fa-star',
                'title': '提升收藏率',
                'description': f'当前收藏率为 {collect_rate:.2f}%，建议创作更多干货内容，提供实用价值。',
                'priority': 'medium'
            })
    
    # 3. 分享率分析
    if overall_stats['avg_like'] and overall_stats['avg_share']:
        share_rate = (overall_stats['avg_share'] / overall_stats['avg_like']) * 100
        if share_rate < 5:
            suggestions.append({
                'type': 'warning',
                'icon': 'fa-share-alt',
                'title': '分享率待提升',
                'description': f'当前分享率为 {share_rate:.2f}%，建议创作更具传播性的内容，引发情感共鸣。',
                'priority': 'medium'
            })
    
    # 4. 内容质量建议
    if high_performance['avg_like'] and overall_stats['avg_like']:
        performance_gap = (high_performance['avg_like'] / overall_stats['avg_like']) - 1
        if performance_gap > 2:
            suggestions.append({
                'type': 'info',
                'icon': 'fa-lightbulb-o',
                'title': '学习高表现内容',
                'description': f'高表现视频的点赞数是平均值的 {performance_gap + 1:.1f} 倍，建议分析其内容特点和创作手法。',
                'priority': 'high'
            })
    
    # 5. 粉丝增长建议
    if high_performance.get('avg_fans', 0) > 10000:
        suggestions.append({
            'type': 'success',
            'icon': 'fa-users',
            'title': '粉丝基础良好',
            'description': f'高表现视频作者平均粉丝数为 {high_performance["avg_fans"]:.0f}，持续输出优质内容以维持粉丝增长。',
            'priority': 'low'
        })
    else:
        suggestions.append({
            'type': 'info',
            'icon': 'fa-users',
            'title': '加强粉丝运营',
            'description': '建议通过系列内容、固定更新时间等方式培养粉丝粘性。',
            'priority': 'medium'
        })
    
    # 6. 内容策略建议
    suggestions.append({
        'type': 'info',
        'icon': 'fa-calendar',
        'title': '发布时间优化',
        'description': '建议在用户活跃时段发布（晚上7-10点），提高初始曝光量。',
        'priority': 'medium'
    })
    
    # 7. 视频时长建议
    suggestions.append({
        'type': 'info',
        'icon': 'fa-clock-o',
        'title': '视频时长建议',
        'description': '建议控制视频时长在15-60秒，保持内容紧凑，提高完播率。',
        'priority': 'low'
    })
    
    # 8. 标题优化建议
    suggestions.append({
        'type': 'info',
        'icon': 'fa-font',
        'title': '标题优化',
        'description': '使用吸引眼球的标题，包含关键词和数字，提高点击率。',
        'priority': 'medium'
    })
    
    return suggestions


def logout(request):
    """
    退出登录
    """
    # 清除session
    request.session.flush()
    # 添加提示消息
    messages.success(request, '您已成功退出登录')
    # 重定向到登录页
    return redirect('/home/login/')


@login_required
def fans_analysis(request):
    """
    用户粉丝分析 - 饼图展示粉丝排行
    """
    # 获取粉丝数前10的用户
    top_users = VideoData.objects.values('username', 'fansCount').distinct().order_by('-fansCount')[:10]
    
    # 准备图表数据
    chart_data = []
    for user in top_users:
        if user['username'] and user['fansCount']:
            chart_data.append({
                'name': user['username'],
                'value': user['fansCount']
            })
    
    context = {
        'chart_data': chart_data,
        'total_users': VideoData.objects.values('username').distinct().count()
    }
    
    return render(request, "fans_analysis.html", context)


@login_required
def fans_distribution(request):
    """
    粉丝数量分析 - 柱状图展示粉丝区间分布
    """
    # 定义粉丝数区间
    ranges = [
        {'label': '0-1000', 'min': 0, 'max': 1000},
        {'label': '1000-5000', 'min': 1000, 'max': 5000},
        {'label': '5000-1万', 'min': 5000, 'max': 10000},
        {'label': '1万-5万', 'min': 10000, 'max': 50000},
        {'label': '5万-10万', 'min': 50000, 'max': 100000},
        {'label': '10万+', 'min': 100000, 'max': 999999999},
    ]
    
    # 统计每个区间的数量
    distribution = []
    for r in ranges:
        count = VideoData.objects.filter(
            fansCount__gte=r['min'],
            fansCount__lt=r['max']
        ).count()
        distribution.append({
            'range': r['label'],
            'count': count
        })
    
    context = {
        'distribution': distribution
    }
    
    return render(request, "fans_distribution.html", context)


@login_required
def comment_share(request):
    """
    评论与分享分析 - 展示评论和分享的关系
    """
    # 获取评论数和分享数前10的视频
    top_videos = VideoData.objects.order_by('-commentCount')[:10].values(
        'description', 'commentCount', 'shareCount', 'likeCount'
    )
    
    context = {
        'videos': list(top_videos)
    }
    
    return render(request, "comment_share.html", context)


@login_required
def ip_analysis(request):
    """
    IP地址分析 - 展示评论用户的地域分布
    """
    # 获取IP地址统计
    ip_stats = CommentData.objects.values('userIP').annotate(
        count=Count('id')
    ).order_by('-count')[:20]
    
    # 准备图表数据
    chart_data = []
    for item in ip_stats:
        if item['userIP']:
            chart_data.append({
                'location': item['userIP'],
                'count': item['count']
            })
    
    context = {
        'chart_data': chart_data,
        'total_comments': CommentData.objects.count()
    }
    
    return render(request, "ip_analysis.html", context)


@login_required
def video_wordcloud(request):
    """
    视频词云图 - 展示视频描述的关键词
    """
    # 获取所有视频描述
    videos = VideoData.objects.all()[:200]
    descriptions = [v.description for v in videos if v.description]
    
    # 简单的词频统计（实际应该使用jieba分词）
    word_freq = {}
    for desc in descriptions:
        words = desc.split()
        for word in words:
            if len(word) > 1:  # 过滤单字
                word_freq[word] = word_freq.get(word, 0) + 1
    
    # 转换为词云数据格式，包含字体大小
    wordcloud_data = [
        {
            'name': k, 
            'value': v,
            'size': v + 10  # 预先计算字体大小
        } 
        for k, v in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:100]
    ]
    
    context = {
        'wordcloud_data': wordcloud_data,
        'total_videos': len(descriptions)
    }
    
    return render(request, "video_wordcloud.html", context)


@login_required
def comment_wordcloud(request):
    """
    评论词云图 - 展示评论内容的关键词
    """
    # 获取所有评论
    comments = CommentData.objects.all()[:500]
    contents = [c.content for c in comments if c.content]
    
    # 简单的词频统计
    word_freq = {}
    for content in contents:
        words = content.split()
        for word in words:
            if len(word) > 1:
                word_freq[word] = word_freq.get(word, 0) + 1
    
    # 转换为词云数据格式，包含字体大小
    wordcloud_data = [
        {
            'name': k, 
            'value': v,
            'size': v + 10  # 预先计算字体大小
        } 
        for k, v in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:100]
    ]
    
    context = {
        'wordcloud_data': wordcloud_data,
        'total_comments': len(contents)
    }
    
    return render(request, "comment_wordcloud.html", context)


@login_required
def like_prediction(request):
    """
    点赞量趋势预测 - 使用机器学习模型预测
    """
    prediction_result = None
    
    if request.method == 'POST':
        # 获取表单数据
        try:
            duration = int(request.POST.get('duration', 60))
            collect = int(request.POST.get('collect', 0))
            comment = int(request.POST.get('comment', 0))
            share = int(request.POST.get('share', 0))
            fans = int(request.POST.get('fans', 0))
            hour = int(request.POST.get('hour', 12))
            
            # 计算互动率
            interaction_rate = (comment + share) / max(fans, 1)
            
            # 调用预测模型
            from forecast import predict_likes
            input_data = {
                'duration': duration,
                'collect': collect,
                'comment': comment,
                'share': share,
                'fans': fans,
                'interaction_rate': interaction_rate,
                'hour': hour
            }
            
            prediction_result = predict_likes(input_data)
        except Exception as e:
            prediction_result = f"预测失败: {str(e)}"
    
    # 获取历史数据用于展示趋势
    recent_videos = VideoData.objects.order_by('-id')[:30].values(
        'publishTime', 'likeCount'
    )
    
    context = {
        'prediction_result': prediction_result,
        'recent_videos': list(recent_videos)
    }
    
    return render(request, "like_prediction.html", context)


@login_required
def data_management(request):
    """
    信息管理 - 数据统计和管理
    """
    # 获取数据统计
    video_count = VideoData.objects.count()
    comment_count = CommentData.objects.count()
    user_count = User.objects.count()
    
    # 获取最新的视频
    recent_videos = VideoData.objects.order_by('-id')[:10]
    
    # 获取最新的评论
    recent_comments = CommentData.objects.order_by('-id')[:10]
    
    context = {
        'video_count': video_count,
        'comment_count': comment_count,
        'user_count': user_count,
        'recent_videos': recent_videos,
        'recent_comments': recent_comments
    }
    
    return render(request, "data_management.html", context)

@login_required
def video_wordcloud(request):
    """
    视频词云图 - 展示视频描述的关键词
    """
    # 获取所有视频描述
    videos = VideoData.objects.all()[:200]
    descriptions = [v.description for v in videos if v.description]
    
    # 简单的词频统计
    word_freq = {}
    for desc in descriptions:
        words = desc.split()
        for word in words:
            if len(word) > 1:  # 过滤单字
                word_freq[word] = word_freq.get(word, 0) + 1
    
    # 获取最大词频用于归一化
    max_freq = max(word_freq.values()) if word_freq else 1
    
    # 转换为词云数据格式，使用level分级
    wordcloud_data = []
    for k, v in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:100]:
        # 将词频归一化到1-10级
        level = min(10, max(1, int((v / max_freq) * 10)))
        wordcloud_data.append({
            'name': k, 
            'value': v,
            'level': level
        })
    
    context = {
        'wordcloud_data': wordcloud_data,
        'total_videos': len(descriptions),
        'banner_text': f'基于 {len(descriptions)} 个视频描述生成的关键词词云，字体大小代表词频高低'
    }
    
    return render(request, "video_wordcloud.html", context)


@login_required
def comment_wordcloud(request):
    """
    评论词云图 - 展示评论内容的关键词
    """
    # 获取所有评论
    comments = CommentData.objects.all()[:500]
    contents = [c.content for c in comments if c.content]
    
    # 简单的词频统计
    word_freq = {}
    for content in contents:
        words = content.split()
        for word in words:
            if len(word) > 1:
                word_freq[word] = word_freq.get(word, 0) + 1
    
    # 获取最大词频用于归一化
    max_freq = max(word_freq.values()) if word_freq else 1
    
    # 转换为词云数据格式，使用level分级
    wordcloud_data = []
    for k, v in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:100]:
        # 将词频归一化到1-10级
        level = min(10, max(1, int((v / max_freq) * 10)))
        wordcloud_data.append({
            'name': k, 
            'value': v,
            'level': level
        })
    
    context = {
        'wordcloud_data': wordcloud_data,
        'total_comments': len(contents),
        'banner_text': f'基于 {len(contents)} 条评论内容生成的关键词词云，反映用户关注热点'
    }
    
    return render(request, "comment_wordcloud.html", context)


@login_required
def like_prediction(request):
    """
    点赞量趋势预测 - 使用机器学习模型预测
    """
    prediction_result = None
    
    if request.method == 'POST':
        # 获取表单数据
        try:
            duration = int(request.POST.get('duration', 60))
            collect = int(request.POST.get('collect', 0))
            comment = int(request.POST.get('comment', 0))
            share = int(request.POST.get('share', 0))
            fans = int(request.POST.get('fans', 0))
            hour = int(request.POST.get('hour', 12))
            
            # 计算互动率
            interaction_rate = (comment + share) / max(fans, 1)
            
            # 调用预测模型
            from forecast import predict_likes
            input_data = {
                'duration': duration,
                'collect': collect,
                'comment': comment,
                'share': share,
                'fans': fans,
                'interaction_rate': interaction_rate,
                'hour': hour
            }
            
            prediction_result = predict_likes(input_data)
        except Exception as e:
            prediction_result = f"预测失败: {str(e)}"
    
    # 获取历史数据用于展示趋势
    recent_videos = VideoData.objects.order_by('-id')[:30].values(
        'publishTime', 'likeCount'
    )
    
    context = {
        'prediction_result': prediction_result,
        'recent_videos': list(recent_videos)
    }
    
    return render(request, "like_prediction.html", context)


@login_required
def data_management(request):
    """
    信息管理 - 数据统计和管理
    """
    # 获取数据统计
    video_count = VideoData.objects.count()
    comment_count = CommentData.objects.count()
    user_count = User.objects.count()
    
    # 获取最新的视频
    recent_videos = VideoData.objects.order_by('-id')[:10]
    
    # 获取最新的评论
    recent_comments = CommentData.objects.order_by('-id')[:10]
    
    context = {
        'video_count': video_count,
        'comment_count': comment_count,
        'user_count': user_count,
        'recent_videos': recent_videos,
        'recent_comments': recent_comments
    }
    
    return render(request, "data_management.html", context)
