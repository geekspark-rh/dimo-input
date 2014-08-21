import numpy as np
import cv2
import time
import json


stop_key = ord('q')
low_m  = 90
high_m = 255

colors = {
    'red' : {
        'color': (0, 0, 255),
        'lower': np.array([0, low_m, low_m], dtype=np.uint8),
        'upper': np.array([10, high_m, high_m], dtype=np.uint8)

    },
    'green' : {
        'color': (0, 255, 0),
        'lower': np.array([60, low_m, low_m], dtype=np.uint8),
        'upper': np.array([90, high_m, high_m], dtype=np.uint8)
    },
    'blue' : {
        'color': (255, 0, 0),
        'lower': np.array([110, low_m, low_m], dtype=np.uint8),
        'upper': np.array([130, high_m, high_m], dtype=np.uint8)
    }
}

class Finder:

    def get_default_tracker(self):
        return {
            'count': 0,
            'red'  : {'x': 100, 'y': 100},
            'green': {'x': 100, 'y': 100},
            'blue' : {'x': 100, 'y': 100}
        }

    def init(self, server, opts):

        fps = 30 # frames per second
        duration = 1000.0 / 60 # duration of each frame in ms

        cap = cv2.VideoCapture(opts['camera'])

        if opts['debug']:
            while(True):
                server.sendMessage(json.dumps(self.get_default_tracker()))


        tracker = self.get_default_tracker()
        while(True):

            # Capture frame-by-frame
            ret, orig = cap.read()

            if ret == False:
                continue

            start = time.time()

            # blur image
            frame = cv2.blur(orig, (5,5))
            #frame = orig

            # convert to hsv for matching
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # loop over each color
            for k, color in colors.iteritems():
                # get a mask back of the "inRange" colors
                mask = cv2.inRange(hsv, color['lower'], color['upper'])

                # get the image moments from the mask
                moments = cv2.moments(mask, True)

                # if there is an area
                area = moments['m00']
                if area:
                    x = int(moments['m10'] / area)
                    y = int(moments['m01'] / area)

                    tracker[k] = {}
                    tracker[k]['x'] = x
                    tracker[k]['y'] = y

                    cv2.circle(frame, (x, y), 10, color['color'], -1)
                    res = cv2.bitwise_and(frame, frame, mask = mask)
                    cv2.imshow(k, res)

            tracker['count'] = tracker['count'] + 1
            server.sendMessage(json.dumps(tracker))
            # frame = cv2.resize(frame, (frame.shape[1] * 2, frame.shape[0] * 2))
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == stop_key:
                break

            end = time.time()
            time.sleep((duration - (end - start))/1000.0)
            # print("Frame took %0.3f" % ((end - start) * 1000))


        # When everything is done, release the capture
        cap.release()
        cv2.destroyAllWindows()
