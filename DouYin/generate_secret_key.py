"""
生成Django SECRET_KEY的脚本
运行此脚本生成一个新的随机密钥
"""
from django.core.management.utils import get_random_secret_key

def generate_key():
    """生成新的SECRET_KEY"""
    print("=" * 60)
    print("Django SECRET_KEY 生成器")
    print("=" * 60)
    
    # 生成新密钥
    new_key = get_random_secret_key()
    
    print("\n✓ 已生成新的SECRET_KEY:\n")
    print(f"SECRET_KEY = '{new_key}'")
    
    print("\n" + "=" * 60)
    print("使用方法：")
    print("=" * 60)
    print("\n方式1：直接修改 settings.py")
    print(f"  将上面的密钥复制到 dy_project/settings.py 中")
    
    print("\n方式2：使用环境变量（推荐）")
    print("  1. 复制 .env.example 为 .env")
    print("  2. 在 .env 中设置：")
    print(f"     DJANGO_SECRET_KEY={new_key}")
    
    print("\n方式3：使用系统环境变量")
    print("  Windows:")
    print(f"    set DJANGO_SECRET_KEY={new_key}")
    print("  Linux/Mac:")
    print(f"    export DJANGO_SECRET_KEY={new_key}")
    
    print("\n" + "=" * 60)
    print("⚠️  重要提醒：")
    print("=" * 60)
    print("1. 不要将SECRET_KEY提交到Git仓库")
    print("2. 生产环境必须使用强密钥")
    print("3. 定期更换密钥以提高安全性")
    print("=" * 60)

if __name__ == '__main__':
    try:
        generate_key()
    except ImportError:
        print("错误：请先安装Django")
        print("运行：pip install django")
