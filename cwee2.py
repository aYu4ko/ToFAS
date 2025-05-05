import cv2
import numpy as np

def load_and_display_image(image_path):
    # Load the image
    # cv2.imread returns a NumPy array in BGR format (not RGB)
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Could not load image from {image_path}")
        return None
    
    print(f"Image loaded successfully!")
    print(f"Image dimensions: {img.shape}")  # (height, width, channels)
    
    # Display using OpenCV (BGR format)
    cv2.imshow("Image", img)
    cv2.waitKey(0)  # Wait for any key press
    cv2.destroyAllWindows()  # Close the window
    
    return img

def save_image(img, output_path):
    """
    Save an image to a file
    
    Parameters:
    img (numpy.ndarray): Image to save
    output_path (str): Path where to save the image
    
    Returns:
    bool: True if successful, False otherwise
    """
    result = cv2.imwrite(output_path, img)
    if result:
        print(f"Image saved successfully to {output_path}")
    else:
        print(f"Error: Could not save image to {output_path}")
    return result

def main():
    # Example usage
    image_path = "C:\YAD\YADP\Python\\tof\images\ss1223432.png"  # Change this to your image path
    
    # Load and display the image
    img = load_and_display_image(image_path)
    
    if img is not None:
        # Example: Create and display a grayscale version
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Display grayscale image
        cv2.imshow("Grayscale Image", img_gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Save the grayscale image
        save_image(img_gray, "grayscale_output.jpg")

if __name__ == "__main__":
    main()