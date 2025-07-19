# utils/visualize.py
import numpy as np
import cv2

def overlay_lidar_on_image(lidar_path, img_path, calib_path):
    # Load calibration data
    with open(calib_path) as f:
        calib = dict(line.split() for line in f.read().splitlines())
    
    # Load LiDAR and image
    points = np.fromfile(lidar_path, dtype=np.float32).reshape(-1, 4)
    img = cv2.imread(img_path)
    
    # Transform LiDAR→Camera (using calib_velo_to_cam.txt)
    # [Implementation depends on your calibration format]
    # ...
    
    # Project points onto image
    for x, y, z, _ in points:
        u, v = project_3d_to_2d(x, y, z, calib)
        cv2.circle(img, (int(u), int(v)), 2, (0, 255, 0), -1)
    
    cv2.imshow("LiDAR-Image Overlay", img)
    cv2.waitKey(0)