import os
import argparse
import time
import numpy as np
import cv2
import math
import queue

from utils.multithread import Worker
from utils import transforms

def resize_video(in_path, out_path, dst_size, sample_rate=5):
    cap = cv2.VideoCapture(in_path)
    # print("cv2.__version__", cv2.__version__)
    # print(cv2.getBuildInformation())
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    
    fnos = list(range(0, total_frames, sample_rate))
    num_threads = 8  # os.cpu_count()
    print("num_threads = ", num_threads)
    tasks = [[] for _ in range(num_threads)]
    frames_per_task = math.ceil(len(fnos) / num_threads)
    for idx, fno in enumerate(fnos):
        tasks[math.floor(idx / frames_per_task)].append(fno)
    
    data_transform = transforms.Compose([transforms.Resize(dst_size)])
    threads = []
    for _ in range(num_threads):
        w = Worker(transforms=data_transform)
        threads.append(w)
        w.start()
    
    results = queue.Queue(maxsize=100)
    on_done = lambda x: results.put(x)
    for idx, w in enumerate(threads):
        w.decode(in_path, tasks[idx], on_done)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, 25.0, dst_size)
    imgs_id = []
    imgs = []
    while True:
        try:
            # print(f"current size: {results.qsize()}")
            (img_id, img) = results.get(timeout=5)
            imgs_id.append(img_id)
            imgs.append(img)
            # out.write(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        except queue.Empty:
            print("Timeout, queue is still empty. Continue waiting.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    
    imgs = np.array(imgs)[imgs_id]
    for img in imgs:
        out.write(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    out.release()
