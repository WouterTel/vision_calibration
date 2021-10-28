import cv2
import numpy as np
import os
import glob
from xmlrpc.server import SimpleXMLRPCServer
#import xmlrpclib
#from SimpleXMLRPCServer import SimpleXMLRPCServer
import pymsgbox

# Defining the dimensions of checkerboard
CHECKERBOARD = (7,10)
check_size = 23
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp = objp*check_size
prev_img_shape = None

def set_base_calibration():
        
    # Creating vector to store vectors of 3D points for each checkerboard image
    objpoints = []
    # Creating vector to store vectors of 2D points for each checkerboard image
    imgpoints = [] 

    # Extracting path of individual image stored in a given directory
    images = glob.glob('./afbeeldingen/*.jpg')
    for fname in images:
        print('processing image:' + fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        # If desired number of corners are found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+
            cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
        
        """
        If desired number of corner are detected,
        we refine the pixel coordinates and display 
        them on the images of checker board
        """
        if ret == True:
            objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2,ret)
        
        #cv2.imshow('img',img)
        #cv2.waitKey(0)

    #cv2.destroyAllWindows()

    #h,w = img.shape[:2]

    """
    Performing camera calibration by 
    passing the value of known 3D points (objpoints)
    and corresponding pixel coordinates of the 
    detected corners (imgpoints)
    """
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    np.save('calibration/mtx.npy',mtx)
    np.save('calibration/dist.npy',dist)

def calibrate_robot():
    img = cv2.imread('test_afbeelding/test_dist_300mm.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+
            cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)

    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

    mtx = np.load('calibration/mtx.npy')
    dist = np.load('calibration/dist.npy')
    ret,rvec,tvec = cv2.solvePnP(objp, corners2, mtx, dist)
    rotMat,_ = cv2.Rodrigues(rvec)

    return ('Hello!')

response = pymsgbox.alert('Hij draait!','Pas op!')
server = SimpleXMLRPCServer(("localhost", 60050))
server.register_function(calibrate_robot, "ext_calibrate_robot")
server.serve_forever()
"""
if __name__ == "__main__":
    (rotMat, tvec) = calibrate_robot()
    print(rotMat)
    print(tvec)
"""