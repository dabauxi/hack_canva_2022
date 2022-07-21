import cv2
import numpy as np
from face_landmarks_detect import detect_landmarks
from utils import draw_delaunay, draw_voronoi


configs = {
    "img_win_name": "image",
    "num_l_pts": 68  # either 28 or 68
}


def _compute_landmarks(img):
    # detect facial landmarks 
    landmarks = detect_landmarks(img)
    
    if landmarks is None:
        return None

    # use 28 of the 68 landmarks provided by dlib shape-predictor
    if configs["num_l_pts"] == 28:
        mask = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 21, 22, 23, 25, 27, 29, 30, 31, 35, 36, 39, 42, 45, 48, 51, 54, 57]
        landmarks = [landmarks[i] for i in mask]
    return landmarks


def _vis_voronoi_diagram(img, landmark_pts):
    subdiv = _init_subdiv(img)
    try:
        for p in landmark_pts:
            subdiv.insert(p)
    except Exception:
        return 
        
    # allocate space for voronoi Diagram
    img_voronoi = np.zeros(img.shape, dtype=img.dtype)

    # voronoi diagram
    # img_voronoi = cv2.flip(img_voronoi, 1)
    draw_voronoi(img_voronoi, subdiv)
    # cv2.imshow("voronoi", img_voronoi)


def _init_subdiv(img):
    # image rect. to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])

    # init an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect)
    return subdiv


def _first_frame_del_animate(img):
    """Perform Delaunay animation only on the first frame.

    Args:
        img (np.array): first frame captured after the start button.
    """
    # compute landmark on the first frame
    landmark_pts = _compute_landmarks(img)
    if landmark_pts is None:
        return
    
    # init subdiv only once
    subdiv = _init_subdiv(img)
    
    # insert points into subdiv and animate
    for p in landmark_pts:
        try:
            subdiv.insert(p)
        except Exception:
            return
        img_copy = img.copy()
        
        # draw & show delaunay triangles
        draw_delaunay(img_copy, subdiv, (0, 255, 255))
        
        img_copy = cv2.flip(img_copy, 1)
        cv2.imshow(configs["img_win_name"], img_copy)
        cv2.waitKey(100)
           

def main():
    print("starting webcam...")
    cv2.namedWindow(configs["img_win_name"])
    vc = cv2.VideoCapture(2)

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
        
    else:
        rval = False
        
    frame_id = 0
    while rval:
        frame = cv2.flip(frame, 1)
        
        cv2.imshow(configs["img_win_name"], frame)
        rval, frame = vc.read()
        frame_id += 1
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # exit on ESC
            break
        
        # if key == ord("s"):
        #     start_key_id += 1
        #     # for the first frame do the delaunay animation only
        #     if start_key_id == 1:
        #         _first_frame_del_animate(frame)
                
        #         landmarks = _compute_landmarks(frame)
        #         if landmarks is not None:
        #             _vis_voronoi_diagram(frame, landmark_pts=landmarks)
                    
                    
        if key == ord("s"):
            _first_frame_del_animate(frame)
            
            landmarks = _compute_landmarks(frame)
            if landmarks is not None:
                _vis_voronoi_diagram(frame, landmark_pts=landmarks)
                
        # # for rest do the voronoi diagram
        # if start_key_id >= 1:            
        #     landmarks = _compute_landmarks(frame)
        #     if landmarks is not None:
        #         _vis_voronoi_diagram(frame, landmark_pts=landmarks)
            
    cv2.destroyWindow(configs["img_win_name"])
    vc.release()
    
    
if __name__ == "__main__":
    main()