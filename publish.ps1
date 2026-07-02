# 博客自动化发布脚本
# 用法：在 blog 目录下运行 .\publish.ps1 [-Message "提交信息"]
# 默认提交信息为当前日期

param(
    [string]$Message = (Get-Date -Format "yyyy-MM-dd")
)

$ErrorActionPreference = "Stop"

# Hugo 路径
$HugoExe = "C:\Users\Administrator\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe"
$BlogDir = $PSScriptRoot
$TempDir = Join-Path $env:TEMP "hugo_deploy_$(Get-Date -Format 'yyyyMMddHHmmss')"

Write-Host "=== 博客发布脚本 ===" -ForegroundColor Cyan

# 第 1 步：确保在 main 分支
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    Write-Host "切换到 main 分支..." -ForegroundColor Yellow
    git checkout main
}

# 第 2 步：修复中文引号
$fixScript = Join-Path $BlogDir "scripts\fix_chinese_quotes.py"
if (Test-Path $fixScript) {
    Write-Host "[1/7] 修复中文引号..." -ForegroundColor Green
    python $fixScript
} else {
    Write-Host "[1/7] 跳过引号修复（脚本不存在）" -ForegroundColor Yellow
}

# 第 3 步：Hugo 构建
Write-Host "[2/7] Hugo 构建站点..." -ForegroundColor Green
& $HugoExe --gc --minify --baseURL "https://FlamingoCheers.github.io/"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Hugo 构建失败！" -ForegroundColor Red
    exit 1
}

# 第 4 步：备份 public/ 到临时目录
Write-Host "[3/7] 备份构建产物..." -ForegroundColor Green
Copy-Item -Path (Join-Path $BlogDir "public") -Destination $TempDir -Recurse -Force

# 第 5 步：切换到 gh-pages 分支并部署
Write-Host "[4/7] 切换到 gh-pages 分支..." -ForegroundColor Green
git checkout gh-pages

# 清空工作区（保留 .git）
git rm -rf --cached . 2>$null
Get-ChildItem -Path $BlogDir -Force | Where-Object { $_.Name -ne ".git" } | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $BlogDir -Force -Filter ".*" | Where-Object { $_.Name -ne ".git" -and $_.Name -ne ".gitignore" } | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 复制 HTML 文件
Write-Host "[5/7] 复制 HTML 文件..." -ForegroundColor Green
Copy-Item -Path (Join-Path $TempDir "*") -Destination $BlogDir -Recurse -Force

# 第 6 步：提交并推送
Write-Host "[6/7] 提交并推送..." -ForegroundColor Green
git add -A
git commit -m $Message
git push origin gh-pages

# 第 7 步：切回 main 分支并清理
Write-Host "[7/7] 切回 main 分支..." -ForegroundColor Green
git checkout main

# 清理临时文件
Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "=== 发布完成！ ===" -ForegroundColor Cyan
Write-Host "访问 https://flamingocheers.github.io 查看效果" -ForegroundColor Cyan
