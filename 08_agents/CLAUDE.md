# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A small Python package of document-related tools exposed to AI assistants through an MCP server (FastMCP, server name `"docs"`). Document conversion is handled by `markitdown` (DOCX and PDF extras).

This directory is one module (`08_agents`) of a larger course repo rooted at `..`. The git root is the parent directory.

## Commands

```bash
uv sync                            # install exactly what uv.lock pins (use this, not `uv pip install -e .`)

uv run main.py                     # start the MCP server (stdio)
uv run mcp dev main.py             # open the server in MCP Inspector (mcp[cli])

uv run pytest                      # all tests
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf  # single test
```

The README's setup step, `uv pip install -e .`, ignores `uv.lock` and resolves `mcp>=1.6.0` to mcp 2.x. In 2.x, FastMCP was renamed (`mcp.server.fastmcp` no longer exists), so `main.py` fails to import. The code targets mcp 1.x, which `uv.lock` pins at 1.6.0.

A parent `.venv` at `../.venv` may be active in the shell. `uv run` ignores it and uses this folder's `.venv`, but bare `python` or `pytest` will not.

## Code style

- Always give function arguments appropriate type hints.

## Architecture

- `main.py` creates the `FastMCP` instance and registers tools with `mcp.tool()(fn)`. A tool is only exposed if it is registered here. Right now `tools.math.add` and `tools.document.document_path_to_markdown` are registered. `binary_document_to_markdown` is deliberately left unregistered: it's an internal helper, because MCP clients can't easily send raw bytes.
- `tools/` holds plain Python functions, one module per domain. They have no MCP dependency, so tests import and call them directly.
- `tests/fixtures/` contains `mcp_docs.docx` and `mcp_docs.pdf`, which the document conversion tests read as binary input.

## Defining MCP tools

These conventions come from the README. `tools/math.py:add` is the reference implementation.

1. Write the tool as a plain function in a `tools/` module, then register it in `main.py`:

   ```python
   from tools.my_module import my_function
   mcp.tool()(my_function)
   ```

   FastMCP builds the tool's name, description, and input schema from the function, so its signature and docstring are the interface the model sees.

2. Describe every parameter with `pydantic.Field(description=...)` as its default value, and add type hints to every parameter and the return value:

   ```python
   from pydantic import Field

   def my_tool(
       param1: str = Field(description="Detailed description of this parameter"),
       param2: int = Field(description="Explain what this parameter does"),
   ) -> ReturnType:
       """Comprehensive docstring here"""
   ```

3. The docstring becomes the tool description. It should:
   - Begin with a one-line summary
   - Give a detailed explanation of what the tool does
   - Explain when to use the tool and when not to (as a "When to use:" section, like in `add`)
   - Include usage examples with expected input and output (`>>>` doctest style, like in `add`)

`binary_document_to_markdown` doesn't follow these conventions, because it's an internal helper rather than a registered tool. Bring it up to this standard if it is ever registered.
