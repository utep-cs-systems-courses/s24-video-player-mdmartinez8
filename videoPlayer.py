import threading
import cv2
import numpy as np
import base64
import queue
from ExtractAndDisplay import extractFrames, displayFrames


def convert_to_grayscale(inputQueue, outputDir):
    # initialize frame count
    count = 0
    inFileName = f'{outputDir}/grayscale_frame_{count:04d}.bmp'
    # get the next frame file name
    inputFrame = inputQueue.get()
    while inputFrame is not None and count < 739:
        print(f'Converting frame {count}')
        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(inFileName, grayscaleFrame)
        inputQueue.put(grayscaleFrame)
        count += 1
        # load the next frame
        inputFrame = inputQueue.get()
        inFileName = f'{outputDir}/grayscale_frame_{count:04d}.bmp'

def main():
    # filename of clip to load
    filename = 'clip.mp4'
    outputDir = 'frames'

    # shared queue
    extractionQueue = queue.Queue()

    # Thread setup for each function
    thread1 = threading.Thread(target=extractFrames, args=(filename, extractionQueue, 9999))
    thread2 = threading.Thread(target=convert_to_grayscale, args=(extractionQueue, outputDir))
    thread3 = threading.Thread(target=displayFrames, args=(extractionQueue,))

    # Starting threads
    thread1.start()
    thread1.join()

    thread2.start()
    thread2.join()

    thread3.start()
    thread3.join()
    # Waiting for all threads to complete





if __name__ == '__main__':
    main()
