###Use to simply stream and record from the webcam until you kill
###with control-C. currently outputs to simply "output.avi in 
###Documents/TestingOutput, but that can be changed below as necessary


import cv2
from datetime import datetime, timedelta

cap = cv2.VideoCapture("/dev/video1")

#Define codec and create VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('Documents/TestingOutput/output.avi',fourcc,20.0,(640,480))

while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
	frame = cv2.flip(frame,0)

	#write out flipped frame
	out.write(frame)

	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break
    else:
	break

#Release everything
cap.release()
out.release()
cv2.destroyAllWindows()
