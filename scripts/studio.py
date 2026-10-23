#!/usr/bin/env python3
"""Local project bookkeeping and bundled style preparation; no network actions."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import uuid

SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = Path.home() / 'codex_workspace' / '心理测试网页'
MANIFEST = 'studio-project.json'
STYLES = ('jade', 'parchment', 'mist', 'custom')
STAGES = ('plan', 'style', 'build', 'local', 'deploy')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def save(project, data):
    data['updatedAt'] = now()
    target = project / MANIFEST
    temporary = target.with_suffix('.json.new')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(target)


def load(path):
    project = Path(path).expanduser().resolve()
    if project == SKILL_DIR or SKILL_DIR in project.parents:
        raise ValueError('项目不能写入 Skill 本体；请使用独立工作目录。')
    target = project / MANIFEST
    if not target.is_file():
        raise ValueError(f'找不到项目记录：{target}')
    data = json.loads(target.read_text(encoding='utf-8'))
    if data.get('schemaVersion') != 1 or not data.get('projectId'):
        raise ValueError('项目记录格式不受支持。')
    if not all(key in data for key in ('title', 'topic', 'status', 'confirmations')):
        raise ValueError('项目记录缺少基本资料或确认列表。')
    return project, data


def active(data):
    if data.get('status') == 'archived':
        raise ValueError('项目已归档；先 restore 再修改或准备上线。')


def latest(data, stage):
    return next((e for e in reversed(data.get('confirmations', [])) if e['stage'] == stage), None)


def init(args):
    topic = args.topic.strip()
    if not topic:
        raise ValueError('主题不能为空。')
    safe_name = re.sub(r'[\x00-\x1f/\\:*?"<>|]', '-', topic).strip(' .')[:80]
    if not args.output and safe_name in ('', '.', '..'):
        raise ValueError('主题不能作为目录名；请用 --output 指定项目目录。')
    project = (Path(args.output).expanduser() if args.output else DEFAULT_ROOT / safe_name).resolve()
    if project == SKILL_DIR or SKILL_DIR in project.parents:
        raise ValueError('请把项目保存到工作目录，而非 Skill 本体。')
    if project.exists():
        raise ValueError(f'目录已存在，未覆盖。继续旧项目请使用 show：{project}')
    gallery = SKILL_DIR / 'assets/style-gallery/index.html'
    if not gallery.is_file():
        raise ValueError('Skill 风格预览资产缺失，尚未创建项目。')
    project.mkdir(parents=True)
    for name in ('package', 'source', 'previews', 'validation'):
        (project / name).mkdir()
    shutil.copyfile(gallery, project / 'previews/style-gallery.html')
    data = {
        'schemaVersion': 1, 'projectId': str(uuid.uuid4()),
        'topic': topic, 'title': args.title or topic,
        'contentMode': args.mode, 'status': 'active',
        'createdAt': now(), 'selectedStyle': None,
        'confirmations': [],
        'deployment': {'provider': 'upma', 'url': None, 'projectId': None},
    }
    save(project, data)
    output({'project': str(project), 'manifest': str(project / MANIFEST),
            'gallery': str(project / 'previews/style-gallery.html'), 'phase': 'planning'})


def list_projects(args):
    root = Path(args.root).expanduser().resolve()
    projects, errors = [], []
    for record in sorted(root.glob('*/' + MANIFEST)):
        try:
            project, data = load(record.parent)
            if args.all or data.get('status') != 'archived':
                projects.append({'project': str(project), 'title': data['title'],
                                 'status': data['status'], 'style': data.get('selectedStyle'),
                                 'url': data.get('deployment', {}).get('url')})
        except (ValueError, OSError) as error:
            errors.append({'record': str(record), 'error': str(error)})
    output({'root': str(root), 'projects': projects, 'errors': errors})


def mutate(args):
    project, data = load(args.project)
    if args.command == 'show':
        output({'project': str(project), **data})
        return
    if args.command == 'archive':
        data['status'] = 'archived'
    elif args.command == 'restore':
        data['status'] = 'active'
    else:
        active(data)
        if args.command == 'edit':
            for key in ('topic', 'title'):
                value = getattr(args, key)
                if value is not None:
                    if not value.strip():
                        raise ValueError(f'{key} 不能为空。')
                    data[key] = value.strip()
        elif args.command == 'record':
            evidence = args.evidence.strip()
            if not evidence:
                raise ValueError('必须填写真实用户确认原文；记录不能创造授权。')
            event = {'stage': args.stage, 'evidence': evidence, 'at': now()}
            if args.stage == 'style':
                if not args.style:
                    raise ValueError('style 阶段需要 --style。')
                event['style'] = args.style
                data['selectedStyle'] = args.style
            elif args.style:
                raise ValueError('--style 仅用于 style 阶段。')
            if args.stage == 'local':
                site = project / 'site/index.html'
                if not site.is_file():
                    raise ValueError('尚无 site/index.html，不能登记本地网页验收。')
                event['siteSha256'] = digest(site)
            data['confirmations'].append(event)
        elif args.command == 'deployment':
            if not latest(data, 'deploy'):
                raise ValueError('先根据真实部署指令登记 deploy 授权。')
            if not re.fullmatch(r'https://[^\s/]+(?:/[^\s]*)?', args.url):
                raise ValueError('部署网址应为经过验证的 HTTPS 正式入口。')
            data['deployment'].update({'provider': 'upma', 'url': args.url, 'recordedAt': now()})
            if args.provider_project_id is not None:
                data['deployment']['projectId'] = args.provider_project_id
    save(project, data)
    output({'project': str(project), 'status': data['status'],
            'selectedStyle': data.get('selectedStyle'), 'saved': True})


def prepare_style(args):
    project, data = load(args.project)
    active(data)
    missing = [stage for stage in ('plan', 'style', 'build') if not latest(data, stage)]
    if missing:
        raise ValueError('先登记真实确认：' + ', '.join(missing))
    theme = data.get('selectedStyle')
    if theme not in STYLES[:-1]:
        raise ValueError('自定义风格应按用户参考制作 source/theme.css，不套内置模板。')
    target = project / 'source/theme.css'
    if target.exists() and not args.refresh:
        raise ValueError('source/theme.css 已存在，未覆盖。确定要重取内置样式时加 --refresh。')
    css = [(SKILL_DIR / 'assets/styles' / name).read_text(encoding='utf-8')
           for name in ('base.css', theme + '.css')]
    target.parent.mkdir(exist_ok=True)
    target.write_text('\n'.join(css), encoding='utf-8')
    output({'style': theme, 'css': str(target), 'htmlAttribute': f'data-theme="{theme}"'})


def check(args):
    project, data = load(args.project)
    errors, notices = [], []
    if data.get('status') != 'active':
        errors.append('项目已归档。')
    index = project / 'package/资料包索引.md'
    if not index.is_file():
        errors.append('缺少 package/资料包索引.md；请先交付完整规划资料。')
    site = project / 'site/index.html'
    result = {'project': str(project), 'selectedStyle': data.get('selectedStyle')}
    if site.is_file():
        result['site'] = {'path': str(site), 'bytes': site.stat().st_size, 'sha256': digest(site)}
        for stage in ('plan', 'style', 'build'):
            if not latest(data, stage):
                errors.append(f'缺少 {stage} 确认记录；核对已有对话，勿凭记录反复问。')
    elif args.deploy:
        errors.append('缺少可发布文件 site/index.html。')
    if args.deploy:
        for stage in ('local', 'deploy'):
            if not latest(data, stage):
                errors.append(f'缺少 {stage} 记录；请核对实际用户验收与部署指令。')
        accepted = latest(data, 'local')
        if accepted and site.is_file() and accepted.get('siteSha256') != digest(site):
            notices.append('当前网页与验收摘要不同：审阅差异与修复范围，再决定是否需补充验收。')
    notices.append('此检查只核对项目文件和阶段记录，不证明计分正确、网页可用或全国可访问。')
    output({**result, 'ok': not errors, 'errors': errors, 'notices': notices})
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    create = sub.add_parser('init', help='创建独立规划项目和风格示意，不生成正式网页')
    create.add_argument('--topic', required=True)
    create.add_argument('--title')
    create.add_argument('--output')
    create.add_argument('--mode', choices=('original-entertainment', 'validated-instrument'),
                        default='original-entertainment')
    listing = sub.add_parser('list', help='列出目录下的工作室项目')
    listing.add_argument('--root', default=str(DEFAULT_ROOT))
    listing.add_argument('--all', action='store_true')
    for command in ('show', 'edit', 'archive', 'restore', 'record', 'prepare-style', 'check', 'deployment'):
        entry = sub.add_parser(command)
        entry.add_argument('--project', required=True)
        if command == 'edit':
            entry.add_argument('--title')
            entry.add_argument('--topic')
        elif command == 'record':
            entry.add_argument('--stage', choices=STAGES, required=True)
            entry.add_argument('--evidence', required=True)
            entry.add_argument('--style', choices=STYLES)
        elif command == 'prepare-style':
            entry.add_argument('--refresh', action='store_true')
        elif command == 'check':
            entry.add_argument('--deploy', action='store_true')
        elif command == 'deployment':
            entry.add_argument('--url', required=True)
            entry.add_argument('--provider-project-id')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            init(args)
        elif args.command == 'list':
            list_projects(args)
        elif args.command == 'prepare-style':
            prepare_style(args)
        elif args.command == 'check':
            return check(args)
        else:
            mutate(args)
    except (ValueError, OSError) as error:
        print(f'错误：{error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
