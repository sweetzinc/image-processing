import numpy as np

def analyze_grayscale_image(image):
    """
    Analyze a grayscale image to compute its histogram and optimal threshold.
    
    Args:
        image (numpy.ndarray): Input grayscale image (uint8, values 0-255)
        
    Returns:
        tuple: (histogram, threshold)
            - histogram: array of size 256 containing pixel counts for each intensity
            - threshold: optimal threshold value using Otsu's method
    """
    # Input validation
    if image.dtype != np.uint8:
        raise ValueError("Image must be uint8")
    
    # Calculate histogram
    histogram = np.zeros(256, dtype=np.int32)
    for i in range(256):
        histogram[i] = np.sum(image == i)
    
    # Otsu's method for threshold calculation
    total_pixels = image.size
    pixel_range = np.arange(256)
    
    # Compute cumulative sums
    cumsum = histogram.cumsum()
    cumsum_vals = (pixel_range * histogram).cumsum()
    
    # Avoid division by zero
    mask = (cumsum != 0) & (cumsum != total_pixels)
    
    # Calculate between-class variance
    w1 = cumsum[:-1]
    w2 = total_pixels - w1
    mu1 = cumsum_vals[:-1] / w1
    mu2 = (cumsum_vals[-1] - cumsum_vals[:-1]) / w2
    
    # Calculate variance
    variance = w1 * w2 * (mu1 - mu2) ** 2
    
    # Find threshold that maximizes variance
    threshold = np.argmax(variance)
    
    return histogram, threshold

#%%
from PIL import Image
import numpy as np

# Example usage
# Read image and convert to grayscale
image = Image.open('your_image.png').convert('L')
# Convert to numpy array for processing
image_array = np.array(image)

histogram, threshold = analyze_grayscale_image(image_array)

# Visualize results
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 4))

# Plot histogram
plt.subplot(121)
plt.plot(histogram)
plt.title('Grayscale Histogram')
plt.xlabel('Intensity')
plt.ylabel('Pixel Count')

# Plot binarized image
plt.subplot(122)
binary_image = (image_array > threshold).astype(np.uint8) * 255
plt.imshow(binary_image, cmap='gray')
plt.title(f'Binarized Image (threshold={threshold})')
plt.show()

# If you want to save the binary image:
binary_pil = Image.fromarray(binary_image)
binary_pil.save('binary_output.png')