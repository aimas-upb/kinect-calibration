# kinect-calibration
Calibration of multiple Kinect cameras to obtain a single positioning coordinate system in a laboratory room.

# demo

- Align Depth and RGB image using the MapDepthFrameToColorFrame() method available for Kinect Windows SDK and save depth mappings in a csv file.

< pictures of normal vs aligned frames> 

- Extract checkerboard corners using a combination of the results obtained by the cornerHarris and findChessboardCorners detectors (available in OpenCV 2).

< picture of extracted corners>

- Find best fit plane using Orthogonal Distance Regression (available in scipy.odr)

- Project checkerboard points onto best fit plane.

- Extract origin and normal of the plane.

< picture of origin and normal>

- Compute rotation matrix and translation vector (math)

- Extract the cameras' coordinate systems and apply transformations.

# reference

- Rizwan Macknojia, Alberto Chávez-Aragón and Pierre Payeur, Robert Laganière, "Calibration of a Network of Kinect Sensors for Robotic Inspection over a Large Workspace"

- P. T. Boggs and J. E. Rogers, “Orthogonal Distance Regression,” in “Statistical analysis of measurement error models and applications: proceedings of the AMS-IMS-SIAM joint summer research conference held June 10-16, 1989,” Contemporary Mathematics, vol. 112, pg. 186, 1990.

- Z. Zhang, "Camera Calibration: a Personal Retrospective"
