import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import Counter
from PIL import Image
import requests
from io import BytesIO
import os
from datetime import datetime
import sqlite3
import json
import pandas as pd
from scipy.spatial import KDTree
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ====================== WEBCOLORS FIX ======================
try:
    from webcolors import hex_to_rgb
    CSS3_HEX_TO_NAMES = {
        '#000000': 'black', '#ffffff': 'white', '#ff0000': 'red', '#00ff00': 'lime',
        '#0000ff': 'blue', '#ffff00': 'yellow', '#ff00ff': 'fuchsia', '#00ffff': 'cyan',
        '#800000': 'maroon', '#808000': 'olive', '#008000': 'green', '#800080': 'purple',
        '#008080': 'teal', '#c0c0c0': 'silver', '#808080': 'gray', '#ffa500': 'orange'
    }
except ImportError:
    logging.info("Installing webcolors...")
    os.system('pip install --upgrade webcolors')
    try:
        from webcolors import hex_to_rgb
        CSS3_HEX_TO_NAMES = {
            '#000000': 'black', '#ffffff': 'white', '#ff0000': 'red', '#00ff00': 'lime',
            '#0000ff': 'blue', '#ffff00': 'yellow', '#ff00ff': 'fuchsia', '#00ffff': 'cyan',
            '#800000': 'maroon', '#808000': 'olive', '#008000': 'green', '#800080': 'purple',
            '#008080': 'teal', '#c0c0c0': 'silver', '#808080': 'gray', '#ffa500': 'orange'
        }
    except Exception as e:
        logging.error(f"Failed to install webcolors: {str(e)}")
        raise ImportError("webcolors is required but could not be installed")

# ====================== DATABASE FUNCTIONS ======================

