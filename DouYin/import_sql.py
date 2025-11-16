"""
SQL数据导入脚本
从SQL文件导入数据到数据库
"""
import subprocess
import os
from config import Config

def import_from_sql():
    """从SQL文件导入数据"""
    print("=" * 50)
    print("开始导入数据库...")
    print("=" * 50)
    
    # SQL文件路径
    sql_file = 'data/database_backup.sql'
    
    # 检查文件是否存在
    if not os.path.exists(sql_file):
        print(f"✗ 错误: 未找到SQL文件: {sql_file}")
        print("\n请先运行导出脚本:")
        print("  python export_sql.py")
        return
    
    # 构建mysql命令
    cmd = [
        'mysql',
        '-h', Config.DB_HOST,
        '-P', str(Config.DB_PORT),
        '-u', Config.DB_USER,
        f'-p{Config.DB_PASSWORD}',
        '--default-character-set=utf8mb4',
        Config.DB_NAME
    ]
    
    try:
        print(f"\n正在导入数据到数据库: {Config.DB_NAME}")
        print(f"从文件: {sql_file}\n")
        
        # 执行导入
        with open(sql_file, 'r', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdin=f,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
        
        if result.returncode == 0:
            print("✓ 数据导入成功!")
            
            print("\n" + "=" * 50)
            print("导入完成！")
            print("=" * 50)
            print("\n可以使用以下命令启动服务器:")
            print("  python manage.py runserver")
            print("\n访问地址:")
            print("  前台系统: http://127.0.0.1:8000/")
            print("  管理后台: http://127.0.0.1:8000/admin/")
            print("=" * 50)
        else:
            print(f"✗ 导入失败: {result.stderr}")
            print("\n请确保:")
            print("1. 数据库已创建")
            print("2. 数据库配置正确")
            print("3. 有足够的权限")
            
    except FileNotFoundError:
        print("✗ 错误: 未找到mysql命令")
        print("\n请安装MySQL客户端工具:")
        print("  Windows: 安装MySQL或MariaDB")
        print("  Linux: sudo apt-get install mysql-client")
        print("  macOS: brew install mysql-client")
    except Exception as e:
        print(f"✗ 导入失败: {e}")


if __name__ == '__main__':
    try:
        import_from_sql()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n\n错误: {e}")
