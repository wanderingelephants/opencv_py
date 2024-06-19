import cv2
import numpy as np
import sys

def crop_circle(center_x, center_y, radius, input_image):
    # Create a black image as a mask
    mask = np.zeros_like(input_image)

    # Draw a filled white circle on the mask
    cv2.circle(mask, (center_x, center_y), radius, (255, 255, 255), -1)

    # Bitwise AND operation to extract the region inside the circle
    masked_image = cv2.bitwise_and(input_image, mask)

    # Find contours in the mask (this is optional, just for visualizing)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the bounding box of the circle (optional)
    x, y, w, h = cv2.boundingRect(contours[0])

    # Crop the circle region from the input image
    cropped_circle = masked_image[y:y+h, x:x+w]

    return cropped_circle

# Example usage:
if __name__ == "__main__":
    # Read an example input image (replace this with your own image path)
    input_image = cv2.imread(sys.argv[1])

    # Example circle parameters (center coordinates and radius)
    center_x = 850
    center_y = 1494
    radius = 81

    # Crop the circle from the input image
    cropped_circle = crop_circle(center_x, center_y, radius, input_image)

    # Display the cropped circle (optional, you can save it or do further processing)
    #cv2.imshow('Cropped Circle', cropped_circle)
    cv2.imwrite("cropped_circle0.jpg", cropped_circle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()