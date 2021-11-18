import cv2
import numpy as np
import math
import pymsgbox
from SimpleXMLRPCServer import SimpleXMLRPCServer

# Defining the dimensions of checkerboard
CHECKERBOARD = (7,10)   # (heigth,width)
check_size = 22.3     # size of squares in mm
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Defining the coordinates of the checkerboard crosspoints that the camera will detect
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp = objp*check_size

# Define internal camera variables
mtx = np.matrix([[1.51832488e+03, 0.00000000e+00, 1.29086673e+03],[0.00000000e+00, 1.51879862e+03, 1.01228124e+03],[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist = np.array([-0.33306284,  0.19744536,  0.00151984, -0.00074798, -0.19647672])

def _get_rot_dist():

    # Get grayscale of image and find crosspoints
    #img = _get_image_on_press()
    img = _get_image()

    #img = cv2.imread(image)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD)
    if not (ret):
        raise ValueError()

    # Refine pixel coordinates
    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    
    # Calculate distance vector and rotation matrix
    ret,rvec,tvec = cv2.solvePnP(objp, corners2, mtx, dist)
    rotMat,_ = cv2.Rodrigues(rvec)
    
    return (rotMat, tvec)
    
def _get_euler_angles (rotMatBase, rotMatCal):
    rotMatTot = np.matmul(rotMatBase.transpose(),rotMatCal)
    rx = math.atan(rotMatTot[2,1]/rotMatTot[2,2])
    ry = - math.sin(rotMatTot[2,0])
    rz = math.atan(rotMatTot[1,0]/rotMatTot[0,0])

    rx = rx*180/math.pi
    ry = ry*180/math.pi
    rz = rz*180/math.pi

    return (rx, ry, rz)

def _get_image_on_press():
    cap = cv2.VideoCapture('rtsp://user1:Dymat0!1!@192.168.0.64:554/profile2/media.smp', cv2.CAP_FFMPEG)
    while True:
        ret, frame = cap.read()
        if not ret:
            return ValueError()

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            return frame

def _get_image():
    cap = cv2.VideoCapture('rtsp://user1:Dymat0!1!@192.168.0.64:554/profile2/media.smp', cv2.CAP_FFMPEG)
    ret, frame = cap.read()
    if not ret:
        return ValueError()
    return frame 

def calibrate_camera():
    # Creating vector to store coordinates checkerboard crosspoints in real world
    objpoints = []
    # Creating vector to store coordinates checkerboard crosspoints on image
    imgpoints = [] 

    for i in range (1,11):
        img = _get_image_on_press()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board crosspoints
        # If desired number of crosspoints are found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+
            cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
        
        """
        If desired number of crosspoints are detected,
        pixel coordinates are refined and coordinates are stored in vector
        """
        if ret == True:
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            
            # Add coordinate points to vector
            imgpoints.append(corners2)  # coordinates in image
            objpoints.append(objp)      # coordinates in real world
        else:
            pymsgbox.alert('Try again!','Pas op!')
            i = i-1 

    """
    Performing camera calibration by 
    passing the value of known coordinates in real world (objpoints)
    and corresponding pixel coordinates in images of the 
    detected crosspoints (imgpoints)
    """
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

    print(mtx)
    print(dist)

def initial_calibration():
    try:
        (calRotMat, calTvec) = _get_rot_dist()
    except ValueError:
        return "Something went wrong"

    totvec = []
    for i in calTvec:
        totvec.append(i.item())
    for i in calRotMat:
        for q in i:
            totvec.append(q.item())      
    return totvec

def operation_calibration(initVec):

    calRotMat = np.zeros([3,3])
    calTvec = np.zeros([3,1])

    for i in range (0,3):
        calTvec[i] = initVec[i]
        for q in range(0,3):
            calRotMat[i,q] = initVec[q+(3*(i+1))]


    try:
        (operRotMat, operTvec) = _get_rot_dist()
    except ValueError:
        return "Couldn't get rotation and dist vectors"

    tvecRel = operTvec - calTvec
    rvecRel = _get_euler_angles(calRotMat,operRotMat)

    return [tvecRel.item(0),tvecRel.item(1),tvecRel.item(2),rvecRel[0],rvecRel[1],rvecRel[2]]


host = 'localhost'
port = 60050
server = SimpleXMLRPCServer((host, port))
server.register_function(calibrate_camera, "ext_calibrate_camera")
server.register_function(initial_calibration, "ext_initial_calibration")
server.register_function(operation_calibration, "ext_operation_calibration")
server.serve_forever()
