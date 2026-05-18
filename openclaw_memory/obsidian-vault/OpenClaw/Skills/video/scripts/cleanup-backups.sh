#!/bin/bash
# VIDEO技能目录备份清理脚本
# 用法: ./cleanup-backups.sh [天数]
# 默认清理超过30天的备份文件

DAYS=${1:-30}
VIDEO_DIR="/root/.openclaw/workspace/skills/video"
BACKUP_DIR="$VIDEO_DIR/备份"
PROJECT_BACKUP_DIRS=(
    "$VIDEO_DIR/projects/偏爱难藏-硅谷AI版/备份"
    "$VIDEO_DIR/projects/clara-divorce/备份"
)

echo "=== VIDEO技能目录备份清理 ==="
echo "清理标准: 超过 ${DAYS} 天的备份文件"
echo ""

# 清理主备份目录
echo "1. 清理主备份目录: $BACKUP_DIR"
if [ -d "$BACKUP_DIR" ]; then
    find "$BACKUP_DIR" -name "*.bak" -type f -mtime +$DAYS -ls -delete 2>/dev/null
    echo "   ✓ 主备份目录清理完成"
else
    echo "   ⚠ 主备份目录不存在"
fi

# 清理项目备份目录
echo ""
echo "2. 清理项目备份目录"
for dir in "${PROJECT_BACKUP_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "   清理: $dir"
        find "$dir" -type f -mtime +$DAYS -ls -delete 2>/dev/null
    fi
done

# 清理项目目录中的旧README备份
echo ""
echo "3. 清理项目目录中的旧README备份"
find "$VIDEO_DIR/projects" -name "README.md.backup.*" -type f -mtime +$DAYS -ls -delete 2>/dev/null
find "$VIDEO_DIR/projects" -name "README.md.old" -type f -mtime +$DAYS -ls -delete 2>/dev/null
find "$VIDEO_DIR/projects" -name "*.md.backup.*" -type f -mtime +$DAYS -ls -delete 2>/dev/null

echo ""
echo "=== 清理完成 ==="
echo "下次运行: $(date -d "+7 days" +%Y-%m-%d)"
