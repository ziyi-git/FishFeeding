import threading, queue
import cv2
import math
import numpy as np
from PIL import Image
import torch

#https://vuamitom.github.io/2019/12/13/fast-iterate-through-video-frames.html
class Worker(threading.Thread):
    def __init__(self, mask=None, transforms=None):
        threading.Thread.__init__(self)
        self.queue = queue.Queue(maxsize=20)
        # self.wid = np.random.randint(0, 1000)
        self.mask = mask
        # self.transforms = transforms
    
    def decode(self, video_path, fnos, callback):
        self.queue.put((video_path, fnos, callback))
    
    def run(self):
        """the run loop to execute frame reading"""
        video_path, fnos, on_decode_callback = self.queue.get()
        cap = cv2.VideoCapture(video_path)
        
        # set initial frame 
        cap.set(cv2.CAP_PROP_POS_FRAMES, fnos[0])
        success = cap.grab()
        
        results = []
        idx, count = 0, fnos[0]
        img_pair = []
        while success:
            if count == fnos[idx]:
                success, img = cap.retrieve()
                # 对图像做预处理
                size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 4), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 4))
                img = cv2.resize(img, size)
                if self.mask is not None:
                    img = cv2.bitwise_and(img, img, mask=self.mask.astype(np.uint8))
                img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                img = torch.FloatTensor(np.ascontiguousarray(np.array(img)[:, :, ::-1].transpose(2, 0, 1).astype(np.float32) * (1.0 / 255.0)))
                img_pair.append((fnos[idx], img))
                if success:
                    if len(img_pair) > 1:
                        # on_decode_callback((fnos[idx], image))
                        on_decode_callback(img_pair)
                        img_pair = [img_pair[1]]
                else:                
                    break                    
                idx += 1
                if idx >= len(fnos):
                    break
            count += 1
            success = cap.grab()