import cv2

class Compose(object):
    def __init__(self, transforms):
        self.transforms = transforms
    
    def __call__(self, img, target=None):
        for trans in self.transforms:
            img, target = trans(img, target)
        return img, target

class Resize(object):
    def __init__(self, dst_size):
        self.dst_size = dst_size
    
    def __call__(self, img, target):
        img = cv2.resize(img, self.dst_size)
        return img, target