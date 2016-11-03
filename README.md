# kinect-calibration
Calibration of multiple Kinect cameras to obtain a single positioning coordinate system in a laboratory room.

# demo

- Align Depth and RGB image using the MapDepthFrameToColorFrame() method available for Kinect Windows SDK and save depth mappings in a csv file.

- Extract checkerboard corners using a combination of the results obtained by the cornerHarris and findChessboardCorners detectors (available in OpenCV 2).

![alt tag](https://github.com/paula-gradu/kinect-calibration/blob/master/Screenshot%20from%202016-11-01%2013:13:30.png)

- Find best fit plane using Orthogonal Distance Regression (available in scipy.odr)

- Project checkerboard points onto best fit plane.

- Extract origin and normal of the plane.

- Compute rotation matrix and translation vector.

- Extract the cameras' coordinate systems and apply transformations (always from one camera to the other).

R = [[  9.83507715e-01   8.26415576e-03  -1.31342591e-04]
     [ -8.26302378e-03   9.83506358e-01  -1.38576655e-04]
     [ -8.26302378e-03   9.83506358e-01  -1.38576655e-04]] 
     
T = [  5.87812299e-01   6.94506028e+00   1.70568353e+03]

- Images used for calibration:
![alt tag](https://github.com/paula-gradu/kinect-calibration/blob/master/rgb1_1.jpg = 320x240)
![alt tag](https://github.com/paula-gradu/kinect-calibration/blob/master/rgb1.jpg = 320x240)

- Difference between camera frames in cm and degrees:

dx = 120 cm, dy = 21 cm, dz = -5 cm
ux = 125°, uy = 20°, uz = 85°

# reference

- Rizwan Macknojia, Alberto Chávez-Aragón and Pierre Payeur, Robert Laganière, "Calibration of a Network of Kinect Sensors for Robotic Inspection over a Large Workspace"

- P. T. Boggs and J. E. Rogers, “Orthogonal Distance Regression,” in “Statistical analysis of measurement error models and applications: proceedings of the AMS-IMS-SIAM joint summer research conference held June 10-16, 1989,” Contemporary Mathematics, vol. 112, pg. 186, 1990.

- Microsoft Research, "Zhang's Camera Calibration"
