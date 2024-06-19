import cv2
import sys
import numpy as np

def crop_circle_hough(image, center_x, center_y, radius):
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    
    # Detect circles using Hough Circle Transform
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                               param1=50, param2=30, minRadius=0, maxRadius=0)
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        # Find the circle closest to the specified center and radius
        closest_circle = None
        min_distance = float('inf')
        
        for (x, y, r) in circles:
            distance = np.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
            if abs(distance - radius) < min_distance:
                min_distance = abs(distance - radius)
                closest_circle = (x, y, r)
        
        if closest_circle is not None:
            (x, y, r) = closest_circle
            
            # Crop the circle region from the original image
            cropped_circle = image[y - r:y + r, x - r:x + r]
            
            return cropped_circle
    
    return None

# Example usage:
if __name__ == "__main__":
    # Read an example input image (replace this with your own image path)
    input_image = cv2.imread(sys.argv[1])
    
    # Example circle parameters (center coordinates and radius)
    center_x = 444
    center_y = 1224
    radius = 80
    
    # Crop the circle using Hough Circle Transform
    cropped_circle = crop_circle_hough(input_image, center_x, center_y, radius)
    
    if cropped_circle is not None:
        # Display the cropped circle (optional, you can save it or do further processing)
        cv2.imwrite("cropped_circle1.jpg", cropped_circle)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Circle not found or could not be cropped.")