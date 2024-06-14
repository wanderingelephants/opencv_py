import cv2
import numpy as np

def crop_largest_circle(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Get the dimensions of the image
    height, width = image.shape[:2]

    # Define the coordinates for the 4th quadrant (bottom-right quadrant)
    x_start = width // 2
    y_start = height // 2
    x_end = width
    y_end = height

    # Crop the 4th quadrant
    cropped_quadrant = image[y_start:y_end, x_start:x_end]

    # Convert the cropped image to grayscale
    gray = cv2.cvtColor(cropped_quadrant, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Hough Circle Transform
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=0, maxRadius=100)

    # If circles are found
    if circles is not None:
        # Convert the coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # Find the largest circle
        largest_circle = max(circles, key=lambda circle: circle[2])

        # Extract the coordinates and radius of the largest circle
        (x, y, r) = largest_circle

        # Crop the circular region
        cropped_circle = cropped_quadrant[y - r:y + r, x - r:x + r]

        # Display the cropped circle (optional)
#        cv2.imshow("Cropped Circle", cropped_circle)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Save the cropped circle to a file (optional)
        cv2.imwrite("cropped_circle3.jpg", cropped_circle)
    else:
        print("No circular figure found in the cropped quadrant.")

# Path to the input image file
image_path = "cropped_quadrant.jpg"

# Call the function to find and crop the largest circular figure within the cropped quadrant
crop_largest_circle(image_path)