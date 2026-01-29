# KERAG Web - 知识库浏览器

一个为 KERAG 知识库打造的现代化 Web 界面，基于 Vue 3、TypeScript 和 Pinia 构建。

## 相关项目

| 项目 | 描述 | 仓库 |
|---------|-------------|------------|
| **KERAG** | 核心库，用于构建、打包和管理知识库 | [TongWang-AI4S/KERAG](https://github.com/TongWang-AI4S/KERAG) |
| **KERAG MCP** | MCP 服务器，用于 AI 助手集成 | [TongWang-AI4S/kerag-mcp](https://github.com/TongWang-AI4S/kerag-mcp) |
| **KERAG Modules** | 预构建知识库模块（可直接安装的 tar 文件） | [TongWang-AI4S/KERAG-Modules](https://github.com/TongWang-AI4S/KERAG-Modules) |

## 教程

- **构建知识库**：学习如何编写知识库文件、打包和分发
  [KERAG-Tutorial.zh.md](https://github.com/TongWang-AI4S/KERAG/blob/main/KERAG-Tutorial.zh.md)

## 快速开始 (一行命令)

可以使用 `pip` 或 `uv` 直接安装并运行 KERAG Web。

### 1. 直接从 GitHub 安装

**使用 uv (推荐):**
```bash
uv tool install git+https://github.com/TongWang-AI4S/kerag-web.git
```

**使用 pip:**
```bash
pip install git+https://github.com/TongWang-AI4S/kerag-web.git
```

### 2. 运行
安装完成后，只需在终端输入以下命令：
```bash
kerag-web
```
服务将在 http://localhost:8001 启动。

### 3. 参数配置
您可以直接在命令后添加参数：
```bash
kerag-web --port 9000 --global-root /你的/知识库/路径
```

---

## 功能特性

- **模块管理**: 轻松加载和卸载知识模块。
- **树状导航**: 直观的分层浏览，配备面包屑导航。
- **丰富的展示格式**: 支持以 Markdown、纯文本、树形结构或 JSON 格式查看笔记。
- **全文搜索**: 在整个知识库中快速查找信息。

## 开源协议

本项目采用 MIT 开源协议。
