# KERAG Web - Knowledge Base Explorer

A web interface for viewing the KERAG knowledge base, built with Vue 3, TypeScript, and Pinia.

## Related Projects

| Project | Description | Repository |
|---------|-------------|------------|
| **KERAG** | Core library for building, packing, and managing knowledge bases | [TongWang-AI4S/KERAG](https://github.com/TongWang-AI4S/KERAG) |
| **KERAG MCP** | MCP server for AI assistant integration | [TongWang-AI4S/kerag-mcp](https://github.com/TongWang-AI4S/kerag-mcp) |
| **KERAG Modules** | Pre-built knowledge base modules (ready-to-install tar archives) | [TongWang-AI4S/KERAG-Modules](https://github.com/TongWang-AI4S/KERAG-Modules) |

## Tutorials

- **Building Knowledge Bases**: Learn how to write knowledge base files, package and distribute them
  [KERAG-Tutorial.md](https://github.com/TongWang-AI4S/KERAG/blob/main/KERAG-Tutorial.md)

## Quick Start (One-liner)

You don't even need to clone the repository. You can install and run KERAG Web directly using `pip` or `uv`.

### 1. Install directly from GitHub

**Using uv (Recommended):**
```bash
uv tool install git+https://github.com/TongWang-AI4S/kerag-web.git
```

**Using pip:**
```bash
pip install git+https://github.com/TongWang-AI4S/kerag-web.git
```

### 2. Run it
After installation, simply run the following command in your terminal:
```bash
kerag-web
```
This will start the server on http://localhost:8001.

### 3. Options
You can pass arguments directly to the command:
```bash
kerag-web --port 9000 --global-root /path/to/your/knowledge
```

## Features

- **Module Management**: Load and unload knowledge modules easily.
- **Tree Navigation**: Intuitive hierarchical browsing with breadcrumbs.
- **Rich Content Display**: View notes in Markdown, Plain Text, Tree, or JSON formats.
- **Full-text Search**: Find information quickly across your entire knowledge base.

## License

This project is licensed under the MIT License.
