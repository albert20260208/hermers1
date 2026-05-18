---
name: vision-local-image-debugging
description: Vision本地图片分析故障排查 - 当vision_analyze无法读取本地缓存图片时的正确处理方法
---

# Vision 本地图片分析故障排查

## 触发条件

vision_analyze 工具报错 "I cannot see the image" 或 "Invalid image source"，但图片文件确实存在。

## 根本原因

vision_analyze 服务端跑在远程服务器，**无法访问本机的 `/root/.hermes/image_cache/` 目录**。即使文件是有效JPEG，远程也无法读取。

## 排查步骤

1. **验证文件存在且有效**（用 execute_code 读文件头）：
   ```python
   with open("/root/.hermes/image_cache/img_xxx.jpg", "rb") as f:
       data = f.read()
   print(f"Size: {len(data)}, First bytes: {data[:20]}")
   # 有效JPEG应以 \xff\xd8 开头
   ```

2. **如果文件有效但 vision 仍读不到**，说明是服务端访问权限问题，不是文件损坏

## 正确解法（二选一）

1. **让用户直接在聊天窗口拖拽重新发图片** — 这是最简单的方式，图片会作为新的消息附件到达，vision工具能正确读取
2. **提供公网URL** — 把图片上传到可访问的公网地址，vision_analyze 支持 HTTP/HTTPS URL

## 禁忌

- 不要依赖 `/root/.hermes/image_cache/` 路径让 vision 读图 — 必定失败
- 不要尝试用本地HTTP服务器（localhost）— vision服务端在另一台机器，访问不到
- 不要反复 patch 文件路径 — 改变的是客户端路径，远程仍然读不到
