---
name: github-upload
description: 上传 OpenClaw skills 到 GitHub 仓库。支持单个 skill 上传、批量同步、查看本地 skills 列表。使用前需确保已登录 GitHub (gh auth login)。
---

# GitHub Upload Skill

上传 OpenClaw skills 到 GitHub 仓库。

## 使用方式

```bash
# 列出所有本地 skills
python skills/github-upload/scripts/upload_skill.py --list

# 上传 skill 到默认仓库 (WillWeiZ/my_skills)
python skills/github-upload/scripts/upload_skill.py -s stock-a-quotes

# 上传到指定仓库
python skills/github-upload/scripts/upload_skill.py -s weather -r https://github.com/your/repo.git

# 指定分支和提交信息
python skills/github-upload/scripts/upload_skill.py -s stock-a-quotes -b main -m "Update stock skill"
```

## 前置条件

1. **登录 GitHub**
   ```bash
   echo "your_github_token" | gh auth login --with-token
   ```

2. **验证登录状态**
   ```bash
   gh auth status
   ```

## 参数说明

| 参数 | 简写 | 说明 |
|------|------|------|
| `--skill` | `-s` | 要上传的 skill 名称 |
| `--repo` | `-r` | 目标仓库 URL (默认: WillWeiZ/my_skills) |
| `--branch` | `-b` | 分支名 (默认: main) |
| `--message` | `-m` | 提交信息 |
| `--list` | `-l` | 列出所有本地 skills |

## 示例

```bash
# 上传单个 skill
python skills/github-upload/scripts/upload_skill.py -s stock-a-quotes

# 上传新创建的 skill
python skills/github-upload/scripts/upload_skill.py -s weather-query

# 查看可上传的 skills
python skills/github-upload/scripts/upload_skill.py --list
```

## 仓库结构

上传后 GitHub 仓库结构：
```
my_skills/
├── stock-a-quotes/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── stock_price.py
│   └── .clawhub/
│       └── origin.json
├── weather-query/
│   └── ...
└── ...
```

## 注意事项

- Skill 必须存在于 `~/.openclaw/workspace/skills/` 目录
- 上传前会自动克隆或更新本地仓库
- 会强制推送到目标分支
