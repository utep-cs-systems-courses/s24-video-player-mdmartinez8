#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
from ExtractAndDisplay import extractFrames, displayFrames
import time


def convert_to_grayscale(inputQueue, displayQueue):
    # initialize frame count
    time.sleep(3)
    count = 0
    inFileName = f'frames/grayscale_frame_{count:04d}.bmp'
    # get the next frame file name
    inputFrame = inputQueue.get()
    while inputFrame is not None and count < 739:
        print(f'Converting frame {count}')
        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(inFileName, grayscaleFrame)
        displayQueue.put(grayscaleFrame)
        count += 1
        # load the next frame
        inputFrame = inputQueue.get()
        inFileName = f'frames/grayscale_frame_{count:04d}.bmp'

def main():
    # filename of clip to load
    filename = 'clip.mp4'

    # shared queue
    extractionQueue = queue.Queue()
    displayQueue = queue.Queue()

    # Thread setup for each function
    thread1 = threading.Thread(target=extractFrames, args=(filename, extractionQueue, 9999))
    thread2 = threading.Thread(target=convert_to_grayscale, args=(extractionQueue, displayQueue))
    thread3 = threading.Thread(target=displayFrames, args=(displayQueue,))

    # Starting threads
    thread1.start()


    thread2.start()


    thread3.start()

    # waiting for all threads to complete
    thread1.join()
    thread2.join()
    thread3.join()


if __name__ == '__main__':
    main()
