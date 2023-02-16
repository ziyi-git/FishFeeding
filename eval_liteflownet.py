import argparse
import time

import torch
import numpy as np
import pandas as pd
import PIL
import PIL.Image
import cv2 as cv
from skimage import color, morphology, img_as_float
from skimage.io import imread, imshow
from skimage.transform import resize
from skimage.morphology import convex_hull_image

from liteflownet.run import estimate

import math
import queue
from video_utils.multithread import Worker

def demo(args):
    num_threads = 1
    sample_rate = 5

    print(args.video)
    cap = cv.VideoCapture(args.video)
    size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv.CAP_PROP_FPS)
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    fnos = list(range(0, total_frames, sample_rate))
    tasks = [[] for _ in range(num_threads)]
    frames_per_task = math.ceil(len(fnos) / num_threads)
    for idx, fno in enumerate(fnos):
        tasks[math.floor(idx / frames_per_task)].append(fno)
    
    # mask
    cap.set(cv.CAP_PROP_POS_FRAMES, 5001)
    success = cap.grab()
    success, img = cap.retrieve()
    cv.imwrite("./mask.jpg", img)
    img = img_as_float(img) # opencv to skimage
    img = resize(img, (img.shape[0] // 4, img.shape[1] // 4), anti_aliasing=True)
    lum = color.rgb2gray(img)
    mask = morphology.remove_small_holes(morphology.remove_small_objects(lum < 0.8, 5000),500)
    mask = morphology.opening(mask, morphology.disk(3))
    mask = convex_hull_image(~mask)

    threads = []
    for _ in range(num_threads):
        w = Worker(mask=mask)
        threads.append(w)
        w.start()
    
    results = queue.Queue(maxsize=100)
    on_done = lambda x: results.put(x)
    for idx, w in enumerate(threads):
        w.decode(args.video, tasks[idx], on_done)
    
    t = time.time()
    eval_results = []
    while True:
        # image_pair = results.get(timeout=5)
        # (idx1, img1), (idx2, img2) = image_pair
        # tenOutput = estimate(img1, img2)
        try:
            image_pair = results.get(timeout=5)
            (idx1, img1), (idx2, img2) = image_pair
            tenOutput = estimate(img1, img2)
            tenOutput = tenOutput.numpy()
            tenOutput = np.sqrt(np.power(tenOutput[0, :, :], 2) + np.power(tenOutput[1, :, :], 2)).sum()
            eval_results.append((idx1, tenOutput))
        except:
            break
    (all_idx, all_results) = tuple(zip(*eval_results))
    s = np.argsort(all_idx)  # 从小到大排序
    all_idx = np.array(all_idx)[s]
    all_results = np.array(all_results)[s]
    save_file = pd.DataFrame({"idx": all_idx, "all_results": all_results})
    save_file.to_csv("./abc.csv", index=None)
    print("duration = ", time.time() - t)

    cap.release()
    print("done")


parser = argparse.ArgumentParser()
parser.add_argument("--video", default="/data/Data/xyz.mp4")
args = parser.parse_args()
demo(args)

"""
python eval_liteflownet.py --video /Users/liuziyi/Downloads/ln-szln-p001-s0007_main_20221125191111_26.mp4
"""
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--video", default="/Users/liuziyi/Downloads/ln-szln-p001-s0007_main_20221125191111_26.mp4")
#     args = parser.parse_args()
#     demo(args)

    # mask = mask(args.video_path, idx=5001)
    # # cv.imshow("mask", mask)
    # # key = cv.waitKey(0)
    # mask = resize(mask, (mask.shape[0] // 4, mask.shape[1] // 4), anti_aliasing=True)
    # lum = color.rgb2gray(mask)
    # mask = morphology.remove_small_holes(morphology.remove_small_objects(lum < 0.8, 5000),500)
    # mask = morphology.opening(mask, morphology.disk(3))
    # mask = convex_hull_image(~mask)
    # cv.imshow("mask", mask.astype(numpy.uint8))
    # key = cv.waitKey(0)
    # demo(args)