import cv2
import sys

def crop_first_quadrant(image_path): 
        # Load the image 
        image = cv2.imread(image_path)

        # Get image dimensions
        height, width, _ = image.shape

        # Define the coordinates for cropping
#        start_row = height // 2
#        end_row = height
        start_row = 0
        end_row = height // 2
        start_col = 0
        end_col = width // 2

        # Crop the image
        # cropped_image = image[start_y:height, start_x:width]
        cropped_image = image[start_row:end_row, start_col:end_col]

        # Display the cropped image
        #cv2.imshow("Cropped Image", cropped_image)
        file_name = image_path.split(".")
        cv2.imwrite(file_name[0]+"-first."+file_name[1], cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Specify the path to the input image
input_image_path = sys.argv[1]

# Call the function to crop the fourth quadrant
crop_first_quadrant(input_image_path)
