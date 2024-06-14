import cv2

def crop_fourth_quadrant(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Get the dimensions of the image
    height, width, _ = image.shape
    
    # Define the region of interest (ROI) for the fourth quadrant
    start_row = height // 2
    end_row = height
    start_col = width // 2
    end_col = width
    
    # Crop the fourth quadrant
    cropped_image = image[start_row:end_row, start_col:end_col]
    
    # Save the cropped image
    cv2.imwrite(output_path, cropped_image)
    
    print("Cropped image saved successfully!")

# Input image file path
input_image_path = "input_image.jpg"

# Output image file path
output_image_path = "cropped_image.jpg"

# Call the function to crop the fourth quadrant
crop_fourth_quadrant(input_image_path, output_image_path)