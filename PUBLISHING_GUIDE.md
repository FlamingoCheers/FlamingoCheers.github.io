# 博客发布指南

## 发布新文章

### 方法一：使用 Hugo 命令（推荐）

```bash
# 进入博客目录
cd blog

# 创建新文章（替换 your-article-title 为你的文章标题）
hugo new posts/your-article-title.md
```

这会创建 `content/posts/your-article-title.md` 文件，包含默认的前置元数据。

### 方法二：手动创建

在 `content/posts/` 目录下创建 `.md` 文件，添加以下前置元数据：

```markdown
---
title: "文章标题"
date: 2026-07-02T19:40:00+08:00
draft: false
author: "你的名字"
description: "文章摘要，会显示在列表页"
tags: ["标签1", "标签2"]
categories: ["分类名"]
series: ["系列名"]  # 可选
---

你的文章内容...
```

## 文章前置元数据说明

| 字段 | 说明 | 必填 |
|------|------|------|
| `title` | 文章标题 | 是 |
| `date` | 发布日期 | 是 |
| `draft` | 是否为草稿（true/false） | 是 |
| `author` | 作者 | 否 |
| `description` | 文章摘要 | 建议填写 |
| `tags` | 标签列表 | 建议填写 |
| `categories` | 分类 | 建议填写 |
| `series` | 系列名称 | 可选 |

## 本地预览

```bash
# 启动本地服务器
hugo server -D

# 浏览器访问 http://localhost:1313
```

`-D` 参数会显示草稿文章。

## 发布到 GitHub Pages

### 首次发布

1. **创建 GitHub 仓库**
   - 在 GitHub 创建新仓库，命名为 `yourusername.github.io`
   - 不要勾选 "Initialize with README"

2. **初始化本地仓库并推送**
   ```bash
   cd blog
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/yourusername.github.io.git
   git push -u origin main
   ```

3. **启用 GitHub Pages**
   - 进入仓库 Settings → Pages
   - Source 选择 "GitHub Actions"
   - 保存后，每次 push 到 main 分支会自动部署

### 后续发布文章

```bash
# 1. 写文章
hugo new posts/my-new-article.md
# 编辑 content/posts/my-new-article.md

# 2. 本地预览（可选）
hugo server -D

# 3. 提交并推送
git add .
git commit -m "Add: 文章标题"
git push
```

推送后 GitHub Actions 会自动构建并部署，通常 1-2 分钟后访问你的站点即可看到新文章。

## 文章组织技巧

### 使用分类和标签

- **分类**：大类，如"思考"、"AI"、"阅读"、"旅行"
- **标签**：更细粒度，如"ChatGPT"、"日本旅行"、"心理学"

### 使用系列

如果文章是系列内容，使用相同的 `series` 值：

```markdown
---
series: "AI 使用指南"
---
```

系列文章会自动关联显示。

### 文章排序

- 默认按 `date` 降序排列（最新的在前）
- 可以在 front matter 中用 `weight` 字段自定义排序

## 自定义配置

### 修改站点信息

编辑 `hugo.toml`：

```toml
title = '你的博客名称'
description = '你的博客描述'
author = "你的名字"

# 社交链接
[[params.socialIcons]]
  name = "github"
  url = "https://github.com/yourusername"

[[params.socialIcons]]
  name = "email"
  url = "mailto:your@email.com"
```

### 更换主题

PaperMod 主题文档：https://github.com/adityatelange/hugo-PaperMod

## 常见问题

### Q: 文章没有显示？
- 检查 `draft: false`
- 检查日期是否在将来
- 运行 `hugo server -D` 查看草稿

### Q: 部署失败？
- 检查 GitHub Actions 日志
- 确保 `hugo.toml` 中的 `baseURL` 正确
- 确保 PaperMod 主题子模块已正确初始化

### Q: 如何删除文章？
```bash
# 删除文章文件
rm content/posts/article-name.md

# 提交更改
git add .
git commit -m "Remove: 文章标题"
git push
```

## 快速命令参考

```bash
# 创建文章
hugo new posts/article-name.md

# 本地预览
hugo server -D

# 构建生产版本
hugo --minify

# 查看草稿
hugo server -D

# 提交发布
git add .
git commit -m "Add: 文章标题"
git push
```
