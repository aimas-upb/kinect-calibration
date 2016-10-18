1. Align Depth and RGB image using the MapDepthFrameToColorFrame() method available for Kinect Windows SDK and save depth mappings in a csv file.

<insert pictures of normal vs aligned frames> 

2. Extract checkerboard corners using a combination of the results obtained by the cornerHarris and findChessboardCorners detectors (available in OpenCV 2).

<insert picture of extracted corners>

3. Find best fit plane using Orthogonal Distance Regression (available in scipy.odr)

4. Project checkerboard points onto best fit plane.

5. Extract origin and normal of the plane.

<insert picture of origin and normal>

6. Compute rotation matrix and translation vector (math)

7. Extract the cameras' coordinate systems and apply transformations.
