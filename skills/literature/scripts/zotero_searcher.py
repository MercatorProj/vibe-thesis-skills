import argparse
import sys
import json
import os

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: uv add requests")
    sys.exit(1)


def expand_keywords(query):
    """扩展关键词为相关术语列表"""
    keyword_map = {
        'VPR问题': ['VPR问题', '车辆路径问题', 'VRP', 'Vehicle Routing Problem'],
        '路径规划': ['路径规划', '路线规划', '路径优化', 'path planning'],
        '调度优化': ['调度优化', '排班优化', 'scheduling optimization'],
        '高原环境': ['高原环境', '高寒环境', 'high-altitude environment', 'alpine environment'],
        '车辆运输': ['车辆运输', 'vehicle transportation', 'vehicle logistics']
    }
    return keyword_map.get(query, [query])


def _build_headers(api_key: str | None) -> dict:
    if not api_key:
        return {}
    # Zotero Local API commonly accepts Zotero-API-Key; some setups also accept Authorization: Bearer
    return {
        'Zotero-API-Key': api_key,
        'Authorization': f'Bearer {api_key}',
        # Required for requests that otherwise look like browser traffic (DNS rebinding protection)
        'zotero-allowed-request': '1',
    }


def search_zotero(query, base_url='http://localhost:23119/api/', user_id='0', api_key=None, expand=False, limit=20):
    """执行Zotero本地库搜索（Zotero Local API）"""
    base_url = base_url.rstrip('/') + '/'
    headers = _build_headers(api_key)
    api_url = f'{base_url}users/{user_id}/items'

    queries = expand_keywords(query) if expand else [query]
    all_results = []
    seen_ids = set()

    for q in queries:
        params = {'q': q, 'format': 'json', 'limit': limit}
        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            results = parse_results(response.json())

            for result in results:
                if result['key'] not in seen_ids:
                    seen_ids.add(result['key'])
                    all_results.append(result)
        except requests.exceptions.RequestException as e:
            print(f"搜索'{q}'时出错: {str(e)}", file=sys.stderr)
            continue

    return all_results[:limit]


def parse_results(results):
    """解析API响应，提取文献元数据"""
    parsed = []
    for item in results:
        data = item.get('data', {})
        parsed.append({
            'key': data.get('key') or data.get('id'),
            'title': data.get('title', '无标题'),
            'authors': [author.get('name') or 'Unknown Author' for author in data.get('creators', [])],
            'publication': data.get('publicationTitle', '未知期刊'),
            'year': data.get('date', '未知年份'),
            'abstract': data.get('abstractNote', ''),
            'doi': data.get('DOI', ''),
            'item_type': data.get('itemType', 'unknown')
        })
    return parsed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Zotero文献检索工具')
    parser.add_argument('-q', '--query', required=True, help='搜索关键词')
    parser.add_argument('-e', '--expand', action='store_true', help='启用关键词自动扩展')
    parser.add_argument('-l', '--limit', type=int, default=20, help='返回结果数量限制')
    parser.add_argument('--base-url', default='http://localhost:23119/api/', help='Zotero Local API地址')
    parser.add_argument('--user-id', default='0', help='用户库ID（Local API通常为0）')
    parser.add_argument('--api-key', default=None, help='Zotero Local API key（也可用环境变量ZOTERO_LOCAL_API_KEY/ZOTERO_API_KEY）')
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get('ZOTERO_LOCAL_API_KEY') or os.environ.get('ZOTERO_API_KEY')
    results = search_zotero(
        args.query,
        base_url=args.base_url,
        user_id=args.user_id,
        api_key=api_key,
        expand=args.expand,
        limit=args.limit,
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))
