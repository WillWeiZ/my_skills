#!/usr/bin/env python3
"""
上传 skill 到 GitHub 仓库
"""

import json
import sys
import os
import subprocess


def run_cmd(cmd):
    """执行命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def get_gh_token():
    """获取 GitHub Token"""
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:
        return token
    
    # 尝试从 gh auth 获取
    code, stdout, _ = run_cmd('gh auth token')
    if code == 0 and stdout.strip():
        return stdout.strip()
    
    return None


def upload_skill(skill_name, repo_url=None, branch="main", commit_message=None):
    """
    上传 skill 到 GitHub
    
    Args:
        skill_name: skill 名称
        repo_url: 仓库 URL (默认使用 my_skills)
        branch: 分支名
        commit_message: 提交信息
    """
    workspace = "/Users/willbot/.openclaw/workspace"
    skill_path = os.path.join(workspace, "skills", skill_name)
    
    # 检查 skill 是否存在
    if not os.path.exists(skill_path):
        return {"error": f"Skill '{skill_name}' 不存在于 {skill_path}"}
    
    # 获取 GitHub Token
    token = get_gh_token()
    if not token:
        return {"error": "未找到 GitHub Token，请先运行: echo 'token' | gh auth login --with-token"}
    
    # 解析仓库信息
    if not repo_url:
        repo_url = "https://github.com/WillWeiZ/my_skills.git"
    
    # 提取 owner 和 repo 名称
    if "github.com/" in repo_url:
        parts = repo_url.split("github.com/")[-1].replace(".git", "").split("/")
        owner = parts[0]
        repo_name = parts[1] if len(parts) > 1 else "my_skills"
    else:
        return {"error": "无效的仓库 URL"}
    
    temp_dir = f"/tmp/github_upload_{skill_name}"
    
    try:
        # 克隆或更新仓库
        if os.path.exists(temp_dir):
            os.chdir(temp_dir)
            code, _, _ = run_cmd("git fetch origin")
            code, _, _ = run_cmd(f"git checkout {branch}")
        else:
            code, stdout, stderr = run_cmd(f"git clone {repo_url} {temp_dir}")
            if code != 0:
                # 尝试创建新仓库
                run_cmd(f"mkdir -p {temp_dir}")
                os.chdir(temp_dir)
                run_cmd("git init")
                run_cmd(f"git remote add origin {repo_url}")
            else:
                os.chdir(temp_dir)
        
        # 更新仓库
        os.chdir(temp_dir)
        
        # 确保在正确分支
        run_cmd(f"git checkout {branch} 2>/dev/null || git checkout -b {branch}")
        
        # 复制 skill 文件
        target_path = os.path.join(temp_dir, skill_name)
        if os.path.exists(target_path):
            run_cmd(f"rm -rf {target_path}")
        run_cmd(f"cp -r {skill_path} {target_path}")
        
        # 提交更改
        run_cmd("git add .")
        
        if commit_message is None:
            commit_message = f"Add {skill_name} skill"
        
        run_cmd(f'git commit -m "{commit_message}"')
        
        # 推送
        code, stdout, stderr = run_cmd(f"git push -u origin {branch}")
        
        if code == 0:
            return {
                "success": True,
                "message": f"Skill '{skill_name}' 已成功上传到 GitHub",
                "repo": f"{owner}/{repo_name}",
                "path": skill_name,
                "branch": branch
            }
        else:
            return {"error": f"推送失败: {stderr}"}
            
    except Exception as e:
        return {"error": str(e)}
    finally:
        # 清理临时目录
        if os.path.exists(temp_dir):
            pass  # 保留以供检查


def list_skills():
    """列出本地所有 skills"""
    workspace = "/Users/willbot/.openclaw/workspace/skills"
    skills = []
    for name in os.listdir(workspace):
        if os.path.isdir(os.path.join(workspace, name)):
            skill_file = os.path.join(workspace, name, "SKILL.md")
            if os.path.exists(skill_file):
                skills.append(name)
    return skills


def main():
    import argparse
    parser = argparse.ArgumentParser(description='上传 Skill 到 GitHub')
    parser.add_argument('--skill', '-s', type=str, help='Skill 名称')
    parser.add_argument('--repo', '-r', type=str, help='仓库 URL')
    parser.add_argument('--branch', '-b', type=str, default='main', help='分支名')
    parser.add_argument('--message', '-m', type=str, help='提交信息')
    parser.add_argument('--list', '-l', action='store_true', help='列出本地 skills')
    
    args = parser.parse_args()
    
    if args.list:
        skills = list_skills()
        print("本地 Skills:")
        for s in skills:
            print(f"  - {s}")
        return
    
    if not args.skill:
        print("请指定 skill 名称: python upload_skill.py -s stock-a-quotes")
        return
    
    result = upload_skill(
        skill_name=args.skill,
        repo_url=args.repo,
        branch=args.branch,
        commit_message=args.message
    )
    
    if "error" in result:
        print(f"错误: {result['error']}")
        sys.exit(1)
    else:
        print(f"✅ {result['message']}")
        print(f"   仓库: {result['repo']}")
        print(f"   路径: {result['path']}")


if __name__ == "__main__":
    main()
