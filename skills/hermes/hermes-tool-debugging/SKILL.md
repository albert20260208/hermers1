---
name: hermes-tool-debugging
description: Debug why a registered tool is not available in Hermes Agent - tool registration vs toolset filtering
version: 1.0.0
tags: [hermes, debugging, tools]
---

# Hermes Tool Debugging

## Problem
A tool is registered in `tools/registry.py` but doesn't appear in the available tools list.

## Diagnostic Steps

### 1. Check if tool is registered
```bash
cd /root/.hermes/hermes-agent && source venv/bin/activate && python -c "
from tools.registry import registry
print('rag_search' in registry._tools)
"
```

### 2. Check if tool passes toolset filtering
```bash
cd /root/.hermes/hermes-agent && source venv/bin/activate && python -c "
from hermes_cli.tools_config import _get_platform_tools
from model_tools import get_tool_definitions
import yaml

with open('/root/.hermes/config.yaml') as f:
    config = yaml.safe_load(f)

enabled = _get_platform_tools(config, 'cli')
tools = get_tool_definitions(enabled_toolsets=list(enabled))
tool_names = [t['function']['name'] for t in tools]
print('rag_search' in tool_names)
"
```

### 3. Key insight: Toolset definitions vs tool registration
Tools must be registered AND included in a toolset to be available.

**Common issue**: `toolsets.py` defines toolsets like:
```python
"memory": {
    "tools": ["memory"],  # RAG tools missing!
    ...
}
```

But the actual tool registration in `rag_tools.py` registers `rag_search`, `rag_add_memory`, `rag_stats` under toolset `"memory"`.

**Fix**: Update the toolset definition in `toolsets.py`:
```python
"memory": {
    "tools": ["memory", "rag_search", "rag_add_memory", "rag_stats"],
    ...
}
```

## Session Cache Issue
After fixing, existing CLI sessions still have cached old tools. Start a new session:
```
/new
```
or
```
/clear
```

## File locations
- Tool definitions: `/root/.hermes/hermes-agent/toolsets.py`
- Tool registration: `/root/.hermes/hermes-agent/tools/rag_tools.py`
- Registry: `/root/.hermes/hermes-agent/tools/registry.py`
- Model tools (discovery): `/root/.hermes/hermes-agent/model_tools.py`
