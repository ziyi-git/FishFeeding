import cv2
from skimage import color, morphology, img_as_float
from skimage.io import imread, imshow, imsave
from skimage.transform import resize
from skimage.morphology import convex_hull_image
import numpy as np

def _get_mask(img):    
    img = img_as_float(img) # opencv to skimage
    img = resize(img, (img.shape[0] // 4, img.shape[1] // 4), anti_aliasing=True)
    lum = color.rgb2gray(img)
    mask = morphology.remove_small_holes(morphology.remove_small_objects(lum < 0.8, 5000),500)
    mask = morphology.opening(mask, morphology.disk(3))
    mask = convex_hull_image(~mask)
    
    imsave('mask.png', mask)
    np.save('mask.npy', mask)

    return mask

def resize_and_mask_video(video_path, out_video_path=None, show_out_video=False):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(frame_width // 4), int(frame_height // 4))
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 5000)
    ret, frame = cap.read()
    mask = _get_mask(frame)

    if out_video_path is not None:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或者使用 'XVID'
        out = cv2.VideoWriter(out_video_path, fourcc, fps, size)
    
    ii = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, size)
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

resize_and_mask_video("/Users/liuziyi/workspace/FishFeeding/demo.mp4", "/Users/liuziyi/workspace/FishFeeding/demo_out.mp4")
# _get_mask("/Users/liuziyi/Desktop/TMP/xx_c/demo.mp4", 5000)

# from skimage import color, morphology, img_as_float
# from skimage.io import imread, imshow
# from skimage.transform import resize
# from skimage.morphology import convex_hull_image

# img = imread('path_to_your_image_file')
# img = resize(img, (img.shape[0] // 4, img.shape[1] // 4), anti_aliasing=True)
# lum = color.rgb2gray(img)
# mask = morphology.remove_small_holes(morphology.remove_small_objects(lum < 0.8, 5000),500)
# mask = morphology.opening(mask, morphology.disk(3))
# mask = convex_hull_image(~mask)

