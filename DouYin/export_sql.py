"""
SQL数据导出脚本
将数据库导出为SQL文件，更适合包含特殊字符的数据
"""
import subprocess
import os
from config import Config

def export_to_sql():
    """导出数据库为SQL文件"""
    print("=" * 50)
    print("开始导出数据库...")
    print("=" * 50)
    
    # 输出文件路径
    output_file = 'data/database_backup.sql'
    
    # 确保data目录存在
    os.makedirs('data', exist_ok=True)
    
    # 构建mysqldump命令
    cmd = [
        'mysqldump',
        '-h', Config.DB_HOST,
        '-P', str(Config.DB_PORT),
        '-u', Config.DB_USER,
        f'-p{Config.DB_PASSWORD}',
        '--default-character-set=utf8mb4',
        '--single-transaction',
        '--skip-lock-tables',
        Config.DB_NAME
    ]
    
    try:
        print(f"\n正在导出数据库: {Config.DB_NAME}")
        print(f"导出到: {output_file}\n")
        
        # 执行导出
        with open(output_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
        
        if result.returncode == 0:
            file_size = os.path.getsize(output_file)
            print(f"✓ 数据导出成功!")
            print(f"  文件路径: {output_file}")
            print(f"  文件大小: {file_size / 1024:.2f} KB")
            
            print("\n" + "=" * 50)
            print("导出完成！")
            print("=" * 50)
            print("\n其他用户可以使用以下命令导入数据:")
            print(f"  mysql -u用户名 -p密码 数据库名 < {output_file}")
            print("\n或使用导入脚本:")
            print("  python import_sql.py")
            print("=" * 50)
        else:
            print(f"✗ 导出失败: {result.stderr}")
            print("\n请确保:")
            print("1. 已安装MySQL客户端工具")
            print("2. mysqldump命令在系统PATH中")
            print("3. 数据库配置正确")
            
    except FileNotFoundError:
        print("✗ 错误: 未找到mysqldump命令")
        print("\n请安装MySQL客户端工具:")
        print("  Windows: 安装MySQL或MariaDB")
        print("  Linux: sudo apt-get install mysql-client")
        print("  macOS: brew install mysql-client")
    except Exception as e:
        print(f"✗ 导出失败: {e}")


if __name__ == '__main__':
    try:
        export_to_sql()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n\n错误: {e}")
