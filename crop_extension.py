import os, sys
from PIL import Image 
import random
from typing import Tuple

def random_crop_containing_bbox(image, bbox: Tuple[int, int, int, int], crop_size=(512, 512)):
    """
    Randomly crops an image such that the bounding box is fully contained within the crop.
    
    Args:
        image: PIL Image object
        bbox: Tuple of (x, y, width, height) defining the bounding box
        crop_size: Tuple of (width, height) for the desired crop size
        
    Returns:
        PIL Image object containing the cropped image
        
    Raises:
        ValueError: If the bounding box is outside image bounds or crop size is invalid
    """
    if image is None:
        raise ValueError("Image cannot be None")
        
    if not isinstance(crop_size, tuple) or len(crop_size) != 2:
        raise ValueError("crop_size must be a tuple of length 2")
        
    if crop_size[0] <= 0 or crop_size[1] <= 0:
        raise ValueError("crop_size dimensions must be positive")
    
    width, height = image.size
    
    # Convert bbox from [x,y,w,h] to [x1,y1,x2,y2]
    x, y, w, h = bbox
    bbox_x1, bbox_y1, bbox_x2, bbox_y2 = x, y, x + w, y + h

    # Ensure the bounding box is within the image dimensions
    if (bbox_x1 < 0 or bbox_y1 < 0 or bbox_x2 > width or bbox_y2 > height):
        raise ValueError("Bounding box is out of image bounds")
        
    # Ensure crop size is large enough to contain bbox
    if w > crop_size[0] or h > crop_size[1]:
        raise ValueError("Crop size is smaller than bounding box")

    # Calculate valid range for crop's top-left corner
    min_x = max(0, bbox_x2 - crop_size[0])
    max_x = min(width - crop_size[0], bbox_x1)
    min_y = max(0, bbox_y2 - crop_size[1])
    max_y = min(height - crop_size[1], bbox_y1)

    # Check if valid crop region exists
    if min_x > max_x or min_y > max_y:
        raise ValueError("No valid crop region exists that contains the bounding box")

    # Randomly select a top-left corner for the crop
    x = random.randint(min_x, max_x) if min_x < max_x else min_x
    y = random.randint(min_y, max_y) if min_y < max_y else min_y

    # Crop the image
    cropped_image = image.crop((x, y, x + crop_size[0], y + crop_size[1]))

    return cropped_image, (x, y)


def crop_to_grid(image, tile_size=(512, 512)):
    """
    Crops an image into a grid of specified size. 
    Zero-pad the image if necessary to make it divisible by the grid size.
    """
    width, height = image.size
    tile_width, tile_height = tile_size

    # Calculate the number of crops needed in each dimension
    num_crops_x = (width + tile_width - 1) // tile_width
    num_crops_y = (height + tile_height - 1) // tile_height

    # Create a list to store the cropped images
    crops = []

    # Crop the image into a grid
    for i in range(num_crops_x):
        for j in range(num_crops_y):
            left = i * tile_width
            upper = j * tile_height
            right = min(left + tile_width, width)
            lower = min(upper + tile_height, height)

            # Crop the image
            crop = image.crop((left, upper, right, lower))

            # If the crop is smaller than the grid size, pad it with zeros
            if crop.size != (tile_width, tile_height):
                padded_crop = Image.new("RGB", (tile_width, tile_height))
                padded_crop.paste(crop, (0, 0))
                crops.append(padded_crop)
            else:
                crops.append(crop)

    return crops


def crop_to_grid_with_offset(image, tile_size=(512, 512), offset=(256, 256)):
    """
    Crops an image into a grid of specified size with an offset. 
    Pass for the remaining pixels if the image is not divisible by the grid size.
    """
    width, height = image.size
    tile_width, tile_height = tile_size
    offset_x, offset_y = offset

    # Calculate the number of crops needed in each dimension
    num_crops_x = (width - offset_x - 1) // tile_width
    num_crops_y = (height- offset_y- 1) // tile_height

    # Create a list to store the cropped images
    crops = []
    # Crop the image into a grid
    for i in range(num_crops_x):
        for j in range(num_crops_y):
            left = i * tile_width
            upper = j * tile_height
            right = min(left + tile_width, width)
            lower = min(upper + tile_height, height)

            # Crop the image
            crop = image.crop((left, upper, right, lower))
            crops.append(crop)
    return crops



