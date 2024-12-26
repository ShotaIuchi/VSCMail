from datetime import datetime

def main(args):
    if len(args) < 1:
        return datetime.now().strftime('%Y-%m-%d')
    return datetime.now().strftime(args[0])
