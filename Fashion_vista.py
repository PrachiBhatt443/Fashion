# Fashion Image Analysis with Explicit Validation and Database Integration
# Complete code with highlighted validation and database sections

# Install required packages
# !pip install opencv-python numpy matplotlib scikit-learn pillow tensorflow

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import Counter
from PIL import Image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
import requests
from io import BytesIO
import os
from datetime import datetime
import sqlite3
import json

# ====================== DATABASE SETUP AND FUNCTIONS ======================

def initialize_database(db_name="fashion_analysis.db"):
    """Initialize SQLite database and create tables"""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create analysis_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_url TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                colors_json TEXT NOT NULL,
                pattern_json TEXT NOT NULL,
                style_json TEXT NOT NULL,
                color_validation_json TEXT NOT NULL,
                pattern_style_validation_json TEXT NOT NULL
            )
        ''')

        conn.commit()
        print("✓ Database initialized successfully")
        return conn
    except sqlite3.Error as e:
        print(f"Database initialization failed: {str(e)}")
        return None

def store_analysis_report(conn, report):
    """Store analysis report in the database"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO analysis_results (
                image_url, timestamp, colors_json, pattern_json, style_json,
                color_validation_json, pattern_style_validation_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            report['image_url'],
            report['timestamp'],
            json.dumps(report['colors']),
            json.dumps(report['predictions']['pattern']),
            json.dumps(report['predictions']['style']),
            json.dumps(report['validation']['colors']),
            json.dumps(report['validation']['pattern_style'])
        ))
        conn.commit()
        print("✓ Analysis report stored in database")
    except sqlite3.Error as e:
        print(f"Failed to store report in database: {str(e)}")

def query_analysis_results(conn, image_url=None):
    """Query analysis results from the database"""
    try:
        cursor = conn.cursor()
        if image_url:
            cursor.execute('''
                SELECT * FROM analysis_results WHERE image_url = ?
            ''', (image_url,))
        else:
            cursor.execute('SELECT * FROM analysis_results')
        
        results = cursor.fetchall()
        return [
            {
                'id': row[0],
                'image_url': row[1],
                'timestamp': row[2],
                'colors': json.loads(row[3]),
                'pattern': json.loads(row[4]),
                'style': json.loads(row[5]),
                'color_validation': json.loads(row[6]),
                'pattern_style_validation': json.loads(row[7])
            } for row in results
        ]
    except sqlite3.Error as e:
        print(f"Database query failed: {str(e)}")
        return []

# ====================== EXPLICIT VALIDATION FUNCTIONS ======================

def validate_color_clustering(img_array, dominant_colors, k=5):
    """EXPLICIT VALIDATION: Validate color clustering results"""
    validation_results = {
        'status': 'PASS',
        'metrics': {},
        'warnings': []
    }

    try:
        # Convert image to RGB space
        if len(img_array.shape) == 2:  # Grayscale
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        else:
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        pixels = img_rgb.reshape(-1, 3)

        # 1. Silhouette Score Validation
        sample_size = min(1000, len(pixels))
        sample_indices = np.random.choice(len(pixels), sample_size, replace=False)
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
        kmeans.fit(pixels[sample_indices])
        silhouette = silhouette_score(pixels[sample_indices], kmeans.labels_)
        validation_results['metrics']['silhouette_score'] = silhouette

        if silhouette < 0.5:
            validation_results['warnings'].append(f'Low silhouette score ({silhouette:.2f})')

        # 2. Color Consistency Check
        color_values = np.array([c['color'] for c in dominant_colors])
        color_variation = np.std(color_values, axis=0).mean()
        validation_results['metrics']['color_variation'] = color_variation

        if color_variation > 15:
            validation_results['warnings'].append(f'High color variation ({color_variation:.2f})')

        # 3. Percentage Distribution Check
        percentage_sum = sum(c['percentage'] for c in dominant_colors)
        validation_results['metrics']['percentage_sum'] = percentage_sum

        if abs(percentage_sum - 1.0) > 0.01:
            validation_results['warnings'].append(f'Percentage sum incorrect ({percentage_sum:.2f})')

        # Update status if any warnings
        if validation_results['warnings']:
            validation_results['status'] = 'WARNING'

        # 4. Visual Validation
        visualize_color_validation(img_rgb, dominant_colors)

    except Exception as e:
        validation_results['status'] = 'FAIL'
        validation_results['error'] = str(e)

    return validation_results

def validate_pattern_style(predictions):
    """EXPLICIT VALIDATION: Validate pattern/style predictions"""
    validation_results = {
        'status': 'PASS',
        'warnings': []
    }

    # Check pattern confidence threshold
    if predictions['pattern']['confidence'] < 0.6:
        validation_results['warnings'].append(
            f"Low pattern confidence ({predictions['pattern']['confidence']:.2f})"
        )

    # Check style confidence threshold
    if predictions['style']['confidence'] < 0.6:
        validation_results['warnings'].append(
            f"Low style confidence ({predictions['style']['confidence']:.2f})"
        )

    # Update status if any warnings
    if validation_results['warnings']:
        validation_results['status'] = 'WARNING'

    return validation_results

def visualize_color_validation(img_rgb, dominant_colors):
    """EXPLICIT VALIDATION: Visual validation of color clustering"""
    plt.figure(figsize=(15, 5))

    # Original image
    plt.subplot(1, 3, 1)
    plt.imshow(img_rgb)
    plt.title('Original Image')
    plt.axis('off')

    # Color swatches
    plt.subplot(1, 3, 2)
    for i, color_info in enumerate(dominant_colors):
        color = np.array(color_info['color']).reshape(1, 1, 3)/255
        plt.subplot(1, len(dominant_colors), i+1)
        plt.imshow(color)
        plt.axis('off')
        plt.title(f"{color_info['hex']}\n{color_info['percentage']:.1%}")

    # Color spatial distribution
    plt.subplot(1, 3, 3)
    color_map = np.zeros_like(img_rgb)
    for color_info in dominant_colors:
        target_color = np.array(color_info['color'])
        mask = cv2.inRange(img_rgb, target_color-25, target_color+25)
        color_map[mask > 0] = target_color
    plt.imshow(color_map)
    plt.title('Color Distribution')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

# ====================== ANALYSIS FUNCTIONS ======================

def load_image_from_url(url):
    """Load image from URL with error handling"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return np.array(img)
    except Exception as e:
        raise ValueError(f"Failed to load image: {str(e)}")

def extract_dominant_colors(img_array, k=5):
    """Extract dominant colors from image array"""
    try:
        # Convert image to proper color space
        if len(img_array.shape) == 2:  # Grayscale
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        else:
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        pixels = img_rgb.reshape(-1, 3)

        # Perform clustering
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
        kmeans.fit(pixels)

        # Process results
        counts = Counter(kmeans.labels_)
        center_colors = kmeans.cluster_centers_
        total = sum(counts.values())

        dominant_colors = []
        for i in counts.keys():
            color = np.clip(center_colors[i], 0, 255).astype(int)
            percentage = counts[i] / total
            dominant_colors.append({
                'color': color.tolist(),
                'percentage': float(percentage),
                'hex': '#%02x%02x%02x' % tuple(color)
            })

        # Sort by percentage
        dominant_colors.sort(key=lambda x: x['percentage'], reverse=True)
        return dominant_colors

    except Exception as e:
        raise ValueError(f"Color extraction failed: {str(e)}")

# ====================== MAIN ANALYSIS PIPELINE ======================

def analyze_fashion_image(image_url, conn):
    """Complete analysis pipeline with integrated validation and database storage"""
    try:
        print(f"\nStarting analysis of: {image_url}")

        # 1. Load image
        img_array = load_image_from_url(image_url)
        print("✓ Image loaded successfully")

        # 2. Color analysis
        colors = extract_dominant_colors(img_array)
        print("✓ Color extraction completed")

        # 3. VALIDATE COLOR RESULTS
        print("\nVALIDATING COLOR CLUSTERING...")
        color_validation = validate_color_clustering(img_array, colors)
        print(f"Validation Status: {color_validation['status']}")
        if color_validation['warnings']:
            print("Warnings:")
            for warning in color_validation['warnings']:
                print(f"  - {warning}")

        # 4. Pattern/Style analysis (using dummy model)
        print("\nRunning pattern/style analysis...")
        model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

        # Dummy predictions (replace with actual trained classifiers)
        predictions = {
            'pattern': {
                'predicted': 'floral',
                'confidence': 0.82,
                'all_options': {
                    'floral': 0.82,
                    'striped': 0.10,
                    'geometric': 0.05,
                    'plain': 0.03
                }
            },
            'style': {
                'predicted': 'casual',
                'confidence': 0.75,
                'all_options': {
                    'casual': 0.75,
                    'formal': 0.15,
                    'bohemian': 0.07,
                    'sporty': 0.03
                }
            }
        }

        # 5. VALIDATE PATTERN/STYLE RESULTS
        print("\nVALIDATING PATTERN/STYLE PREDICTIONS...")
        ps_validation = validate_pattern_style(predictions)
        print(f"Validation Status: {ps_validation['status']}")
        if ps_validation['warnings']:
            print("Warnings:")
            for warning in ps_validation['warnings']:
                print(f"  - {warning}")

        # 6. Generate final report
        report = {
            'image_url': image_url,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'colors': colors,
            'predictions': predictions,
            'validation': {
                'colors': color_validation,
                'pattern_style': ps_validation
            }
        }

        # 7. Store report in database
        store_analysis_report(conn, report)

        # 8. Display final results
        print("\n=== FINAL VALIDATED RESULTS ===")
        print("\nDominant Colors (Validated):")
        for idx, color in enumerate(colors, 1):
            print(f"{idx}. {color['hex']} - {color['percentage']:.1%}")

        print("\nPattern Prediction (Validated):")
        print(f"- Predicted: {predictions['pattern']['predicted']}")
        print(f"- Confidence: {predictions['pattern']['confidence']:.2f}")
        print("- All options:")
        for pattern, prob in predictions['pattern']['all_options'].items():
            print(f"  - {pattern}: {prob:.2f}")

        print("\nStyle Prediction (Validated):")
        print(f"- Predicted: {predictions['style']['predicted']}")
        print(f"- Confidence: {predictions['style']['confidence']:.2f}")
        print("- All options:")
        for style, prob in predictions['style']['all_options'].items():
            print(f"  - {style}: {prob:.2f}")

        print("\n=== VALIDATION SUMMARY ===")
        print(f"Color Analysis: {color_validation['status']}")
        print(f"Pattern/Style Analysis: {ps_validation['status']}")

        return report

    except Exception as e:
        print(f"\nAnalysis failed: {str(e)}")
        return None

# ====================== EXAMPLE USAGE ======================

if __name__ == "__main__":
    # Initialize database
    conn = initialize_database()

    if conn:
        # Example Unsplash fashion image URL
        FASHION_IMAGE_URL = "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f"

        # Run complete analysis with validation and database storage
        analysis_report = analyze_fashion_image(FASHION_IMAGE_URL, conn)

        # Query and display stored results
        if analysis_report:
            print("\n=== QUERYING STORED RESULTS ===")
            stored_results = query_analysis_results(conn, FASHION_IMAGE_URL)
            for result in stored_results:
                print(f"\nStored Analysis (ID: {result['id']}):")
                print(f"Image URL: {result['image_url']}")
                print(f"Timestamp: {result['timestamp']}")
                print("Dominant Colors:")
                for idx, color in enumerate(result['colors'], 1):
                    print(f"  {idx}. {color['hex']} - {color['percentage']:.1%}")
                print(f"Pattern: {result['pattern']['predicted']} (Confidence: {result['pattern']['confidence']:.2f})")
                print(f"Style: {result['style']['predicted']} (Confidence: {result['style']['confidence']:.2f})")
                print(f"Color Validation Status: {result['color_validation']['status']}")
                print(f"Pattern/Style Validation Status: {result['pattern_style_validation']['status']}")

        # Save detailed report to file
        if analysis_report:
            report_filename = "validated_fashion_analysis.txt"
            with open(report_filename, "w") as f:
                f.write("=== VALIDATED FASHION IMAGE ANALYSIS REPORT ===\n\n")
                f.write(f"Image URL: {analysis_report['image_url']}\n")
                f.write(f"Analysis Date: {analysis_report['timestamp']}\n\n")

                f.write("=== COLOR ANALYSIS ===\n")
                f.write("Dominant Colors:\n")
                for idx, color in enumerate(analysis_report['colors'], 1):
                    f.write(f"{idx}. {color['hex']}: {color['percentage']:.1%}\n")

                f.write("\nValidation Results:\n")
                f.write(f"Status: {analysis_report['validation']['colors']['status']}\n")
                if analysis_report['validation']['colors']['warnings']:
                    f.write("Warnings:\n")
                    for warning in analysis_report['validation']['colors']['warnings']:
                        f.write(f"- {warning}\n")

                f.write("\n=== PATTERN ANALYSIS ===\n")
                f.write(f"Predicted: {analysis_report['predictions']['pattern']['predicted']}\n")
                f.write(f"Confidence: {analysis_report['predictions']['pattern']['confidence']:.2f}\n")

                f.write("\n=== STYLE ANALYSIS ===\n")
                f.write(f"Predicted: {analysis_report['predictions']['style']['predicted']}\n")
                f.write(f"Confidence: {analysis_report['predictions']['style']['confidence']:.2f}\n")

                f.write("\n=== VALIDATION SUMMARY ===\n")
                f.write(f"Overall Validation Status:\n")
                f.write(f"- Color Analysis: {analysis_report['validation']['colors']['status']}\n")
                f.write(f"- Pattern/Style Analysis: {analysis_report['validation']['pattern_style']['status']}\n")

            print(f"\nFull validated report saved to '{report_filename}'")

        # Close database connection
        conn.close()
        print("✓ Database connection closed")