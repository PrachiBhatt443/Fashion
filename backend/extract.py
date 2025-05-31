import os
import cv2
import numpy as np
from colorthief import ColorThief
import webcolors

def apply_graph_cut(image_path):
    """Apply Graph Cut to segment cloth area."""
    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error loading image {image_path}")
        return None
    
    # Resize image for faster processing (optional)
    image = cv2.resize(image, (500, 500))
    
    # Prepare mask for grabCut
    mask = np.zeros(image.shape[:2], np.uint8)
    
    # Initialize background and foreground models
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # Apply grabCut algorithm
    rect = (10, 10, image.shape[1] - 10, image.shape[0] - 10)  # Define the rectangle covering most of the image
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

    # Modify mask to separate background and foreground
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    segmented_image = image * mask2[:, :, np.newaxis]
    
    return segmented_image

def closest_color(requested_color):
    """
    Finds the closest color name for the given RGB value.
    
    Args:
    requested_color (tuple): RGB color tuple.
    
    Returns:
    str: Name of the closest color.
    """
    min_colors = {}
    for name in webcolors.names("css3"):
        r_c, g_c, b_c = webcolors.name_to_rgb(name)
        distance = ((r_c - requested_color[0]) ** 2 +
                    (g_c - requested_color[1]) ** 2 +
                    (b_c - requested_color[2]) ** 2)
        min_colors[distance] = name
    return min_colors[min(min_colors.keys())]

def extract_dominant_color(image):
    """Use ColorThief to extract the dominant color."""
    # Convert the image to RGB and save temporarily for ColorThief
    temp_path = 'temp_image.jpg'
    cv2.imwrite(temp_path, image)
    
    # Use ColorThief to get the dominant color and palette
    color_thief = ColorThief(temp_path)
    dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=6)
    
    # Exclude black from the palette
    filtered_palette = [color for color in palette if color != (0, 0, 0)]
    
    return dominant_color, filtered_palette

def process_images_in_folder(folder_path):
    """Process all images in the specified folder."""
    color_summary = {}
    dataset_palette = []

    for image_name in os.listdir(folder_path):
        if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, image_name)
            
            # Load the image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image {image_name}")
                continue
            
            # Step 1: Extract dominant color and palette
            dominant_color, palette = extract_dominant_color(image)
            
            # Convert RGB colors to human-readable names
            dominant_color_name = closest_color(dominant_color)
            palette_names = [closest_color(color) for color in palette[:3]]  # Take top 3 non-black colors
            
            # Add the palette to the dataset-wide collection
            dataset_palette.extend(palette)
            
            # Store results
            color_summary[image_name] = {
                'dominant_color_name': dominant_color_name,
                'palette_names': palette_names
            }
    
    # Compute the top 3 colors across the whole dataset
    all_colors = [color for color in dataset_palette if color != (0, 0, 0)]
    top_colors = sorted(set(all_colors), key=all_colors.count, reverse=True)[:3]
    top_color_names = [closest_color(color) for color in top_colors]
    
    return color_summary, top_color_names

# Path to the folder containing images
folder_path = 'datasets'

# Process the images and get the dominant colors
color_summary, dataset_top_colors = process_images_in_folder(folder_path)

# Print the results for each image
for image_name, colors in color_summary.items():
    print(f"{image_name}: Dominant Color: {colors['dominant_color_name']}, Top 3 Colors: {colors['palette_names']}")

# Print the top 3 colors across the whole dataset
print(f"Top 3 Colors across the dataset: {dataset_top_colors}")
def get_color_data(folder_path):
    color_summary, dataset_top_colors = process_images_in_folder(folder_path)
    return {
        "color_summary": color_summary,
        "dataset_top_colors": dataset_top_colors
    }
