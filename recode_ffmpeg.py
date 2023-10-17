import os
import time
import queue
import concurrent.futures
from collections import defaultdict

from utils.files import retrieve_files, make_dir, exec_command

NEW_SIZE = 'scale=228:128'  # 'scale=960:540'

def concat_video_clips(src_root, dst_root, max_workers=4):
    extension = ".mp4"  # The file extension to search for
    identifier = "ln-szln"  # The identifier to search for in the file paths
    
    src_files = retrieve_files(src_root, extension, identifier)
    src_dirs = list(set([os.path.dirname(rf) for rf in src_files]))

    ffmpeg_param1s = []
    ffmpeg_param2s = []

    for src_dir in src_dirs:
        for dir, _, files in os.walk(src_dir):
            # files = [f for f in files if '.DS_Store' not in f]
            groups = defaultdict(list)
            for f in files:
                substring = f[:18]
                groups[substring].append(f)
            grouped_files_list = list(groups.values())
            for gf in grouped_files_list:
                gf_sorted = sorted(gf)
                fp1 = [dir + "/" + gs for gs in gf_sorted]
                ffmpeg_param1s.append(fp1)
                fp2 = fp1[0]
                ffmpeg_param2s.append(fp2)
    
    ffmpeg_param2s = [fp2.replace(src_root, dst_root) for fp2 in ffmpeg_param2s]
    temp = []
    for (fp1, fp2) in zip(ffmpeg_param1s, ffmpeg_param2s):
        make_dir(fp2)
        filelist = fp2.replace(".mp4", ".txt") #  os.path.dirname(fp2) + "/filelist.txt"
        temp.append(filelist)
        with open(filelist, "w") as f:
            for element in fp1:
                f.write(f"file '{element}'\n")
    ffmpeg_param1s = temp
    
    t1 = time.time()

    # base_commands = [["ffmpeg", "-f", "concat", "-safe", "0", "-i", fp1, "-c", "copy", fp2] 
    #                  for (fp1, fp2) in zip(ffmpeg_param1s, ffmpeg_param2s)]
    base_commands = [
        ["ffmpeg", "-f", "concat", "-safe", "0", "-i", fp1, "-pix_fmt", "yuv420p", "-c:v", "libx264", "-c:a", "copy", fp2] for (fp1, fp2) in zip(ffmpeg_param1s, ffmpeg_param2s)]
    failed_messages = queue.Queue(maxsize=100)
    fm_callback = lambda x: failed_messages.put(x)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(exec_command, base_command, fm_callback) for base_command in base_commands[:1]]
        for future in concurrent.futures.as_completed(futures):
            pass  # Optionally, do something with the results

    t2 = time.time()
    print("Duration for recode all files: ", t2 - t1)

    while True:
        try:
            fm = failed_messages.get(timeout=1)
            print(f"failed_message: {fm}\n")
        except:
            break

def recode_videos(src_root, dst_root, max_workers=4):
    extension = ".mp4"  # The file extension to search for
    identifier = "ln-szln"  # The identifier to search for in the file paths

    files = retrieve_files(src_root, extension, identifier)
    print("\n".join(files))

    new_files = [file.replace(src_root, dst_root) for file in files]
    print("\n".join(new_files))

    for nf in new_files:
        make_dir(nf)

    start_time = 0  # Start time in seconds
    duration = 1000  # Duration in seconds
    # max_workers = 4  # Maximum number of concurrent tasks
    base_commands = [
        ["ffmpeg", "-i", f, "-ss", str(start_time), "-t", str(duration), nf] 
        for (f, nf) in zip(files, new_files)]

    import time
    t1 = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(exec_command, base_command) for base_command in base_commands[:2]]
        for future in concurrent.futures.as_completed(futures):
            pass  # Optionally, do something with the results

    t2 = time.time()
    print("Duration for recode all files: ", t2 - t1)

def resize_video(src_root, dst_root, max_workers=4):
    extension = ".mp4"  # The file extension to search for
    identifier = "ln-szln"  # The identifier to search for in the file paths

    src_files = retrieve_files(src_root, extension, identifier)
    dst_files = [sf.replace(src_root, dst_root) for sf in src_files]

    for df in dst_files:
        make_dir(df)

    import time
    t1 = time.time()

    # base_commands = [['ffmpeg', '-i', sf, '-vf', 'scale=iw/4:ih/4', df] for (sf, df) in zip(src_files, dst_files)]
    base_commands = [['ffmpeg', '-i', sf, '-c:v', 'h264_videotoolbox', '-vf', NEW_SIZE, '-q:v', '50', df] for (sf, df) in zip(src_files, dst_files)]
    # failed_messages = queue.Queue(maxsize=100)
    # fm_callback = lambda x: failed_messages.put(x)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # futures = [executor.submit(resize_and_mask_video, sf, df) for (sf, df) in zip(src_files, dst_files)]
        futures = [executor.submit(exec_command, base_command) for base_command in base_commands]
        for future in concurrent.futures.as_completed(futures):
            pass  # Optionally, do something with the results

    t2 = time.time()
    print("Duration for recode all files: ", t2 - t1)  # Duration for recode all files:  6437.959105014801

if __name__ == '__main__':
    # src_root = "/Users/liuziyi/Library/Mobile Documents/com~apple~CloudDocs/硬盘中转/"
    # dst_root = "/Users/liuziyi/workspace/梁孟实验/"
    # recode_videos(src_root, dst_root)

    # src_root = "/Users/liuziyi/Library/Mobile Documents/com~apple~CloudDocs/硬盘中转/"
    # dst_root = "/Users/liuziyi/workspace/梁孟实验/"
    # concat_video_clips(src_root, dst_root, max_workers=4)

    src_root = "/Users/liuziyi/workspace/960_540/"  # "/Users/liuziyi/workspace/梁孟实验/"
    dst_root = "/Users/liuziyi/workspace/228_128/"  # "/Users/liuziyi/workspace/resized_videos_ffmpeg/"
    resize_video(src_root, dst_root, max_workers=4)