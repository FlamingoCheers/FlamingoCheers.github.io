# 两只火烈鸟 · Flamingo Cheers

个人站点：<https://flamingocheers.github.io/>

仓库：<https://github.com/FlamingoCheers/FlamingoCheers.github.io>

本站用 Hugo（Extended 0.163.3）+ PaperMod 构建，通过 GitHub Actions 从 `main` 分支自动部署到 GitHub Pages。站点只有两个内容区：**研究**（长文专题）与**文章**（单篇随笔），另有独立的「关于」页。

---

## 给 AI / 维护者的第一条规则

**新增或修改内容时，只改 `content/` 与 `static/downloads/`。**

`layouts/`、`assets/css/extended/`、`hugo.toml`、`themes/` 是站点架构。除非用户明确要求改版，否则不要改动它们；不要新增主题、插件、Web Font，也不要恢复 `content/posts/`、`gh-pages` 分支或旧的发布脚本。

改完后必须本地构建一次，确认没有 ERROR，再提交。构建命令见[构建与发布](#构建与发布)。

---

## 目录结构

```text
.
├─ hugo.toml                     # 站点配置：菜单、permalink、语言、PaperMod 参数
├─ content/
│  ├─ _index.md                  # 首页 front matter（首页模板不读取正文，改这里不会改变首页）
│  ├─ about.md                   # 关于页（layout: about）
│  ├─ archives.md                # 归档页
│  ├─ search.md                  # 搜索页
│  ├─ research/
│  │  ├─ _index.md               # 研究总览页的标题与说明
│  │  └─ regime-stability/       # 一个研究专题（series）
│  │     ├─ _index.md            # 专题首页：标题、摘要、日期、weight、status
│  │     ├─ 01-xu-yu-fangfa.md
│  │     ├─ 02-san-dai-yu-xian-qin.md
│  │     ├─ …
│  │     └─ 12-fu-lu.md
│  └─ writing/
│     ├─ _index.md               # 文章索引页
│     ├─ ai-era-work-meaning.md
│     └─ changchun-changbaishan-travel-guide.md
├─ layouts/
│  ├─ home.html                  # 首页：全屏站名 + 最新发布 + 研究/文章索引
│  ├─ single.html                # 文章 / 研究章节 / 关于 三种详情页
│  ├─ research/list.html         # /research/ 总览 与 /research/<专题>/ 目录
│  ├─ writing/list.html          # /writing/ 文章索引
│  └─ _partials/header.html      # 自定义页头与导航高亮
├─ assets/css/extended/site.css  # 全站视觉：朱砂强调色、排版、暗色模式
├─ static/downloads/
│  └─ zhengquan-wenguodu-yanjiu-baogao.docx
├─ .github/workflows/hugo.yml    # push main → hugo build → deploy Pages
└─ themes/PaperMod/              # 上游主题，不要修改
```

`public/`、`public_test/`、`public_debug/` 是构建产物，已在 `.gitignore` 中忽略，不要提交。

---

## 内容模型

| 区域 | 目录 | URL | 说明 |
|---|---|---|---|
| 研究总览 | `content/research/_index.md` | `/research/` | 列出所有研究专题 |
| 研究专题 | `content/research/<专题slug>/_index.md` | `/research/<专题slug>/` | 多章长文；每一章自动进入专题目录 |
| 研究章节 | `content/research/<专题slug>/NN-*.md` | `/research/<专题slug>/NN-*/` | 文件名即 URL，发布后不要改名 |
| 文章索引 | `content/writing/_index.md` | `/writing/` | 按年份分组列出所有文章 |
| 文章 | `content/writing/<文件名>.md` | `/writing/<slug>/` | 必须写 `slug` |
| 关于 | `content/about.md` | `/about/` | `layout: "about"` |

首页、专题目录、文章索引都由模板自动生成，新增内容后不需要手工改列表。

### 首页「最新发布」的判定

首页把所有 `writing` 文章和所有**研究专题的 `_index.md`**（不包含单章）按 `date` 排序，取最新的一条。因此：

- 发新文章 → 自动成为「最新发布」。
- 发布新专题 → 自动成为「最新发布」。
- 只给已有专题加章节 → **不会**自动变成最新；若希望它重新出现在最新位，更新该专题 `_index.md` 的 `date`。

首页最多列出 5 篇文章；研究区列出全部专题（按 `weight`）。

---

## 新增一篇文章

在 `content/writing/` 新建 `<英文文件名>.md`：

```yaml
---
title: "文章标题"
slug: "english-url-slug"
date: 2026-11-01T12:00:00+08:00
draft: false
author: "夏渡云"
description: "一句话摘要，会显示在列表和首页最新发布里。"
tags: ["标签1", "标签2", "标签3"]
categories: ["思考"]
aliases: ["/2026/11/旧标题路径/"]   # 仅当需要兼容旧链接时添加
ShowToc: true                        # 可选；文章默认不显示目录
---

正文……
```

规则：

1. **`slug` 必填**，且只用小写英文字母、数字、连字符。`hugo.toml` 的 `[permalinks] writing = '/writing/:slug/'` 依赖它；没有 `slug` 时 Hugo 会用中文标题生成 URL。
2. `categories` 只用现有分类：`思考`、`AI`、`阅读`、`旅行`、`札记`（可新增，但文章索引顶部的筛选会自动读取全站分类）。
3. `tags` 建议 3–5 个，不要用弯引号包裹；YAML 里统一用双引号。
4. `date` 必须是带时区的完整时间（`+08:00`）。首页「最新发布」和文章排序都依赖它。
5. 文章 TOC 由 `ShowToc: true` 控制；研究章节的 TOC 默认显示。
6. 如果文章地址发生变化，保留旧 `aliases`，不要删除。

---

## 新增一个研究专题

1. 建目录 `content/research/<专题slug>/`（slug 用英文小写与连字符）。
2. 建 `_index.md`：

```yaml
---
title: "专题标题"
date: 2026-11-01T12:00:00+08:00
draft: false
author: "夏渡云"
description: "专题摘要，会显示在首页与研究总览。"
tags: ["标签1", "标签2"]
weight: 20                 # 专题排序；现有专题是 10，下一个用 20
status: "已完成"           # 可选，显示在首页/专题页
---
专题导言。这里可以写研究问题、主要发现、阅读方式。
```

3. 章节文件命名为 `01-english-slug.md`、`02-…`，每章 front matter：

```yaml
---
title: "第一章 标题"
date: 2026-11-01T12:00:00+08:00
draft: false
author: "夏渡云"
description: "本章摘要，会显示在专题目录。"
tags: ["标签1", "标签2"]
series: ["专题标题"]        # 与 _index.md 的 title 一致
weight: 110                 # 章节排序，建议 专题weight*10 + 章号
ShowToc: true
TocOpen: false
chapter: "01"               # 目录左侧显示的章节号
group: "问题与方法"          # 目录分组；新分组会自动出现
aliases: ["/research/旧地址/"]  # 仅在改过 URL 时添加
---
```

规则：

1. `group` 决定专题页的分组与顺序。现有分组：`问题与方法`、`个案研究`、`统计与机制`、`结语与附录`。分组顺序按章节 `weight` 首次出现顺序生成；新增分组会追加。
2. `chapter` 是展示用编号（`"01"`），与文件名、`weight` 无关；三处要保持一致，避免顺序错乱。
3. 章节页的「上一章 / 下一章」按 section 顺序生成（模板内部使用 `NextInSection` / `PrevInSection`，方向已校正）。不要手工在正文末尾写上一章/下一章。
4. 专题页会自动统计章数、总字数、日期、`status`，并显示 DOCX 下载。下载块里的「约 2.8 万字」是静态文案，若替换 DOCX 需同步修改 `layouts/research/list.html` 第 52 行。
5. 研究章节**不要**写 `categories`；分类只用于文章。

### 给已有专题加一章

- 文件名继续顺延（如 `13-…md`），`weight` 顺延，`chapter` 填 `"13"`，`series` 与专题一致。
- 专题页的章数、字数、目录自动更新。
- 若希望此专题重新登上首页「最新发布」，更新专题 `_index.md` 的 `date`。

---

## 模板与页面逻辑（改版时才需要看）

### 首页 `layouts/home.html`

- 全屏 `.hero` 只显示中文站名（`site.Title`）与英文名（`site.Params.siteNameEn`）。
- 「最新发布」块带固定徽标「最新发布」，类型显示「研究」或「文章」。
- 研究区读取 `site.GetPage "/research"` 的 `.Sections.ByWeight`，编号取 `weight / 10`。
- 文章区取 `writing` 最新 5 篇。
- 首页**不渲染** `content/_index.md` 的正文。

### 研究 `layouts/research/list.html`

- `.Parent.IsHome` 为真 → 研究总览；否则 → 专题目录。
- 专题目录按 `Params.group` 动态分组，组内按 `weight` 排序。
- 统计字数来自章节 `WordCount` 之和。

### 文章 `layouts/writing/list.html`

- 按 `date` 年份分组，组内倒序；顶部筛选读取 `site.Taxonomies.categories`。

### 详情页 `layouts/single.html`

- `layout: "about"` → 关于页。
- `Section == "research"` → 研究章节：章节号、折叠 TOC、上一章/下一章。
- 其余 → 文章：日期、分类、阅读时间、可选 TOC、文末标签。

### 样式 `assets/css/extended/site.css`

- PaperMod 会自动把 `assets/css/extended/*.css` 打包进全站样式，无需额外引用。
- 主题色变量：`--site-accent: #9a3b2c`（亮色）/ `#c98677`（暗色）。只把它用于编号、hover、当前导航等小面积强调。
- 全站沿用系统字体栈，不引入 Web Font。
- 暗色模式由 `:root[data-theme="dark"]` 控制（PaperMod 在 `<html>` 上设置 `data-theme`，不是 `.dark` class）。
- 布局宽度：正文 760px，首页/列表 960px；移动端断点 640px。

---

## 配置要点 `hugo.toml`

- `title = '两只火烈鸟'`，`params.siteNameEn = 'Flamingo · Cheers'`。
- 四项导航固定为：首页 `/`、研究 `/research/`、文章 `/writing/`、关于 `/about/`。
- `mainSections = ["writing"]`。
- `[permalinks] writing = '/writing/:slug/'`。
- `defaultContentLanguage = 'zh-cn'`、`locale = 'zh-CN'`、`hasCJKLanguage = true`（中文字数统计）。
- `[outputs] home = ["HTML", "RSS", "JSON"]`（搜索索引）。
- `public_test` / `public_debug` 仅供本地验证。

---

## 构建与发布

### 本地构建

```powershell
$site = "C:\Users\Administrator\AppData\Local\Temp\opencode\ghpages"
$hugo = "C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe"
& $hugo --source $site --destination "$site\public_test" --gc --minify --cleanDestinationDir
```

要求：`Pages`、`Aliases` 正常输出，且没有 `ERROR`。主题自身的 `LanguageDirection` / `LanguageCode` 弃用警告可忽略。

### 部署

推送到 `main` 后，`.github/workflows/hugo.yml` 自动执行：

1. `actions/checkout@v5`
2. `peaceiris/actions-hugo@v3`（Hugo 0.163.3 extended）
3. `hugo --gc --minify --baseURL "https://FlamingoCheers.github.io/"`
4. 上传 `public/` 并用 `actions/deploy-pages@v5` 发布

**不要**提交 `public/`，**不要**使用 `gh-pages` 分支，**不要**恢复 `scripts/fix_chinese_quotes.py` 到工作流（该脚本依赖已删除的 `content/posts/`，会让部署失败）。

### 网络备注

当前机器直连 `github.com:443` 可能被重置，但 `api.github.com` 可用。若 `git push` 超时，可用 `gh api` 的 Git Data API 推送（blob → tree → commit → 更新 ref），推送前必须确认新 tree 与本地 `git rev-parse HEAD^{tree}` 一致。不要为此改写提交历史。

曾因 API 推送导致本地 `HEAD` 与远程 `main` 的 SHA 不同但 tree 相同；重新克隆或以远程 `main` 为基线即可，不要在旧历史上强推。

---

## 发布前验收清单

- [ ] `content/` 中没有 `draft: true` 的待发内容。
- [ ] 新文章有英文 `slug`，URL 为 `/writing/<slug>/`。
- [ ] 新章节的 `chapter`、`weight`、`series`、`group` 连续且与专题一致。
- [ ] 改过 URL 的内容保留了旧 `aliases`。
- [ ] 本地构建无 ERROR；首页「最新发布」指向预期页面。
- [ ] `/research/`、`/research/<专题>/`、`/writing/`、新详情页、旧别名地址均可打开。
- [ ] 暗色模式与移动端（640px 以下）没有横向滚动。
- [ ] 只提交了 `content/`、`static/` 及确需变更的模板/CSS，未提交 `public*/`。

---

## 常见坑

1. **Windows PowerShell 5.1 写 UTF-8 会带 BOM**，Hugo 报 `toml: invalid character at start of key: ï`。修改 `hugo.toml` 用编辑器/`edit` 工具；必须用脚本写时使用 `New-Object System.Text.UTF8Encoding($false)`。
2. **PowerShell 控制台显示中文可能乱码**，但文件本身通常是 UTF-8；检查中文内容优先用编辑器的读取工具。
3. **`hugo --minify` 会去掉 HTML 属性引号**，用文本搜索验证时匹配 `class=hero-title` 这类裸写法。
4. **文章没有 `slug` 就会用中文标题做 URL**；这是最容易破坏链接的改动。
5. **不要给研究章节加 `categories`**；分类筛选只应包含文章。
6. **不要手工改 `themes/PaperMod/`**；升级主题会覆盖。站点定制只放在根目录 `layouts/` 与 `assets/css/extended/site.css`。
7. **不要运行旧的 `publish.ps1`**：它属于已废弃的 `gh-pages` 发布方式，会清空工作区并把构建产物推到 `gh-pages`。本站只用 GitHub Actions。
8. **旧文章地址**通过 Hugo `aliases` 生成 meta-refresh 页面（HTTP 200），不是 301；这是预期行为。
9. **首页最新发布取专题的日期**，不是章节日期；加章节后专题不会自动回到最新位。

---

## 许可

- 代码：MIT
- 文章与研究内容：CC BY-NC-ND 4.0
