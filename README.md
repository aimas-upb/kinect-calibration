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
