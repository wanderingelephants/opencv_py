import cv2
import sys

def crop_4th_quadrant(image_path):
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

    # Display the cropped quadrant (optional)
#    cv2.imshow("Cropped 4th Quadrant", cropped_quadrant)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the cropped quadrant to a file (optional)
    cv2.imwrite("cropped_quadrant.jpg", cropped_quadrant)
    exit()     
    
# Path to the input image file
#image_path = "Yokohama.jpg"
image_path = sys.argv[0]
print('process img', image_path)


# Call the function to crop the 4th quadrant
crop_4th_quadrant(image_path)
