import os
import shutil




def format_image_dir(path: str, destination: str):
    """ Formats image dir, i.e. removes the prefix from the dir and extracts Sensor_Date_BeamMode """
    dirs = [os.path.join(path, dir) for dir in os.listdir(path) if os.path.isdir(os.path.join(path, dir))]
    
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
        dst_path = os.path.join(destination, root, dst)
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)

