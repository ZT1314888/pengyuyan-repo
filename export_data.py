"""
数据导出脚本
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dy_project.settings')
django.setup()

from django.core.management import call_command
import sys


def export_data():
    """导出数据库数据"""
    print("=" * 50)
    print("开始导出数据...")
    print("=" * 50)
    
    try:
        # 导出所有数据到fixtures.json
        output_file = 'data/fixtures.json'
        
        # 确保data目录存在
        os.makedirs('data', exist_ok=True)
        
        print(f"\n正在导出数据到: {output_file}")
        
        # 导出video应用的数据
        import io
        import sys
        
        # 临时修改标准输出编码
        old_stdout = sys.stdout
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
        try:
            call_command(
                'dumpdata',
                'video',  # 只导出video应用的数据
                '--indent', '2',  # 格式化JSON
                '--output', output_file,
                '--natural-foreign',  # 使用自然键
                '--natural-primary'  # 使用自然主键
            )
        finally:
            sys.stdout = old_stdout
        
        print(f"✓ 数据导出成功: {output_file}")
        
        # 获取文件大小
        file_size = os.path.getsize(output_file)
        print(f"  文件大小: {file_size / 1024:.2f} KB")
        
        print("\n" + "=" * 50)
        print("导出完成！")
        print("=" * 50)
        print("\n其他用户可以使用以下命令导入数据:")
        print("  python init_database.py")
        print("\n或手动导入:")
        print(f"  python manage.py loaddata {output_file}")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ 导出失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    try:
        export_data()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)
