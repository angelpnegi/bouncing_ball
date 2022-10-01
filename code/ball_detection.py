import os
import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

def concat_vh(list_2d):
  # return final image
  return cv2.vconcat([cv2.hconcat(list_h) 
                        for list_h in list_2d])

def main(path):
    color = (256, 256, 256)
    video = cv2.VideoCapture('gravity_bounce.avi')
    FPS = video.get(cv2.CAP_PROP_FPS)
    width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
    fourcc = VideoWriter_fourcc(*'MP42')
    video_overlay = VideoWriter('./gravity_overlay.avi', fourcc, float(FPS), (width, height))
    # print('frames per second =', fps)
    count = 0
    while True:
        success, image = video.read()
        if not success:
            break 
        # Convert to grayscale.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Blur using 3 * 3 kernel.
        gray_blurred = cv2.blur(gray, (3, 3))
        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT,
                                            1, 20, param1 = 50, param2 = 30)

        # Draw circles that are detected.
        if detected_circles is not None:
            # print(count, "detected")
            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))
            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
                # Draw the circumference of the circle.
                cv2.circle(image, (a, b), r, (0, 255, 0), 2)
                # Draw a small circle (of radius 1) to show the center.
                cv2.circle(image, (a, b), 1, (0, 0, 255), 3)
                # make border
                cv2.copyMakeBorder(image, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                # write the image number on the left top corner of image
                cv2.putText(image, str(count), (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                cv2.imwrite(path+"/result%d.jpg" % count, image)     # save frame as JPEG file 
                # create video with overlay   
                # img = cv2.imread("result"+str(count)+".jpg")
                frame = np.full((height, width, 3), 128, np.uint8)
                # print(type(frame), type(image))
                video_overlay.write(image) #cv2.imread("result"+str(count)+".jpg"))
        count += 1
    video_overlay.release()
    index = np.linspace(0, count-1, 16).astype(int).tolist()
    # print(index)
    k = 0
    images = []
    for i in range(4):
        img = []
        for j in range(4):
            img.append(cv2.imread(path+"/result"+str(index[k])+".jpg"))
            k += 1
        images.append(img)
    img_tile = concat_vh(images)
    # show the output image
    cv2.imwrite("result_grid.jpg", img_tile)     # save frame as JPEG file    
    # cv2.imshow('concat_vh.jpg', img_tile)

if __name__=="__main__":
    path = './detection_images'    
    try: 
        os.mkdir(path) 
    except OSError as error: 
        pass
        # print(error)
    main(path)
