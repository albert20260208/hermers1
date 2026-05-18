#!/usr/bin/env python3
"""
RAG Memory Tools - Vector search over long-term memory

Provides rag_search, rag_add_memory, and rag_stats tools by wrapping
the cpu_rag memory provider's functionality as proper Hermes tools.

The cpu_rag plugin provides get_tool_schemas() and handle_tool_call() methods,
but those are only used by the memory provider interface - they don't get
registered as standalone chat tools. This module bridges that gap.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Lazy-loaded provider instance
_cpurag_provider = None


def _get_cpurag_provider() -> Any:
    """Lazily load and return the CPURAGMemoryProvider singleton."""
    global _cpurag_provider
    if _cpurag_provider is None:
        try:
            from plugins.memory.cpu_rag import CPURAGMemoryProvider
            _cpurag_provider = CPURAGMemoryProvider()
            logger.info("CPURAGMemoryProvider initialized for rag_tools")
        except Exception as e:
            logger.error(f"Failed to load CPURAGMemoryProvider: {e}")
            raise
    return _cpurag_provider


# --- Tool Schemas (re-exported from cpu_rag plugin) ---

try:
    from plugins.memory.cpu_rag import (
        RAG_SEARCH_SCHEMA,
        RAG_ADD_MEMORY_SCHEMA,
        RAG_STATS_SCHEMA,
    )
    _schemas_available = True
except ImportError as e:
    logger.warning(f"cpu_rag plugin not available: {e}")
    RAG_SEARCH_SCHEMA = {
        "name": "rag_search",
        "description": "RAG memory search (cpu_rag plugin not loaded)",
        "parameters": {"type": "object", "properties": {}, "required": []},
    }
    RAG_ADD_MEMORY_SCHEMA = {
        "name": "rag_add_memory",
        "description": "Add memory to RAG store (cpu_rag plugin not loaded)",
        "parameters": {"type": "object", "properties": {}, "required": []},
    }
    RAG_STATS_SCHEMA = {
        "name": "rag_stats",
        "description": "RAG stats (cpu_rag plugin not loaded)",
        "parameters": {"type": "object", "properties": {}, "required": []},
    }
    _schemas_available = False


# --- Tool Handlers ---

def _rag_search_handler(args: Dict[str, Any], **kwargs) -> str:
    """Handler for rag_search tool."""
    if not _schemas_available:
        return '{"error": "cpu_rag plugin not loaded"}'
    provider = _get_cpurag_provider()
    return provider.handle_tool_call("rag_search", args)


def _rag_add_memory_handler(args: Dict[str, Any], **kwargs) -> str:
    """Handler for rag_add_memory tool."""
    if not _schemas_available:
        return '{"error": "cpu_rag plugin not loaded"}'
    provider = _get_cpurag_provider()
    return provider.handle_tool_call("rag_add_memory", args)


def _rag_stats_handler(args: Dict[str, Any], **kwargs) -> str:
    """Handler for rag_stats tool."""
    if not _schemas_available:
        return '{"error": "cpu_rag plugin not loaded"}'
    provider = _get_cpurag_provider()
    return provider.handle_tool_call("rag_stats", args)


# --- Registry ---

from tools.registry import registry, tool_error

registry.register(
    name="rag_search",
    toolset="memory",
    schema=RAG_SEARCH_SCHEMA,
    handler=_rag_search_handler,
    emoji="🧠",
    description="Search long-term memory via vector similarity",
)

registry.register(
    name="rag_add_memory",
    toolset="memory",
    schema=RAG_ADD_MEMORY_SCHEMA,
    handler=_rag_add_memory_handler,
    emoji="💾",
    description="Save important information to vector memory",
)

registry.register(
    name="rag_stats",
    toolset="memory",
    schema=RAG_STATS_SCHEMA,
    handler=_rag_stats_handler,
    emoji="📊",
    description="View RAG memory statistics",
)