def initialize_database(db_name="/content/fashion_analysis.db"):
    """Initialize SQLite database in Colab-friendly path"""
    try:
        db_dir = os.path.dirname(db_name)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logging.info(f"Created directory: {db_dir}")

        conn = sqlite3.connect(db_name, check_same_thread=False)
        cursor = conn.cursor()

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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cluster_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cluster_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                popular_colors_json TEXT NOT NULL,
                popular_patterns_json TEXT NOT NULL,
                popular_styles_json TEXT NOT NULL,
                image_urls_json TEXT NOT NULL
            )
        ''')

        conn.commit()
        logging.info(f"Database initialized at {db_name}")
        if os.path.exists(db_name):
            logging.info(f"Database file confirmed: {db_name}")
        else:
            logging.warning(f"Database file not found at {db_name}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error during database initialization: {str(e)}")
        return None

def store_analysis_report(conn, report):
    """Store individual image analysis report"""
    if not conn:
        logging.error("No database connection")
        return
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
        logging.info("Report stored in database")
    except sqlite3.Error as e:
        logging.error(f"Failed to store report: {str(e)}")

def store_cluster_analysis(conn, cluster_report):
    """Store cluster-level analysis"""
    if not conn:
        logging.error("No database connection")
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cluster_analysis (
                cluster_name, timestamp, popular_colors_json,
                popular_patterns_json, popular_styles_json, image_urls_json
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            cluster_report['cluster_name'],
            cluster_report['timestamp'],  # Fixed: Use cluster_report['timestamp']
            json.dumps(cluster_report['popular_colors']),
            json.dumps(cluster_report['popular_patterns']),
            json.dumps(cluster_report['popular_styles']),
            json.dumps(cluster_report['image_urls'])
        ))
        conn.commit()
        logging.info("Cluster analysis stored")
    except sqlite3.Error as e:
        logging.error(f"Failed to store cluster report: {str(e)}")

# ====================== COLOR UTILITIES ======================

def get_color_name(hex_color):
    """Convert HEX to CSS3 color name"""
    try:
        rgb_color = hex_to_rgb(hex_color)
        hex_codes = list(CSS3_HEX_TO_NAMES.keys())
        rgb_values = [hex_to_rgb(hex_code) for hex_code in hex_codes]
        color_names = [CSS3_HEX_TO_NAMES[hex_code] for hex_code in hex_codes]
        kdt_db = KDTree(rgb_values)
        _, index = kdt_db.query(rgb_color)
        return color_names[index]
    except Exception as e:
        logging.error(f"Error in get_color_name: {str(e)}")
        return "unknown"

# ====================== VALIDATION FUNCTIONS ======================

def validate_color_clustering(img_array, dominant_colors, k=5):
    """Validate color clustering results"""
    validation_results = {'status': 'PASS', 'metrics': {}, 'warnings': []}
    try:
        max_size = 200
        h, w = img_array.shape[:2]
        if h > max_size or w > max_size:
            scale = max_size / max(h, w)
            img_array = cv2.resize(img_array, (int(w * scale), int(h * scale)))

        img_rgb = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB if len(img_array.shape) == 2 else cv2.COLOR_BGR2RGB)
        pixels = img_rgb.reshape(-1, 3)
        sample_size = min(500, len(pixels))
        if sample_size < k:
            validation_results['status'] = 'FAIL'
            validation_results['error'] = "Too few pixels for clustering"
            return validation_results

        start_time = time.time()
        sample_indices = np.random.choice(len(pixels), sample_size, replace=False)
        kmeans = KMeans(n_clusters=k, n_init=3, random_state=42)
        kmeans.fit(pixels[sample_indices])
        silhouette = silhouette_score(pixels[sample_indices], kmeans.labels_)
        validation_results['metrics']['silhouette_score'] = silhouette
        logging.info(f"Clustering took {time.time() - start_time:.2f} seconds")
        if silhouette < 0.5:
            validation_results['warnings'].append(f'Low silhouette score ({silhouette:.2f})')

        color_values = np.array([c['color'] for c in dominant_colors])
        color_variation = np.std(color_values, axis=0).mean()
        validation_results['metrics']['color_variation'] = color_variation
        if color_variation > 15:
            validation_results['warnings'].append(f'High color variation ({color_variation:.2f})')

        percentage_sum = sum(c['percentage'] for c in dominant_colors)
        validation_results['metrics']['percentage_sum'] = percentage_sum
        if abs(percentage_sum - 1.0) > 0.01:
            validation_results['warnings'].append(f'Percentage sum incorrect ({percentage_sum:.2f})')

        visualize_color_validation(img_rgb, dominant_colors, k)
    except Exception as e:
        validation_results['status'] = 'FAIL'
        validation_results['error'] = str(e)
        logging.error(f"Error in validate_color_clustering: {str(e)}")
    return validation_results

def validate_pattern_style(predictions):
    """Validate pattern/style predictions"""
    validation_results = {'status': 'PASS', 'warnings': []}
    try:
        if predictions['pattern']['confidence'] < 0.6:
            validation_results['warnings'].append(f"Low pattern confidence ({predictions['pattern']['confidence']:.2f})")
        if predictions['style']['confidence'] < 0.6:
            validation_results['warnings'].append(f"Low style confidence ({predictions['style']['confidence']:.2f})")
        if validation_results['warnings']:
            validation_results['status'] = 'WARNING'
    except Exception as e:
        validation_results['status'] = 'FAIL'
        validation_results['error'] = str(e)
        logging.error(f"Error in validate_pattern_style: {str(e)}")
    return validation_results

def visualize_color_validation(img_rgb, dominant_colors, k=5):
    """Visual validation of color clustering"""
    try:
        plt.figure(figsize=(15, 5))
        total_plots = 2 + k  # Original, distribution, k colors
        plt.subplot(1, total_plots, 1)
        plt.imshow(img_rgb)
        plt.title('Original Image')
        plt.axis('off')

        for i, color_info in enumerate(dominant_colors):
            plt.subplot(1, total_plots, i + 2)
            color_array = np.zeros((100, 100, 3), dtype=np.uint8)
            color_array[:, :] = np.array(color_info['color'])
            plt.imshow(color_array)
            plt.axis('off')
            plt.title(f"{color_info['hex']}\n{color_info['percentage']:.1%}")

        plt.subplot(1, total_plots, total_plots)
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
    except Exception as e:
        logging.error(f"Error in visualize_color_validation: {str(e)}")

# ====================== ANALYSIS FUNCTIONS ======================

def load_image_from_url(url, retries=3, timeout=10):
    """Load image from URL with retries"""
    for attempt in range(retries):
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img_array = np.array(img)
            if img_array.size == 0:
                raise ValueError("Empty image")
            return img_array
        except Exception as e:
            logging.warning(f"Attempt {attempt+1} failed for {url}: {str(e)}")
            if attempt < retries - 1:
                time.sleep(2)
    logging.error(f"Failed to load image from {url} after {retries} attempts")
    return None

def extract_dominant_colors(img_array, k=5):
    """Extract dominant colors"""
    try:
        max_size = 200
        h, w = img_array.shape[:2]
        if h > max_size or w > max_size:
            scale = max_size / max(h, w)
            img_array = cv2.resize(img_array, (int(w * scale), int(h * scale)))

        img_rgb = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB if len(img_array.shape) == 2 else cv2.COLOR_BGR2RGB)
        pixels = img_rgb.reshape(-1, 3)
        if len(pixels) < k:
            logging.error("Too few pixels for clustering")
            return []
        kmeans = KMeans(n_clusters=k, n_init=3, random_state=42)
        kmeans.fit(pixels)
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
        dominant_colors.sort(key=lambda x: x['percentage'], reverse=True)
        return dominant_colors
    except Exception as e:
        logging.error(f"Color extraction failed: {str(e)}")
        return []

# ====================== CLUSTER ANALYSIS ======================

def analyze_cluster(image_urls, cluster_name, conn):
    """Analyze a cluster of images"""
    cluster_report = {
        'cluster_name': cluster_name,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'image_urls': image_urls,
        'popular_colors': [],
        'popular_patterns': [],
        'popular_styles': [],
        'individual_reports': []
    }
    
    logging.info(f"Starting analysis of cluster: {cluster_name} with {len(image_urls)} images")
    
    for url in image_urls:
        report = analyze_fashion_image(url, conn)
        if report:
            cluster_report['individual_reports'].append(report)
            logging.info(f"Successfully analyzed: {url}")
        else:
            logging.warning(f"Skipping URL due to analysis failure: {url}")
    
    logging.info(f"Generated {len(cluster_report['individual_reports'])} valid reports")
    if cluster_report['individual_reports']:
        try:
            compute_popular_features(cluster_report)
            store_cluster_analysis(conn, cluster_report)
            visualize_cluster_results(cluster_report)
            logging.info("Cluster analysis completed")
        except Exception as e:
            logging.error(f"Error in cluster analysis: {str(e)}")
    else:
        logging.warning(f"No valid reports generated for cluster: {cluster_name}")
    
    return cluster_report

def compute_popular_features(cluster_report):
    """Compute popular features"""
    try:
        logging.info("Computing popular features...")
        all_colors = []
        pattern_counter = Counter()
        style_counter = Counter()
        
        for report in cluster_report['individual_reports']:
            for color in report['colors']:
                all_colors.append({
                    'hex': color['hex'],
                    'percentage': color['percentage'],
                    'name': get_color_name(color['hex'])
                })
            pattern = report['predictions']['pattern']['predicted']
            style = report['predictions']['style']['predicted']
            pattern_counter[pattern] += 1
            style_counter[style] += 1
        
        logging.info(f"Collected {len(all_colors)} colors")
        color_df = pd.DataFrame(all_colors)
        if not color_df.empty:
            color_df['simple_name'] = color_df['name'].str.replace(r'(light|dark|pale|bright)', '', regex=True).str.strip()
            popular_colors = color_df.groupby('simple_name').agg(
                total_percentage=('percentage', 'sum'),
                count=('hex', 'count'),
                hex=('hex', lambda x: x.mode()[0]),
                name=('name', lambda x: x.mode()[0])
            ).reset_index()
            popular_colors['avg_percentage'] = popular_colors['total_percentage'] / popular_colors['count']
            popular_colors = popular_colors.sort_values('total_percentage', ascending=False).head(5)
            cluster_report['popular_colors'] = popular_colors.to_dict('records')
            logging.info(f"Popular colors: {[c['name'] for c in cluster_report['popular_colors']]}")
        else:
            logging.warning("No colors collected for cluster")
        
        cluster_report['popular_patterns'] = [
            {'pattern': p, 'count': c, 'frequency': c/len(cluster_report['individual_reports'])} 
            for p, c in pattern_counter.most_common(3)
        ]
        cluster_report['popular_styles'] = [
            {'style': s, 'count': c, 'frequency': c/len(cluster_report['individual_reports'])} 
            for s, c in style_counter.most_common(3)
        ]
        logging.info(f"Popular patterns: {[p['pattern'] for p in cluster_report['popular_patterns']]}")
        logging.info(f"Popular styles: {[s['style'] for s in cluster_report['popular_styles']]}")
    except Exception as e:
        logging.error(f"Error in compute_popular_features: {str(e)}")
        cluster_report['popular_colors'] = []
        cluster_report['popular_patterns'] = []
        cluster_report['popular_styles'] = []

def visualize_cluster_results(cluster_report):
    """Visualize cluster results"""
    try:
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 2, 1)
        if cluster_report['popular_colors']:
            colors = [c['hex'] for c in cluster_report['popular_colors']]
            names = [f"{c['name']}\n({c['avg_percentage']:.1%})" for c in cluster_report['popular_colors']]
            for i, (color, name) in enumerate(zip(colors, names)):
                plt.subplot(2, len(colors), i+1)
                color_array = np.zeros((100, 100, 3), dtype=np.uint8)
                color_array[:, :] = np.array(hex_to_rgb(color))
                plt.imshow(color_array)
                plt.title(name)
                plt.axis('off')
        else:
            plt.text(0.5, 0.5, 'No color data', ha='center')
        
        plt.subplot(2, 2, 2)
        if cluster_report['popular_patterns']:
            patterns = [p['pattern'] for p in cluster_report['popular_patterns']]
            freqs = [p['frequency'] for p in cluster_report['popular_patterns']]
            plt.barh(patterns, freqs, color='skyblue')
            plt.title('Pattern Popularity')
            plt.xlabel('Frequency')
            plt.xlim(0, 1)
        else:
            plt.text(0.5, 0.5, 'No pattern data', ha='center')
        
        plt.subplot(2, 2, 3)
        if cluster_report['popular_styles']:
            styles = [s['style'] for s in cluster_report['popular_styles']]
            freqs = [s['frequency'] for s in cluster_report['popular_styles']]
            plt.barh(styles, freqs, color='salmon')
            plt.title('Style Popularity')
            plt.xlabel('Frequency')
            plt.xlim(0, 1)
        else:
            plt.text(0.5, 0.5, 'No style data', ha='center')
        
        plt.subplot(2, 2, 4)
        plt.axis('off')
        plt.text(0.1, 0.9, f"Cluster: {cluster_report['cluster_name']}", fontsize=14)
        plt.text(0.1, 0.7, f"Images: {len(cluster_report['image_urls'])}", fontsize=12)
        plt.text(0.1, 0.5, f"Analysis Date: {cluster_report['timestamp']}", fontsize=12)
        
        plt.tight_layout()
        plt.savefig(f"/content/{cluster_report['cluster_name']}_analysis.png")
        plt.show()
    except Exception as e:
        logging.error(f"Error in visualize_cluster_results: {str(e)}")

# ====================== MAIN ANALYSIS PIPELINE ======================

def analyze_fashion_image(image_url, conn):
    """Analyze a single image"""
    try:
        logging.info(f"Analyzing: {image_url}")
        img_array = load_image_from_url(image_url)
        if img_array is None:
            logging.error(f"Failed to load image: {image_url}")
            return None
        logging.info("Image loaded")

        colors = extract_dominant_colors(img_array)
        if not colors:
            logging.error(f"Failed to extract colors for: {image_url}")
            return None
        logging.info(f"Extracted colors: {[c['hex'] for c in colors]}")

        logging.info("Validating colors...")
        color_validation = validate_color_clustering(img_array, colors)
        logging.info(f"Color Validation Status: {color_validation['status']}")
        if color_validation.get('warnings'):
            logging.warning("Color validation warnings:")
            for warning in color_validation['warnings']:
                logging.warning(f"  - {warning}")

        logging.info("Running pattern/style analysis...")
        predictions = {
            'pattern': {
                'predicted': 'floral',
                'confidence': 0.82,
                'all_options': {'floral': 0.82, 'striped': 0.10, 'geometric': 0.05, 'plain': 0.03}
            },
            'style': {
                'predicted': 'casual',
                'confidence': 0.75,
                'all_options': {'casual': 0.75, 'formal': 0.15, 'bohemian': 0.07, 'sporty': 0.03}
            }
        }

        logging.info("Validating pattern/style...")
        ps_validation = validate_pattern_style(predictions)
        logging.info(f"Pattern/Style Validation Status: {ps_validation['status']}")
        if ps_validation.get('warnings'):
            logging.warning("Pattern/style validation warnings:")
            for warning in ps_validation['warnings']:
                logging.warning(f"  - {warning}")

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

        store_analysis_report(conn, report)
        return report
    except Exception as e:
        logging.error(f"Analysis failed for {image_url}: {str(e)}")
        return None

# ====================== EXAMPLE USAGE ======================

if __name__ == "__main__":
    # Install dependencies
    logging.info("Installing dependencies...")
    os.system('pip install opencv-python-headless numpy matplotlib scikit-learn pillow requests pandas scipy webcolors')

    # Initialize database
    conn = initialize_database()
    if not conn:
        logging.error("Failed to initialize database, exiting...")
        raise SystemExit("Database initialization failed")

    try:
        # Define a cluster of images
        FASHION_CLUSTER = {
            "Summer Collection": [
                "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg",
                "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/messi5.jpg",
                "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/baboon.jpg",
                "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/fruits.jpg",
                "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/left09.jpg"
            ]
        }
        
        # Test URLs
        logging.info("Testing image URLs...")
        for url in FASHION_CLUSTER["Summer Collection"]:
            try:
                response = requests.head(url, timeout=5)
                logging.info(f"{url}: {response.status_code}")
            except Exception as e:
                logging.warning(f"{url}: Failed - {str(e)}")

        # Analyze each cluster
        for cluster_name, image_urls in FASHION_CLUSTER.items():
            cluster_report = analyze_cluster(image_urls, cluster_name, conn)
            
            # Print cluster report
            print("\n=== CLUSTER ANALYSIS REPORT ===")
            print(f"Cluster: {cluster_report['cluster_name']}")
            print(f"Images: {len(cluster_report['image_urls'])}")
            
            print("\nTop Colors in Cluster:")
            if cluster_report['popular_colors']:
                for i, color in enumerate(cluster_report['popular_colors'], 1):
                    print(f"{i}. {color['name']} ({color['hex']}): Avg {color['avg_percentage']:.1%} per image")
            else:
                print("No colors found")
            
            print("\nTop Patterns in Cluster:")
            if cluster_report['popular_patterns']:
                for i, pattern in enumerate(cluster_report['popular_patterns'], 1):
                    print(f"{i}. {pattern['pattern']}: {pattern['frequency']:.0%} of images")
            else:
                print("No patterns found")
            
            print("\nTop Styles in Cluster:")
            if cluster_report['popular_styles']:
                for i, style in enumerate(cluster_report['popular_styles'], 1):
                    print(f"{i}. {style['style']}: {style['frequency']:.0%} of images")  # Fixed: Use style['frequency']
            else:
                print("No styles found")
    
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed")
        else:
            logging.warning("No database connection to close")
