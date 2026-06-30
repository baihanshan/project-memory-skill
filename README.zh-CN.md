# Codex Project Memory Skill

[English](README.md) | [简体中文](README.zh-CN.md)

一个用于维护项目本地长期记忆系统的 Codex skill。

这个 skill 帮助 Codex 保存和检索项目上下文，同时避免把整个记忆库一次性加载进上下文。它使用有边界的 `project_memory/index.md` 作为路由索引，使用 `project_memory/handoff.md` 作为快速恢复入口，并且只在需要时读取详细记忆文件。

## 功能

- 项目本地长期记忆目录：`project_memory/`
- 通过 `handoff.md` 快速恢复会话
- 通过 `index.md` 维护有边界的路由索引
- 按需检索详细记忆文件
- 为 bug、ADR、主题、命令、API 契约、环境说明和模式沉淀提供结构化分类
- 敏感信息脱敏规则
- 带日期和证据的冲突处理机制
- 用于初始化、索引维护、健康检查、脱敏和归档的 Python 脚本

## 安装

克隆这个仓库，并把 skill 文件夹复制到你的 Codex skills 目录：

```bash
git clone https://github.com/baihanshan/project-memory-skill.git project-memory
mkdir -p ~/.codex/skills
cp -R project-memory ~/.codex/skills/project-memory
```

安装后重启 Codex。

## 使用

当一个软件项目已经包含或应该包含 `project_memory/` 目录时，或者你希望 Codex 跨会话保存耐久项目上下文时，可以使用这个 skill。

在项目中初始化记忆目录：

```bash
python ~/.codex/skills/project-memory/scripts/init_memory.py --project-root .
```

该命令会创建：

```text
project_memory/
  index.md
  handoff.md
  inbox.md
  active/
  archive/
```

## 内置脚本

- `scripts/init_memory.py`：创建项目记忆结构和模板
- `scripts/update_index.py`：根据 active memory 文件重建 `project_memory/index.md`
- `scripts/check_memory_health.py`：检查索引大小、缺失链接、handoff 大小、证据和潜在秘密信息
- `scripts/redact_secrets.py`：从记忆文件中脱敏疑似秘密值
- `scripts/archive_memory.py`：将 active memory 文件移动到 archive，并更新状态元数据

## 许可证

MIT
