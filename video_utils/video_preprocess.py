import cv2
import matplotlib.pyplot as plt
from typing import Sequence
import numpy as np
from numpy import ndarray


def create_video(frames: Sequence[ndarray], out: str, fourcc: int, fps: int,
                 size: tuple) -> None:
    """Create a video to save the optical flow.
    Args:
        frames (list, tuple): Image frames.
        out (str): The output file to save visualized flow map.
        fourcc (int): Code of codec used to compress the frames.
        fps (int):      Framerate of the created video stream.
        size (tuple): Size of the video frames.
    """
    # init video writer
    video_writer = cv2.VideoWriter(out, fourcc, fps, size, True)

    for frame in frames:
        video_writer.write(frame)
    video_writer.release()

def merge_videos(videos: Sequence[str], out: str):
    init = 0
    for v in videos:
        cap = cv2.VideoCapture(v)
        if not init:
            size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            fps = cap.get(cv2.CAP_PROP_FPS)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(out, fourcc, fps, size, True)
            init = 1
        while cap.isOpened():
            flag, img = cap.read()
            if not flag:
                break
            video.write(img)
        cap.release()
    video.release()

def cut_video(video: str, out: str, start: int, stop: int):
    cap = cv2.VideoCapture(video)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    size = (768, 384)
    video = cv2.VideoWriter(out, fourcc, fps, size, True)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, start * fps)
    pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
    while pos <= stop * fps:
        flag, img = cap.read()
        img = cv2.resize(img, size)
        video.write(img)
        if not flag:
            break
        pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
    cap.release()
    video.release()

def resize_video(video: str, out: str):
    cap = cv2.VideoCapture(video)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc('I','4','2','0')
    size = (768, 384)
    video = cv2.VideoWriter(out, fourcc, fps, size, True)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, start * fps)
    pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
    i = 0
    while (pos <= stop * fps) and (i < 200):
        flag, img = cap.read()
        img = cv2.resize(img, size)
        video.write(img)
        if not flag:
            break
        pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
        i += 1
    cap.release()
    video.release()

def extract_frames(video: str, dir: str, index: Sequence[int]):
    """
    Parameters:
    video: path of video from which to extract frames.
    dir: directory to save extracted frames.
    index: which frames to be extracted.

    Usage:
    index = list(range(0, 10000, 100))
    extract_frames('video.mp4', 'save_dir', index)
    """
    cap = cv2.VideoCapture(video)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # cap.set(cv2.CAP_PROP_POS_FRAMES, index[0])
    # pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
    i = 0
    while (i < len(index)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, index[i])
        flag, img = cap.read()
        if not flag:
            break
        path = dir + '/' + video.split('/')[-1] + '__' + str(index[i]) + '.jpg'
        print('path is ', path)
        cv2.imwrite(path, img, [int(cv2.IMWRITE_JPEG_QUALITY),100])
        # pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
        i += 1
    
    cap.release()