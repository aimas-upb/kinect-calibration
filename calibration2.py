import cv2
import numpy as np
import math
import scipy.odr

eps = 0.1
inf = (1<<20)
nrlin = 8
nrcol = 9

#load mappings
dataf1 = open('/home/pauey/AIMAS/imagine_prel/Camera1_mapping.txt', 'r')
dataf2 = open('/home/pauey/AIMAS/imagine_prel/Camera2_mapping.txt', 'r')

data1 = np.loadtxt(dataf1)
depth1 = {}
data2 = np.loadtxt(dataf2)
depth2 = {}

for i in range(0, data1.shape[0]):
	depth1[(data1[i][3], data1[i][4])] = data1[i][0]

for i in range(0, data2.shape[0]):
	depth2[(data2[i][3], data2[i][4])] = data2[i][0]

def mindist(point, point_set): #calculate the minimal distance between current point and the checkerboard points
	d = 640
	for i in point_set:
		di = (point[0] - i[0]) * (point[0] - i[0]) + (point[1] - i[1]) * (point[1] - i[1])
		if(di < d and di > eps):
			d = di
	return math.sqrt(d)

#load images
filename1 = '/home/pauey/AIMAS/imagine_prel/rgb1.bmp' 
filename2 = '/home/pauey/AIMAS/imagine_prel/rgb2.bmp'

def get_corners(filename, depth):
	# get harris corners
	img = cv2.imread(filename)
	img2 = cv2.medianBlur(img, 3)  #apply 3x3 median filter to remove salt&pepper noise
	gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
	gray = np.float32(gray)
	dst = cv2.cornerHarris(gray,2,3,0.04) # image (gray&floar32), block size, ksize (aperture parameter of Sobel derivative used), k (Harris detector free parameter)
	dst = cv2.dilate(dst,None)
	ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
	dst = np.uint8(dst)

	# find centroids
	ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

	# refine the harris corners
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
	corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
	
	# get chessboard corners
	gray2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret2, corners2 = cv2.findChessboardCorners(gray2, (9,7),None)

	# combine chessboard corners and harris corners
	harris_points = {}
	chess_points = {}

	for i in corners:
		t = i
		harris_points[t[0], t[1]] = True

	for i in corners2:
		chess_points[(i[0][0], i[0][1])] = True

	dist = mindist(chess_points.keys()[0], chess_points.keys())

	final_points = {}

	for i in chess_points.keys():
		final_points[i] = True

	for i in harris_points.keys():
		if(mindist(i, chess_points.keys()) > eps and (mindist(i, chess_points.keys()) < dist * 2.5 or mindist(i, final_points.keys()) < dist * 2.5)):
			final_points[i] = True	

	points = []

	for i in final_points.keys():
		fin = (i[0], i[1], depth[(round(i[0]), round(i[1]))])
		points.append(fin) # add depth

	return points

#estimate best fit plane using scipy ODR

def f(B, x):
    ''' A*x + B*y + C = z
    B = vector of the parameters.
    x = array of the current xy values. '''
    return B[0] * x[0] + B[1] * x[1] + B[2]
    
def odr(points):
	x = []
	for i in points:
		x.append(i[0])
	y = []
	for i in points:
		y.append(i[1])
	z = []
	for i in points:
		z.append(i[2])
		
	xy = np.array([x, y])
	z = np.array(z)

	model = scipy.odr.Model(f)
	mydata = scipy.odr.Data(xy, y=z, we=None, wd=None, fix=None, meta={})
	myodr = scipy.odr.ODR(mydata, model, beta0=[1., 2., 3.])
	myoutput = myodr.run()
	
	return myoutput.beta # return found parameters 

corner_no = 80

def centroid(points): # compute centroid for point set
	sumx = 0
	sumy = 0
	sumz = 0
	for i in points:
		(x, y, z) = i
		sumx = sumx + x
		sumy = sumy + y
		sumz = sumz + z
	return (1.0 * sumx/len(points), 1.0 * sumy/len(points), 1.0 * sumz/len(points))

def find_O_normal(points, params): # find center and normal
	lin = 0
	col = 1
	lines = []
	O = centroid(points)
	point1 = np.array([points[0][0] - O[0], points[0][1] - O[1], points[0][2] - O[2]])
	point2 = np.array([points[1][0] - O[0], points[1][1] - O[1], points[1][2] - O[2]])
	normal = np.cross(point1, point2)
	normal = normal / np.linalg.norm(normal)
	return (O, normal)

def project_point(point, params): #project points on plane
	(x, y, z) = point
	(a, b, c) = params
	vector_norm = a*a + b*b + c*c
	normal_vector = np.array([a, b, c]) / np.sqrt(vector_norm)
	point_in_plane = np.array([a, b, c]) / vector_norm

	points = np.column_stack((x, y, z))
	points_from_point_in_plane = points - point_in_plane
	proj_onto_normal_vector = np.dot(points_from_point_in_plane,
                                     normal_vector)
	proj_onto_plane = (points_from_point_in_plane -
                       proj_onto_normal_vector[:, None]*normal_vector)

	ans = point_in_plane + proj_onto_plane
	return (ans[0][0], ans[0][1], ans[0][2])

points_camera1 = get_corners(filename1, depth1)
points_camera2 = get_corners(filename1, depth1)

projected_points_camera1 = []
projected_points_camera2 = []

#find odr planes for the two point sets
(x1, y1, z1) = odr(points_camera1)
(x2, y2, z2) = odr(points_camera2)

params_camera1 = (-x1, -y1, 1.0)
params_camera2 = (-x2, -y2, 1.0)

#project points on odr plane
for i in points_camera1:
	projected_points_camera1.append(project_point(i, params_camera1))
	
for i in points_camera2:
	projected_points_camera2.append(project_point(i, params_camera2))

(O1, n1) = find_O_normal(projected_points_camera1, params_camera1)
(O2, n2) = find_O_normal(projected_points_camera2, params_camera2)

theta = math.acos(np.vdot(n1, n2))
vn = np.cross(n1, n2)

q0 = math.cos(theta/2)
q1 = vn[0] * math.sin(theta/2)
q2 = vn[1] * math.sin(theta/2)
q3 = vn[2] * math.sin(theta/2)

q = (q0, q1, q2, q3)

R1 = [1 - 2 * q2 * q2 - 2 * q3 * q3, 2 * q1 * q2 + 2 * q0 * q3, 2 * q1 * q3 - 2 * q0 * q2]
R2 = [2 * q1 * q2 - 2 * q0 * q3, 1 - 2 * q1 * q1 - 2 * q3 * q3, 2 * q2 * q3 + 2 * q0 * q1]
R3 = [2 * q1 * q3 + 2 * q0 * q2, 2 * q2 * q3 - 2 * q0 * q1, 1 - 2 * q1 * q1 - 2 * q2 * q2]

R = np.array([R1, R2, R2]) # Rotation Matrix

T = O1 - np.dot(R, O1) # Translation Vector

print R, T
