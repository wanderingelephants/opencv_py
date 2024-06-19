import sys
from PIL import Image, ImageDraw

def crop_circle_pieslice(image_path, center_x, center_y, radius):
    # Load the image
    img = Image.open(image_path)
    
    # Create a mask image with alpha channel
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw a filled white circle on the mask
    draw.pieslice([(center_x - radius, center_y - radius),
                   (center_x + radius, center_y + radius)],
                   0, 360, fill=255)
    
    # Apply the mask to the image
    img.putalpha(mask)
    
    # Crop the circular region
    cropped_image = img.crop((center_x - radius, center_y - radius,
                              center_x + radius, center_y + radius))
    
    return cropped_image

# Example usage:
if __name__ == "__main__":
    # Example input image path
    image_path = sys.argv[1]
    
    # Example circle parameters (center coordinates and radius)
    center_x = 444
    center_y = 1224
    radius = 81
    
    # Crop the circular image using pieslice method
    cropped_image = crop_circle_pieslice(image_path, center_x, center_y, radius)
    
    # Display the cropped image (optional, you can save it or do further processing)
    #cropped_image.show()
    
    # Save the cropped image (optional)
    path = image_path.split(".")
    cropped_image.save(path[1]+"1."+path[1])