import os
import shutil


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)


def main():
    PATH = r'./img'
    DESTINATON = r'./tmp'

    dirs = [os.path.join(PATH, dir) for dir in os.listdir(PATH) if os.path.isdir(os.path.join(PATH, dir))]
    
    continer = [] 
    for path in dirs:
        obj = {}
        obj['src'] = path 
        # sanitize
        sanitized = path.split("\\")[-1] # this is the folder name i want
    
        # get the prefix and suffix
        split = sanitized.split("_")
        prefix = "_".join(split[:2])
        suffix = "_".join(split[2:])
    
        obj['root'] = prefix
        obj['dst'] = suffix
        continer.append(obj)
        obj = {}

    for data in continer:
        root, dst = data.get('root'), data.get('dst')
        src_path = data.get('src')
        dst_path = os.path.join(DESTINATON, root, dst)
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
