---
name: github-secret-cleanup-push
description: 当 GitHub push 被 secret-scanning GH013 拦截时，清理敏感信息并完成推送的完整流程
---

# GitHub Secret 清理与推送流程

## 触发场景
向 GitHub push 时被 GH013 / secret-scanning 拦截，原因是 commit 中包含敏感信息（token、secret key、签名 URL 等）

## 完整流程

### 1. 诊断拦截原因
```bash
git push 2>&1
# 输出会列出: secret 类型、所在文件、commit hash
```

### 2. 清理敏感信息
```bash
# GitHub PAT / Token 模式
sed -i 's/ghp_[A-Za-z0-9._-]*/ghp_REDACTED_TOKEN/g' <file>

# VolcEngine / 阿里云 TOS 签名 URL
sed -i 's/X-Tos-Credential=[^&]*/X-Tos-Credential=REDACTED/g' <file>
sed -i 's/X-Tos-Signature=[^&]*/X-Tos-Signature=REDACTED/g' <file>

# AWS Access Key
sed -i 's/AKIA[A-Z0-9]\{16\}/AKIA_REDACTED/g' <file>
```

### 3. 提交清理结果
```bash
git add -A
git commit --amend --no-edit   # 修改最后一个 commit，避免新 commit 再次带 secret
```

### 4. 推送
```bash
GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no" git push
```
> `StrictHostKeyChecking=no` 绕过 SSH known_hosts 问题（服务器首次连接 GitHub 时 known_hosts 文件为空会失败）

### 5. 预防
- 敏感信息不要进 git，优先用环境变量
- `.gitignore` 排除 `.env`、`*secret*`、`*token*` 等文件
- 已 push 的 token 立即在 GitHub Settings → Tokens 页面 revoke

## 关键教训
- `--amend` 比新 commit 再 push 更干净（避免形成带 secret 的 commit 历史）
- 如果 push 前发现文件有 secret，直接 `git rm --cached <file>` + 新 commit 再 push
