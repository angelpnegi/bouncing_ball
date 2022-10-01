import cv2
import numpy as np
import argparse
from cv2 import VideoWriter, VideoWriter_fourcc

def main(ball_color, bounce, gravity, height, number_of_balls):

    # print(ball_color, bounce, gravity, height)
    if ball_color=="black":
        color = (0, 0, 0)
    elif ball_color=="white":
        color = (256, 256, 256)
    elif ball_color=="blue":
        color = (256, 0, 0)
    elif ball_color=="red":
        color = (0, 0, 256)
    elif ball_color=="green":
        color = (0, 256, 0)
    else: # black default
        color = (0, 0, 0)

    width = int(height*1280/720)      #input
    # height = 720     #input
    FPS = 24
    radius = int(height*0.1)
    # number_of_balls = 1

    fourcc = VideoWriter_fourcc(*'MP42')
    video = VideoWriter('./gravity_bounce.avi', fourcc, float(FPS), (width, height))

    # bounce = 100      #input
    # gravity = 10     #input

    if number_of_balls<=3:
      paint_h = [int(radius*1.1), int(height/2-radius), int(0)]
      paint_w = [int(width/2), int(width/4), int(3*width/4)]
    else:
      paint_h = np.random.randint(height, size=number_of_balls)-2*radius
      paint_w = np.linspace(radius, width-radius, number_of_balls).astype(int).tolist()

    # print(paint_w, paint_h, radius, width-radius)

    y = [] # variable representing changes in y-path due to gravity. more towards the ground, lower in the air.
    negative = [] # to check if the variable y becomes negative at least once between a bounce. (else signifies that ball has stopped bouncing)
    flag = [] # to take care of the boundary case where ball has no energy left to bounce again (found by variable 'negative')
    count = []  # count the number of frames (for documentation)
    after = []  # to handle edge cases when more number of bounces are given and the ball stops before it reaches the number
    c = 0
    bounces = []
    for i in range(number_of_balls):
      bounces.append(bounce)
      y.append(0)
      negative.append(0)
      flag.append(0)
      count.append(0)
      after.append(0)

    while True:
      # print(c)
      c += 1
      frame = np.full((height, width, 3), 128, np.uint8)
      for i in range(number_of_balls):
        # print("ball", i, flag[i], y[i], paint_h[i])
        # change in y
        y[i] += gravity
        paint_h[i] += y[i]

        if y[i]<0:
          negative[i] = 1

        # set the y
        if flag[i]==0:
          cv2.circle(frame, (paint_w[i], paint_h[i]), radius, color, -1)
        else:   # once the ball stops, stop y coordinate fom changing.
          cv2.circle(frame, (paint_w[i], flag[i]), radius, color, -1)

        # check for bounce
        if paint_h[i]>=height-int(radius*1.5) and y[i]>0:
            # print("####", i, flag[i], y[i], paint_h[i])
            y[i] *= -1
            bounces[i] -= 1
            if negative[i]==0 and flag[i]==0 and count[i]!=0:
              flag[i] = paint_h[i]
              after[i] += 1
            negative[i] = 0
            count[i] += 1
        if after[i]!=0:
            after[i]+=1
      if max(bounces)<0 or min(after)>24:
          break
      video.write(frame)
    video.release()

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--color', required=False,
                        help='color of the ball (preferably values: [white, black, red, green, blue])')
    parser.add_argument('-b', '--bounce', required=False,
                        help='number of times ball bounces (preferably values: [1, 50])')
    parser.add_argument('-g', '--gravity', required=False,
                        help='gravity of the ball (preferably values: [1, 10])')
    parser.add_argument('-r', '--resolution', required=False,
                        help='height of the frame (preferably values: [500, 2000])')
    parser.add_argument('-n', '--number', required=False,
                        help='number of balls to bounce (preferably values: [1, 10])')
    args = parser.parse_args()

    ball_color = "white"
    bounce = 2
    gravity = 1
    height = 720
    number = 3

    if args.color!=None:
        ball_color = args.color
    if args.bounce!=None:
        bounce = int(args.bounce)
    if args.gravity!=None:
        gravity = int(args.gravity)
    if args.resolution!=None:
        height = int(args.resolution)
    if args.number!=None:
        number = int(args.number)
    if args.number=="0":
        number = 1

    # print(type(ball_color), type(bounce), type(gravity), type(height))

    main(ball_color, bounce, gravity, height, number)
