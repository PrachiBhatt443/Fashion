# from tensorflow.keras.applications import InceptionV3
# from tensorflow.keras.applications.inception_v3 import preprocess_input
# from tensorflow.keras.preprocessing.image import img_to_array, load_img
# import numpy as np
# from sklearn.cluster import KMeans
import os

# # Load pre-trained model
# base_model = InceptionV3(weights='imagenet', include_top=False, pooling='avg')  # Global feature extraction

# # Path to dataset
dataset_path = 'datasets'
# image_features = []

# # Loop through all images and extract features
# for image_name in os.listdir(dataset_path):
#     image_path = os.path.join(dataset_path, image_name)
#     image = load_img(image_path, target_size=(224, 224))  # Resize to 224x224
#     image_array = img_to_array(image)
#     image_array = preprocess_input(image_array)  # Preprocess for InceptionV3
#     image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

#     # Extract features
#     features = base_model.predict(image_array)
#     image_features.append(features.flatten())  # Flatten the feature vector

# # Convert to NumPy array
# image_features = np.array(image_features)

# # Cluster the images into patterns (e.g., striped, checked, etc.)
# kmeans = KMeans(n_clusters=5, random_state=42)  # Adjust the number of clusters
# kmeans.fit(image_features)

# # Get cluster labels
# cluster_labels = kmeans.labels_

# # Display cluster assignments
# for i, image_name in enumerate(os.listdir(dataset_path)):
#     print(f"Image: {image_name}, Cluster: {cluster_labels[i]}")
from google.cloud import vision

client = vision.ImageAnnotatorClient()

# Analyze each image
for image_name in os.listdir(dataset_path):
    image_path = os.path.join(dataset_path, image_name)
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print(f"Image: {image_name}, Labels: {[label.description for label in labels]}")
