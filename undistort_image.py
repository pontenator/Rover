import cv2 as cv
import glob
import numpy as np
from pathlib import Path


def read_params():
	distL = np.loadtxt(f"/home/pnut/cv/params/distL.txt")
	distR = np.loadtxt(f"/home/pnut/cv/params/distR.txt")

	mtxL = np.loadtxt(f"/home/pnut/cv/params/mtxL.txt")
	mtxR = np.loadtxt(f"/home/pnut/cv/params/mtxR.txt")

	return mtxL, distL, mtxR, distR


def undistort_func(img0, dist_coeffs, camera_matrix):
	# Load the image
	image = cv.imread(img0, 1)
	height, width = image.shape[:2]

	# Get the new camera matrix
	newcameramatrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (width, height), 1, (width, height))

	# Return the undistorted image
	return cv.undistort(image, camera_matrix, dist_coeffs, None, newcameramatrix)

def main():
	# Read params
	mtxL, distL, mtxR, distR  = read_params()

	# Grab files
	left_files = sorted(glob.glob(f'/home/pnut/cv/picz/left/*'))
	right_files = sorted(glob.glob(f'/home/pnut/cv/picz/right/*'))
	zipped_files = zip(left_files, right_files)

	# Undistort each file in img folder
	for left_file, right_file in zipped_files:
		# Grab names
		left_name = Path(left_file).stem
		right_name = Path(right_file).stem

		left_undist_img = undistort_func(left_file, distL, mtxL)
		cv.imwrite(f"/home/pnut/cv/picz/undist_{left_name}.jpg", left_undist_img)

		right_undist_img = undistort_func(right_file, distR, mtxR)
		cv.imwrite(f"/home/pnut/cv/picz/undist_{right_name}.jpg", right_undist_img)

	cv.waitKey(0)
	cv.destroyAllWindows()
	print("end of script")

if __name__ == "__main__":
	main()
