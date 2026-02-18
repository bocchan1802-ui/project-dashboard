#!/usr/bin/env python3
"""
GitHub Issuesからプロジェクトダッシュボードを生成するスクリプト
"""

import os
import json
from datetime import datetime
import requests

# GitHub API設定
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
REPO = os.getenv('GITHUB_REPOSITORY', 'bocchan1802-ui/project-dashboard')
GITHUB_API = f"https://api.github.com/repos/{REPO}/issues"

# ステータスマッピング
STATUS_MAP = {
    '計画中': 'planned',
    '進行中': 'in-progress',
    '完了': 'completed',
    '保留': 'planned',
}

LABEL_STATUS_MAP = {
    'status:planned': 'planned',
    'status:in-progress': 'in-progress',
    'status:completed': 'completed',
    'status:hold': 'planned',
}

def fetch_issues():
    """GitHub Issuesを取得"""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }

    # ラベルでフィルタリング（プロジェクト関連のIssueのみ）
    params = {
        'state': 'all',
        'labels': 'project',
        'sort': 'updated',
        'direction': 'desc',
    }

    response = requests.get(GITHUB_API, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def parse_issue_body(body):
    """Issue本文を解析"""
    fields = {
        'current_task': '',
        'blockers': '',
        'tags': '',
        'demo_url': '',
        'repo_url': '',
    }

    current_field = None
    for line in body.split('\n'):
        line = line.strip()
        if line.startswith('###'):
            field_key = line.lower().replace('###', '').strip().replace(' ', '_')
            current_field = field_key
        elif current_field and line:
            if fields.get(current_field):
                fields[current_field] += '\n' + line
            else:
                fields[current_field] = line

    return fields

def get_status_from_labels(labels):
    """ラベルからステータスを判定"""
    for label in labels:
        label_name = label['name']
        if label_name in LABEL_STATUS_MAP:
            return LABEL_STATUS_MAP[label_name]
    return 'planned'

def generate_html(issues):
    """IssuesからHTMLを生成"""
    projects = []
    for issue in issues:
        # Skip pull requests
        if 'pull_request' in issue:
            continue

        fields = parse_issue_body(issue['body'])

        # ステータス判定
        status = get_status_from_labels(issue.get('labels', []))

        # タグ処理
        tags = [tag.strip() for tag in fields['tags'].split(',') if tag.strip()]

        # リンク
        links = []
        if fields['demo_url']:
            links.append({
                'type': 'primary',
                'label': '🚀 開く',
                'url': fields['demo_url']
            })
        if fields['repo_url']:
            links.append({
                'type': 'secondary',
                'label': '📁 GitHub',
                'url': fields['repo_url']
            })
        links.append({
            'type': 'secondary',
            'label': '💬 Issue',
            'url': issue['html_url']
        })

        # コメント（現在の状況）
        comments = []
        if fields['current_task']:
            comments.append({
                'text': f"🔵 作業中: {fields['current_task']}",
                'date': datetime.fromisoformat(issue['updated_at']).strftime('%Y-%m-%d')
            })
        if fields['blockers']:
            comments.append({
                'text': f"🔴 課題: {fields['blockers']}",
                'date': datetime.fromisoformat(issue['updated_at']).strftime('%Y-%m-%d')
            })

        project = {
            'id': issue['id'],
            'title': issue['title'],
            'description': issue['body'].split('\n')[0] if issue['body'] else '',
            'status': status,
            'tags': tags,
            'links': links,
            'comments': comments
        }
        projects.append(project)

    # 既存のindex.htmlからベースを取得
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # プロジェクトデータ部分を置換
    projects_json = json.dumps(projects, ensure_ascii=False, indent=8)
    projects_start = 'const projects = ['
    projects_end = '];'

    start_idx = html_content.find(projects_start)
    end_idx = html_content.find(projects_end, start_idx)

    if start_idx != -1 and end_idx != -1:
        new_projects_section = f'const projects = {projects_json};'
        new_html = (
            html_content[:start_idx] +
            new_projects_section +
            html_content[end_idx + len(projects_end):]
        )

        # 最終更新日時を追加
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_html = new_html.replace(
            '<p>マスターのためのプロジェクト管理ダッシュボード</p>',
            f'<p>マスターのためのプロジェクト管理ダッシュボード</p>\n                <p style="font-size: 0.8rem; color: #718096; margin-top: 5px;">最終更新: {update_time}</p>'
        )

        return new_html

    return html_content

def main():
    """メイン処理"""
    print("📊 GitHub Issuesからダッシュボードを生成中...")

    try:
        issues = fetch_issues()
        print(f"📝 {len(issues)}件のIssueを取得")

        html = generate_html(issues)

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)

        print("✅ index.htmlを更新しました！")

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    main()
