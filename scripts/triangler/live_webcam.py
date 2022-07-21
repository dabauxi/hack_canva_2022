import cv2
import triangler

configs = {
    "img_win_name": "image"
}

def main():
    print("starting webcam...")
    cv2.namedWindow(configs["img_win_name"])
    vc = cv2.VideoCapture(2)
    
    triangler_instance = triangler.Triangler()

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
        
        if key == ord("s"):
            # Convert and save as an image
            img = triangler_instance.triangulate_img(frame)
            img = cv2.flip(img, 1)
            cv2.imshow("triangulate", img)
            
    cv2.destroyWindow(configs["img_win_name"])
    vc.release()
    
    
if __name__ == "__main__":
    main()