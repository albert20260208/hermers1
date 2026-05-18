#!/bin/bash
# OpenClaw Obsidian Vault 自动同步脚本
# 版本：v1.0
# 创建时间：2026-04-04
# 用途：自动同步 Obsidian Vault 到 Git 仓库

# 配置变量
VAULT_DIR="/root/.openclaw/workspace/obsidian-vault"
LOG_FILE="/root/.openclaw/workspace/obsidian-vault/sync.log"
REMOTE_NAME="origin"
BRANCH_NAME="main"

# 进入仓库目录
cd "$VAULT_DIR" || {
    echo "[ERROR] 无法进入仓库目录: $VAULT_DIR"
    exit 1
}

# 记录开始时间
START_TIME=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$START_TIME] 开始同步检查..." >> "$LOG_FILE"

# 1. 检查是否有未提交的更改
if git status --porcelain | grep -q '.'; then
    echo "[INFO] 检测到文件更改，开始同步流程..." | tee -a "$LOG_FILE"
    
    # 2. 添加所有更改的文件（包括新文件和修改的文件）
    echo "[INFO] 添加所有更改到暂存区..." | tee -a "$LOG_FILE"
    git add .
    
    # 3. 提交更改
    COMMIT_MSG="自动同步: $START_TIME UTC"
    echo "[INFO] 提交更改: $COMMIT_MSG" | tee -a "$LOG_FILE"
    if git commit -m "$COMMIT_MSG"; then
        echo "[SUCCESS] 提交成功" | tee -a "$LOG_FILE"
        
        # 4. 检查是否已设置远程仓库
        if git remote | grep -q "$REMOTE_NAME"; then
            echo "[INFO] 检测到远程仓库 '$REMOTE_NAME'，开始推送..." | tee -a "$LOG_FILE"
            
            # 5. 推送到远程仓库
            if git push "$REMOTE_NAME" "$BRANCH_NAME"; then
                echo "[SUCCESS] 推送成功" | tee -a "$LOG_FILE"
                RESULT="同步完成（包含推送）"
            else
                echo "[WARNING] 推送失败，但本地提交已保存" | tee -a "$LOG_FILE"
                RESULT="同步完成（仅本地提交，推送失败）"
            fi
        else
            echo "[INFO] 未设置远程仓库，仅保存本地提交" | tee -a "$LOG_FILE"
            echo "[HINT] 请使用以下命令设置远程仓库：" | tee -a "$LOG_FILE"
            echo "[HINT]   git remote add origin <远程仓库URL>" | tee -a "$LOG_FILE"
            echo "[HINT]   git push -u origin main" | tee -a "$LOG_FILE"
            RESULT="同步完成（仅本地提交，无远程仓库）"
        fi
    else
        echo "[ERROR] 提交失败" | tee -a "$LOG_FILE"
        RESULT="同步失败（提交错误）"
    fi
else
    echo "[INFO] 无文件更改，跳过同步" | tee -a "$LOG_FILE"
    RESULT="无更改需要同步"
fi

# 记录结束时间和结果
END_TIME=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$END_TIME] 同步结束: $RESULT" >> "$LOG_FILE"

# 输出摘要
echo "========================================" | tee -a "$LOG_FILE"
echo "同步摘要: $RESULT" | tee -a "$LOG_FILE"
echo "开始时间: $START_TIME" | tee -a "$LOG_FILE"
echo "结束时间: $END_TIME" | tee -a "$LOG_FILE"
echo "日志文件: $LOG_FILE" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"