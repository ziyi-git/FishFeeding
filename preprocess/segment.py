import cv2
from skimage import color, morphology, img_as_float
from skimage.io import imread, imshow, imsave
from skimage.transform import resize
from skimage.morphology import convex_hull_image
import numpy as np


def _get_mask(img):    
    img = img_as_float(img) # opencv to skimage
    lum = color.rgb2gray(img)
    mask = morphology.remove_small_holes(morphology.remove_small_objects(lum < 0.8, 5000),500)
    mask = morphology.opening(mask, morphology.disk(3))
    mask = convex_hull_image(~mask)
    
    imsave('mask.png', mask)
    np.save('mask.npy', mask)

    return mask

def mask_video(video_path, out_video_path=None, show_out_video=False):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening {video_path}\n")
    else:
        print(f"Open {video_path}\n")
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 5000)
    ret, frame = cap.read()
    mask = _get_mask(frame)

    if out_video_path is not None:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或者使用 'XVID'
        out = cv2.VideoWriter(out_video_path, fourcc, fps, (frame_width, frame_height))
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.bitwise_and(frame, frame, mask=mask.astype(np.uint8))
            if show_out_video:
                cv2.imshow('Frame', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            if out_video_path is not None:
                out.write(frame)
        else:
            break
    
    cap.release()
    out.release()
    if show_out_video:
        cv2.destroyAllWindows()

# resize_and_mask_video("/Users/liuziyi/workspace/FishFeeding/demo2.mp4", "/Users/liuziyi/workspace/FishFeeding/demo_out.mp4")

def capture_frame(video_path, fno=0):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening {video_path}\n")
    else:
        print(f"Open {video_path}\n")
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
    ret, frame = cap.read()

    cv2.imwrite('frame.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])