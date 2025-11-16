"""
数据库初始化脚本
用于快速初始化数据库和导入示例数据
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dy_project.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User as DjangoUser
import sys


def init_database():
    """初始化数据库"""
    print("=" * 50)
    print("开始初始化数据库...")
    print("=" * 50)
    
    # 1. 执行数据库迁移
    print("\n[1/4] 执行数据库迁移...")
    try:
        call_command('makemigrations')
        call_command('migrate')
        print("✓ 数据库迁移完成")
    except Exception as e:
        print(f"✗ 数据库迁移失败: {e}")
        return False
    
    # 2. 创建超级管理员
    print("\n[2/4] 创建超级管理员账号...")
    try:
        if not DjangoUser.objects.filter(username='admin').exists():
            DjangoUser.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("✓ 超级管理员创建成功")
            print("  用户名: admin")
            print("  密码: admin123")
            print("  ⚠️  请在生产环境中修改密码！")
        else:
            print("✓ 超级管理员已存在")
    except Exception as e:
        print(f"✗ 创建超级管理员失败: {e}")
    
    # 3. 导入示例数据
    print("\n[3/4] 导入示例数据...")
    try:
        # 检查是否有fixtures文件
        fixtures_path = 'data/fixtures.json'
        if os.path.exists(fixtures_path):
            call_command('loaddata', fixtures_path)
            print("✓ 示例数据导入成功")
        else:
            print("⚠️  未找到示例数据文件，跳过此步骤")
            print(f"   如需导入数据，请将数据文件放在: {fixtures_path}")
    except Exception as e:
        print(f"⚠️  示例数据导入失败: {e}")
    
    # 4. 创建测试用户
    print("\n[4/4] 创建测试用户...")
    try:
        from video.models import User as VideoUser
        if not VideoUser.objects.filter(username='test').exists():
            VideoUser.objects.create(
                username='test',
                password='test123'
            )
            print("✓ 测试用户创建成功")
            print("  用户名: test")
            print("  密码: test123")
        else:
            print("✓ 测试用户已存在")
    except Exception as e:
        print(f"⚠️  创建测试用户失败: {e}")
    
    print("\n" + "=" * 50)
    print("数据库初始化完成！")
    print("=" * 50)
    print("\n可以使用以下命令启动服务器:")
    print("  python manage.py runserver")
    print("\n访问地址:")
    print("  前台系统: http://127.0.0.1:8000/")
    print("  管理后台: http://127.0.0.1:8000/admin/")
    print("=" * 50)
    
    return True


if __name__ == '__main__':
    try:
        init_database()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n初始化失败: {e}")
        sys.exit(1)
