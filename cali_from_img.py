import cv2 as cv
import glob
import numpy as np

# Modified version, based on:
# https://temugeb.github.io/opencv/python/2021/02/02/stereo-camera-calibration-and-triangulation.html

def calibrate_camera(img_folder):
	images_names = sorted(glob.glob(img_folder))
	nfiles = len(images_names)
	images = []
	for imname in images_names:
		im = cv.imread(imname, 1)
		images.append(im)

	#criteria used by checkerboard pattern detector.
	#Change this if the code can't find the checkerboard
	criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

	rows = 6 #number of checkerboard rows.
	columns = 8 #number of checkerboard columns.
	world_scaling = 1. #change this to the real world square size. Or not.

	#coordinates of squares in the checkerboard world space
	objp = np.zeros((rows*columns,3), np.float32)
	objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
	objp = world_scaling* objp

	#frame dimensions. Frames should be the same size.
	width = images[0].shape[1]
	height = images[0].shape[0]

	#Pixel coordinates of checkerboards
	imgpoints = [] # 2d points in image plane.

	#coordinates of the checkerboard in checkerboard world space.
	objpoints = [] # 3d point in real world space

	found = 0
	for frame in images:
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

		#find the checkerboard
		ret, corners = cv.findChessboardCorners(gray, (rows, columns), None)

		if ret == True:
			#print(f"found")
			found += 1

			#Convolution size used to improve corner detection. Don't make this too large.
			conv_size = (11, 11)

			#opencv can attempt to improve the checkerboard coordinates
			corners = cv.cornerSubPix(gray, corners, conv_size, (-1, -1), criteria)
			cv.drawChessboardCorners(frame, (rows,columns), corners, ret)
			cv.imshow('img', frame)
			cv.imwrite(f"/home/pnut/cv/picz/4R.jpg", frame)

			k = cv.waitKey(500)

			objpoints.append(objp)
			imgpoints.append(corners)
		else:
			print(f"not found")

	print(f"found {found}/{nfiles}")

	ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (width, height), None, None)
	#print('rmse:', ret)
	#print('camera matrix:\n', mtx)
	#print('distortion coeffs:', dist)
	#print('Rs:\n', rvecs)
	#print('Ts:\n', tvecs)

	return mtx, dist

def main():
	left = False
	if left:
		print("LCam")
		mtxL, distL = calibrate_camera(f"/home/pnut/cv/picz/left/*.jpg")
	#	cv.imwrite(f"/home/pnut/cv/picz/undist_{right_name}.jpg", left_frame)

	#	np.savetxt(f"/home/pnut/cv/params/mtxL.txt", mtxL, fmt='%0.8f')
	#	np.savetxt(f"/home/pnut/cv/params/distL.txt", distL, fmt='%0.8f')

	right = True
	if right:
		print("\nRCam")
	mtxR, distR = calibrate_camera(f"/home/pnut/cv/picz/right/*.jpg")
	#	cv.imwrite(f"/home/pnut/cv/picz/undist_{right_name}.jpg", right_frame)

	#	np.savetxt(f"/home/pnut/cv/params/mtxR.txt", mtxR, fmt='%0.8f')
	#	np.savetxt(f"/home/pnut/cv/params/distR.txt", distR, fmt='%0.8f')

	print("end of script")

if __name__ == "__main__":
	main()
