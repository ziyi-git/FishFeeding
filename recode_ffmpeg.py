import concurrent.futures

from utils.files import retrieve_files, make_dir, exec_command

def main(src_root, dst_root):
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
    max_workers = 4  # Maximum number of concurrent tasks
    base_commands = [
        ["ffmpeg", "-i", f, "-ss", str(start_time), "-t", str(duration), nf] 
        for (f, nf) in zip(files, new_files)]

    import time
    t1 = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(exec_command, base_command) for base_command in base_commands]
        for future in concurrent.futures.as_completed(futures):
            pass  # Optionally, do something with the results

    t2 = time.time()
    print("Duration for recode all files: ", t2 - t1)

if __name__ == '__main__':
    src_root = "/Users/liuziyi/Library/Mobile Documents/com~apple~CloudDocs/硬盘中转/"
    dst_root = "/Users/liuziyi/workspace/梁孟实验/"
    main(src_root, dst_root)