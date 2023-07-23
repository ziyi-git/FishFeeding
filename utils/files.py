import os
import subprocess
import concurrent.futures
import shutil


def retrieve_files(dir_path, extension, identifier):
    """
    Return file paths with specified extension (e.g. mp4) and identifier.

    Example:
    >>> retrieve_files("/X", ".mp4", "ln-szln")
    ["/X/第1次投喂数据/乐农水面摄食视频/ln-szln-p001-s0006_main_20221201110010_42.mp4", ...]
    """
    # Check if the directory exists
    if not os.path.isdir(dir_path):
        print(f"{dir_path} is not a valid directory.")
        return []
    
    # List to store the paths of all matching files
    matching_files = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # Check if the file has the desired extension and contains the identifier in its path
            if file.endswith(extension) and identifier in os.path.join(root, file):
                matching_files.append(os.path.join(root, file))
    
    return matching_files

def make_dir(destination_path):
    """
    Create directory if destination_path not exist.
    Example:
    >>> make_dir("/A/B/C.mp4") create "/A/B/" if "/A/B/" not exist
    >>> make_dir("/A/B/")      create "/A/B/" if "/A/B/" not exist
    >>> make_dir("/A/B")       create "/A/"   if "/A/" not exist
    """
    # Check if the destination directory exists
    destination_dir = os.path.dirname(destination_path)
    if not os.path.exists(destination_dir):
        try:
            # Try to create the directory
            os.makedirs(destination_dir)
            print(f"Directory {destination_dir} created.")
        except OSError:
            print(f"Could not create directory {destination_dir}.")
            return False

def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
        print(f"Video file {src} copied to {dst}.")
        return True
    except shutil.Error as e:
        print(f"Coulds not copy video file: {e}")
        return False

def exec_command(command):
    print(command)
    try:
        subprocess.run(command, check=True)
        print(f"Exec {command} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Exec {command} failed: {e.output}")



def main():
    # Example usage
    dir_path = "/Users/liuziyi/Library/Mobile Documents/com~apple~CloudDocs/硬盘中转/"  # The directory to search
    extension = ".mp4"  # The file extension to search for
    identifier = "ln-szln"  # The identifier to search for in the file paths

    files = retrieve_files(dir_path, extension, identifier)
    print("\n".join(files))

    new_files = [file.replace(dir_path, "/Users/liuziyi/workspace/梁孟实验/") for file in files]
    print("\n".join(new_files))

    for nf in new_files:
        make_dir(nf)

    print(files[0])
    print(new_files[0])

    start_time = 0  # Start time in seconds
    duration = 300  # Duration in seconds
    max_workers = 1  # Maximum number of concurrent tasks
    base_commands = [
        ["ffmpeg", "-i", f, "-ss", str(start_time), "-t", str(duration), nf] 
        for (f, nf) in zip(files, new_files)]

    import time
    t1 = time.time()
    # Use a ThreadPoolExecutor to run the function in parallel
    # with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     # futures = [executor.submit(exec_command, base_command) for base_command in base_commands]
    #     futures = [executor.submit(exec_command, base_command) for base_command in base_commands[:12]]
    #     for future in concurrent.futures.as_completed(futures):
    #         pass  # Optionally, do something with the results
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # futures = [executor.submit(exec_command, base_command) for base_command in base_commands]
        futures = [executor.submit(exec_command, base_command) for base_command in base_commands[:12]]
        for future in concurrent.futures.as_completed(futures):
            pass  # Optionally, do something with the results
    t2 = time.time()
    print("t2 - t1 = ", t2 - t1)

if __name__ == '__main__':
    main()