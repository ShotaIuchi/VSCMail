import os
import sys
import urllib.parse
import webbrowser
import yaml

def load_config():
    with open(os.path.abspath('config.yml'), 'r', encoding='utf-8') as fp:
        data = yaml.safe_load(fp)
    return data

def load_env(file):
    with open(os.path.abspath('env.yml'), 'r', encoding='utf-8') as fp:
        datas = yaml.safe_load(fp)
    for data in datas:
        if data['FILE'] in file:
            return data
    return None

def load_template(file):
    with open(file, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    
    if len(lines) < 1:
        print(f"File {file} is empty")
        sys.exit(10)
    
    title = lines[0]
    body  = ''.join(lines[2:])

    return title, body

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_mail.py <email>")
        sys.exit(1)

    file = os.path.abspath(sys.argv[1])
    if not os.path.exists(file):
        print(f"File {file} not found")
        sys.exit(2)
        
    env = load_env(file)
    if not env:
        print("Environment variables not found")
        sys.exit(3)

    configs = load_config()

    title, body = load_template(file)
    if not title or not body:
        print("Template is empty")
        sys.exit(4)

    for config in configs:
        TAG = config['TAG']
        MSG = config['MSG']
        if config.get('OPT', '') == 'script':
            import importlib
            module = importlib.import_module(MSG)
            MSG = module.main(config.get('ARG', []))
        title = title.replace(TAG, MSG)
        body = body.replace(TAG, MSG)

    title = urllib.parse.quote(title)
    body = urllib.parse.quote(body)

    TO = env['TO']
    CC = env.get('CC', '')
    BCC = env.get('BCC', '')

    query_params = []
    if CC:
        query_params.append(f'cc={CC}')
    if BCC:
        query_params.append(f'bcc={BCC}')
    query_params.append(f'subject={title}')
    query_params.append(f'body={body}')

    mailto = f'mailto:{TO}'
    if query_params:
        mailto += '?' + '&'.join(query_params)

    webbrowser.open(mailto)

if __name__ == '__main__':
    main()
