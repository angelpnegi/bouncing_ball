# bouncing_ball
Create a video of ball bouncing adhering to gravity using openCV.


**To run the main script (ball_bouncing):**
  $python3 ball_bounce.py -c "white" -b 2 -g 1 -r 720
  - b represents number of bounces
  - c represents color of the ball
  - g represents gravity
  - r represents height of the frame. width is fixed.

    **running % python3 ball_bounce.py --help gives: **     
        usage: ball_bounce.py [-h] [-c COLOR] [-b BOUNCE] [-g GRAVITY] [-r RESOLUTION]
        optional arguments:
          -h, --help            show this help message and exit
          -c COLOR, --color COLOR
                                color of the ball (preferably values: [white, black, red, green, blue])
          -b BOUNCE, --bounce BOUNCE
                                number of times ball bounces (preferably values: [1, 50])
          -g GRAVITY, --gravity GRAVITY
                                gravity of the ball (preferably values: [1, 10])
          -r RESOLUTION, --resolution RESOLUTION
                                height of the frame (preferably values: [500, 2000])

