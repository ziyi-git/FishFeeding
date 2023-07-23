import threading, queue
import cv2
import numpy as np

class Worker(threading.Thread):
    def __init__(self, transforms=None):
        threading.Thread.__init__(self)
        self.queue = queue.Queue(maxsize=20)
        self.transforms = transforms
    
    def decode(self, video_path, fnos, callback):
        self.queue.put((video_path, fnos, callback))
    
    def run(self):
        """the run loop to execute frame reading"""
        video_path, fnos, on_decode_callback = self.queue.get()
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, fnos[0])  # set initial frame 
        success = cap.grab()
        idx, count = 0, fnos[0]
        
        while success:
            if count == fnos[idx]:
                success, img = cap.retrieve()
                if success:
                    img, _ = self.transforms(img)
                    # for trans in self.transforms:
                    #     img = trans(img)
                    # on_decode_callback(img)
                    on_decode_callback((count, img))
                else:
                    break
                idx += 1
                if idx >= len(fnos):
                    break
            count += 1
            success = cap.grab()