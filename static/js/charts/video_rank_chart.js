// 视频排行图表初始化
function initVideoRankChart(videoData) {
    var chartDom = document.getElementById('videoRankChart');
    if (!chartDom) {
        console.error('图表容器未找到');
        return;
    }
    
    var myChart = echarts.init(chartDom);
    
    // 处理数据
    var categories = videoData.map(function(item, index) {
        var desc = item.description || '视频' + (index + 1);
        return desc.length > 15 ? desc.substring(0, 15) + '...' : desc;
    });
    
    var collectData = videoData.map(function(item) {
        return item.collectCount || 0;
    });
    
    var commentData = videoData.map(function(item) {
        return item.commentCount || 0;
    });
    
    var shareData = videoData.map(function(item) {
        return item.shareCount || 0;
    });
    
    var likeData = videoData.map(function(item) {
        return item.likeCount || 0;
    });
    
    var option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#999'
                }
            }
        },
        legend: {
            data: ['收藏', '评论', '分享', '点赞'],
            top: 10
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: categories,
                axisPointer: {
                    type: 'shadow'
                },
                axisLabel: {
                    interval: 0,
                    rotate: 30,
                    fontSize: 11
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '数量',
                axisLabel: {
                    formatter: '{value}'
                }
            },
            {
                type: 'value',
                name: '点赞数',
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: [
            {
                name: '收藏',
                type: 'bar',
                data: collectData,
                itemStyle: {
                    color: '#fbbf24'
                }
            },
            {
                name: '评论',
                type: 'bar',
                data: commentData,
                itemStyle: {
                    color: '#f59e0b'
                }
            },
            {
                name: '分享',
                type: 'bar',
                data: shareData,
                itemStyle: {
                    color: '#d97706'
                }
            },
            {
                name: '点赞',
                type: 'line',
                yAxisIndex: 1,
                data: likeData,
                smooth: true,
                itemStyle: {
                    color: '#10b981'
                },
                lineStyle: {
                    width: 3
                }
            }
        ]
    };
    
    myChart.setOption(option);
    
    // 响应式
    window.addEventListener('resize', function() {
        myChart.resize();
    });
    
    return myChart;
}
