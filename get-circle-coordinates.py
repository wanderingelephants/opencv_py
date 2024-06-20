import cv2
import sys
import numpy as np

def mark_circle():
    # Read image. 
    img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR) 
  
    # Convert to grayscale. 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (3, 3)) 
    
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                param2 = 30, minRadius = 75, maxRadius = 82) 
    
    # Draw circles that are detected. 
    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
        i = 0
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
    
            # Draw the circumference of the circle. 
            cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
    
            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 
            #cv2.imshow("Detected Circle", img) 
            filename = sys.argv[1].split(".")
            cv2.imwrite(filename[0]+"-green."+filename[1],img)
            cv2.waitKey(0) 

            # Return circle boundary

            #crop_circle("yokohama-"+str(i)+".jpg",(a,b,r))
            crop_circle(sys.argv[1],(a,b,r),i)
            i = i + 1
#            return (a,b,r)

def crop_circle(image_path, circle, index):
    print("Going to crop:",circle[0],circle[1],circle[2])
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

    # Create a circular mask
    mask = np.zeros(cropped_quadrant.shape[:2], dtype=np.uint8)
    center = (cropped_quadrant.shape[1] // 2, cropped_quadrant.shape[0] // 2)
    #radius = min(center)
    # cv2.circle(mask, center, radius, (255, 255, 255), -1)
    cv2.circle(mask, center, circle[2], (255, 255, 255), -1)

    # Apply the mask to the cropped image
    cropped_circle = cv2.bitwise_and(cropped_quadrant, cropped_quadrant, mask=mask)

    # Display the cropped circle (optional)
#    cv2.imshow("Cropped Circle", cropped_circle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the cropped circle to a file (optional)
    cv2.imwrite("yokohama-"+str(index)+".jpg", cropped_circle)

# Call the function to crop the circle within the cropped quadrant

#circle = mark_circle()

#crop_circle(sys.argv[1], circle)

mark_circle()

