## 🔔 重要提醒规则

⚠️ **重要**: 选择工作流前，先阅读 [deerflow_WORKFLOWS_INDEX.md](./deerflow_WORKFLOWS_INDEX.md)

### 下次制作视频时必须执行的步骤

1. **第一时间阅读工作流索引**
   ```bash
   cat /root/.openclaw/workspace/projects/deerflow_WORKFLOWS_INDEX.md
   ```

2. **查看完整目录结构**
   ```bash
   cat /root/.openclaw/workspace/projects/deerflow+dreamina_DIRECTORIES.md
   ```

2. **检查 DeerFlow 服务状态**
   ```bash
   cd /root/.openclaw/workspace/projects/deerflow-integration/deerflow-repo
   make status
   ```

3. **确认 Dreamina 积分余额**
   ```bash
   dreamina user_credit
   ```

4. **根据决策树选择工作流**
   - 商业广告 → 半自动工作流（`workflow-ad`）
   - 批量生成 → 全自动工作流（`workflow-auto`）
   - 详见: [deerflow_WORKFLOWS_INDEX.md](./deerflow_WORKFLOWS_INDEX.md)

5. **启动选定的工作流**
   ```bash
   # 半自动广告工作流
   cd /root/.openclaw/workspace/projects/ad-workflow
   python workflows/ad_creation_workflow.py
   
   # 全自动视频工作流
   cd /root/.openclaw/workspace/projects/auto-video-generation
   bash start_generation.sh
   ```

---

**此规则已记录到**: 
- `/root/.openclaw/workspace/projects/deerflow_WORKFLOWS_INDEX.md` - 工作流索引（新增）
- `/root/.openclaw/workspace/projects/deerflow+dreamina_DIRECTORIES.md` - 完整目录
