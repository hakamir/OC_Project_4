# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import os.path


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p","--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.4,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = [ "background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
vs = VideoStream(src="http://192.168.43.84:8080/?action=stream").start()
time.sleep(2.0)
fps = FPS().start()
nbperson=0

# loop over the frames from the video stream
while True:
	try:
		time1 = time.time()
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 1000 pixels
		#frame = cv2.imread(vs)
		frame = vs.read()
		frame = imutils.resize(frame, width=800)
		# grab the frame dimensions and convert it to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (250, 250)),
			0.007843, (250, 250), (127.5,127.5,127.5), True)

		# pass the blob through the network and obtain the detections and
		# predictions
		net.setInput(blob)
		detections = net.forward()
		nbperson = 0
		# loop over the detections
		for i in np.arange(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by ensuring the `confidence` is
			# greater than the minimum confidence
			if confidence > args["confidence"]:
				# extract the index of the class label from the
				# `detections`, then compute the (x, y)-coordinates of
				# the bounding box for the object
				idx = int(detections[0, 0, i, 1])
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				# draw the prediction on the frame
				if CLASSES[idx] == "person" :
					label = "{} {}: {:.2f}%".format(CLASSES[idx], i,
						confidence * 100)
					cv2.rectangle(frame, (startX, startY), (endX, endY), 3)
					y = startY - 15 if startY - 15 > 15 else startY + 15
					cv2.putText(frame, label, (startX, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
					#print("\r\r\r\r\r\r\r\r")
					#print("Person %s" %i)
					#print("###########################")
					#print("start x : %s " % startX)
					#print("start y : %s " % startY)
					#print("end x : %s " % endX)
					#print("end y : %s " % endY)
					#print("###########################")
					nbperson = i + 1 
			
		print("Nombre de personnes :",nbperson)
		file = open("persons.txt", "w")
		file.write(str(nbperson))
		file.close()		


		# show the output frame
		cv2.imshow("Deep Learning detection window", frame)
		key = cv2.waitKey(1)

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

		# update the FPS counter
		fps.update()
		time2 = time.time()
		print("FPS : %s" %round(1/(time2-time1)))
		print("\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r")
	except AttributeError:
		print("Missed frame.")

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
