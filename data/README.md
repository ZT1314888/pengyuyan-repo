# 数据目录说明

本目录包含项目的数据文件和数据处理脚本。

## 📁 文件说明

### 数据备份文件
- `database_backup.sql` - 完整的数据库备份文件（SQL格式）
- `fixtures.json` - Django格式的数据备份（JSON格式）

### 原始数据文件
- `data.csv` - 视频数据
- `comment_data.csv` - 评论数据
- `nlp_result.csv` - NLP分析结果

### 数据处理脚本
- `csv_to_sql.py` - CSV数据导入到数据库
- `data_analysis.py` - 数据分析脚本
- `nlp.py` - 自然语言处理脚本
- `wordCloud.py` - 词云生成脚本
- `spider.py` - 视频数据爬虫
- `spider_comment.py` - 评论数据爬虫

### 其他文件
- `stopwords_baidu.txt` - 中文停用词表
- `addresses.json` - 地址数据
- `countries.json` - 国家数据
- `XB.js` - JavaScript工具文件

## 🚀 快速开始

### 方式1：导入SQL备份（推荐）

1. 确保已创建数据库
2. 配置好 `config.py`
3. 运行导入脚本：
```bash
python import_sql.py
```

### 方式2：使用初始化脚本

运行项目根目录的初始化脚本：
```bash
python init_database.py
```

### 方式3：手动导入

使用MySQL命令行：
```bash
mysql -u用户名 -p密码 数据库名 < data/database_backup.sql
```

## 📊 数据表结构

### video_videodata（视频数据表）
- `aweme_id` - 视频ID
- `username` - 用户名
- `likeCount` - 点赞数
- `collectCount` - 收藏数
- `commentCount` - 评论数
- `shareCount` - 分享数
- `downloadCount` - 下载数
- 其他字段...

### video_commentdata（评论数据表）
- `userid` - 用户ID
- `username` - 用户名
- `commentTime` - 评论时间
- `userIP` - 用户IP
- `likeCount` - 点赞数
- 其他字段...

### video_user（用户表）
- `username` - 用户名
- `password` - 密码
- `createTime` - 创建时间

## 🔄 数据导出

如果你修改了数据并想要导出：

```bash
# 导出为SQL格式
python export_sql.py

# 导出为JSON格式
python export_data.py
```

## ⚠️ 注意事项

1. **数据隐私**
   - 如果数据包含真实用户信息，请不要上传到公开仓库
   - 可以使用脱敏数据或示例数据替代

2. **文件大小**
   - SQL备份文件可能较大，注意Git仓库大小限制
   - 可以使用Git LFS管理大文件

3. **字符编码**
   - 所有数据文件使用UTF-8编码
   - 导入时确保数据库字符集为utf8mb4

4. **数据完整性**
   - 导入前请备份现有数据
   - 确保数据库版本兼容

## 📝 数据来源

本项目的数据来源于：
- 抖音公开数据（需遵守平台规则）
- 示例数据（用于演示）

**请遵守相关法律法规和平台规则，不要滥用数据。**

## 🤝 贡献数据

如果你有更好的示例数据，欢迎贡献：
1. Fork项目
2. 添加你的数据文件
3. 提交Pull Request

---

**数据使用请遵守相关法律法规！**
