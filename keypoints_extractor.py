import cv2
import numpy as np

def extract_road_centerline(image_path, step=30):
    """Extract points from black road on white background"""
    # Read image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours (road edges)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return []
    
    # Approximate centerline
    largest_contour = max(contours, key=cv2.contourArea)
    points = []
    
    # Sample points along the contour
    for i in range(0, len(largest_contour), step):
        x, y = largest_contour[i][0]
        points.append((x, y))
    
    return points

# Usage
road_points = extract_road_centerline("road_map.png")
road_points2=extract_road_centerline("road_map.png")
print(f"Extracted {len(road_points)} points:")
#print(road_points[:10])  # Print first 10 points
if road_points==road_points2:
    print(True)
else:
    print(False)