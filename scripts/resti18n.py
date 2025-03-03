import json

def iterate_dict(d, path, strings):
    if '.' in path:
        ele = d
    else:
        ele = d[path]

    for k, v in ele.items():
        if isinstance(v, dict) and not k.startswith('x-apifox'):
            iterate_dict(v, path + '.' + k, strings)
        elif isinstance(v, list):
            iterate_list(v, path + '.' + k, strings)
        else:
            strings.append(path + '.' + k + ': ' + v) if k in ['summary', 'description'] else []
            print(path + '.' + k, ':', v)

    return strings

def iterate_list(l, path, strings):
    for i, v in enumerate(l):
        if isinstance(v, dict):
            iterate_dict(v, path + '.' + str(i), strings)
        elif isinstance(v, list):
            iterate_list(v, path + '.' + str(i), strings)
        else:
            print(path + '.' + str(i), ':', v)

if __name__ == '__main__':
    with open('apis/openapi.json') as f:
        openapi = json.load(f)

    # list all 'summary' and 'description' of all path and parameters in a separate i18n file with specific key paths
    # for example: 'paths./api/v1/health.get.summary' and 'paths./api/v1/health.get.description'

    strings = []

    strings = iterate_dict(openapi, 'paths', strings)

    with open('apis/zh-CN.properties', 'w') as f:
        f.write('\n'.join(strings))
    
    
