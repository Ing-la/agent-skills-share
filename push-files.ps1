# 切换到脚本所在目录（项目根目录）
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "=== 当前 Git 状态 ===" -ForegroundColor Yellow
git status

Write-Host "`n=== 当前跟踪的文件 ===" -ForegroundColor Yellow
git ls-files

Write-Host "`n=== 移除所有已跟踪的文件 ===" -ForegroundColor Yellow
git rm -r --cached . 2>&1

Write-Host "`n=== 添加正确的文件 ===" -ForegroundColor Yellow
git add .gitignore
git add README.md
git add skill-share/
git add Agent-skills-share/

Write-Host "`n=== 检查添加的文件 ===" -ForegroundColor Yellow
git status --short

Write-Host "`n=== 提交更改 ===" -ForegroundColor Yellow
Write-Host "请输入提交信息（直接回车使用默认信息）:" -ForegroundColor Cyan
$commitMessage = Read-Host
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Update: Add skill-share and Agent-skills-share files"
}
git commit -m $commitMessage

Write-Host "`n=== 推送到 GitHub ===" -ForegroundColor Yellow
git push --force

Write-Host "`n=== 最终文件列表 ===" -ForegroundColor Green
git ls-files
