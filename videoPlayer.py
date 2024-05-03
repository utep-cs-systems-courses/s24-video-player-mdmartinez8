#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
import time
from queue import Empty

def displayFrames(inputBuffer):
    time.sleep(5)
    count = 0
    empty_retries = 0  # To count how many times the queue is found empty

    while True:
        try:
            frame = inputBuffer.get(timeout=1)  # Wait for a frame for up to 1 second
            print(f'Displaying frame {count}')
            cv2.imshow('Video', frame)
            if cv2.waitKey(42) & 0xFF == ord("q"):
                break
            count += 1
            empty_retries = 0  # Reset retries count on successful get
        except Empty:
            empty_retries += 1
            if empty_retries > 5:  # Exit if the queue has been empty for several tries
                print("No more frames to display.")
                break

    print('Finished displaying all frames')
    cv2.destroyAllWindows()

def extractFrames(fileName, outputBuffer, maxFramesToLoad=9999):
    # Initialize frame count
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success, image = vidcap.read()

    print(f'Reading frame {count} {success}')
    while success and count < maxFramesToLoad:
        # add the frame to the buffer
        outputBuffer.put(image)

        success, image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1

    print('Frame extraction complete')

def convert_to_grayscale(inputQueue, displayQueue):
    time.sleep(3)
    count = 0

    while True:
        try:
            # Attempt to get a frame with a timeout
            inputFrame = inputQueue.get(timeout=10)
            if inputFrame is None:
                print('No more frames to process.')
                break
            print(f'Converting frame {count}')
            # Convert the image to grayscale
            try:
                grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
                displayQueue.put(grayscaleFrame)
                count += 1
            except Exception as e:
                print(f"Error converting frame {count}: {e}")
        except Empty:
            print('No frame received in 10 seconds, stopping conversion.')
            break

    print('Frame conversion complete')

def main():
    # filename of clip to load
    filename = 'clip.mp4'

    # shared queue
    extractionQueue = queue.Queue()
    displayQueue = queue.Queue()

    # Thread setup for each function
    thread1 = threading.Thread(target=extractFrames, args=(filename, extractionQueue, 9999))
    thread2 = threading.Thread(target=convert_to_grayscale, args=(extractionQueue, displayQueue))
    #thread3 = threading.Thread(target=displayFrames, args=(displayQueue,))

    # Starting threads
    thread1.start()


    thread2.start()


    #thread3.start()

    # waiting for all threads to complete
    thread1.join()
    thread2.join()
    #thread3.join()
    displayFrames(displayQueue)

if __name__ == '__main__':
    main()
