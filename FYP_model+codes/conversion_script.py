import os
import pandas as pd
import cv2

def load_annotations(data_dir, split):
    """Load annotations from individual txt files for each image and detect class names dynamically."""
    images_dir = os.path.join(data_dir, split)
    
    # Prepare to hold image paths and annotations
    data = []
    class_names = set()  # Use a set to collect unique class names
    
    # Iterate over images in the folder
    for image_name in os.listdir(images_dir):
        # Only process .jpg files (you can also handle other formats if needed)
        if image_name.endswith('.jpg'):
            # Get the path to the image
            image_path = os.path.join(images_dir, image_name)
            
            # Corresponding annotation file (e.g., image1.jpg -> image1.txt)
            annotation_file = image_name.replace('.jpg', '.txt')
            annotation_path = os.path.join(images_dir, annotation_file)
            
            if os.path.exists(annotation_path):
                # Read the annotation data from the .txt file
                with open(annotation_path, 'r') as file:
                    for line in file:
                        parts = line.strip().split()
                        
                        # Ensure the annotation format is correct (bounding box + class name + class id)
                        if len(parts) == 10:  # Expecting 8 bounding box coordinates, 1 class name, and 1 class id
                            try:
                                # Parse bounding box coordinates (convert to float and then int)
                                x_min = int(float(parts[0]))
                                y_min = int(float(parts[1]))
                                x_max = int(float(parts[2]))
                                y_max = int(float(parts[3]))
                                
                                # Get the class name (parts[8]) and class id (parts[9])
                                class_name = parts[8]  # This is where the class name is found (position 8)
                                class_id = int(parts[9])  # This is where the class ID is found (position 9)
                                
                                # Add the class name to the set of class names
                                class_names.add(class_name)

                                # Append data
                                data.append({
                                    'image_path': image_path,
                                    'x_min': x_min,
                                    'y_min': y_min,
                                    'x_max': x_max,
                                    'y_max': y_max,
                                    'class_name': class_name  # Save the class name too
                                })
                            except ValueError:
                                print(f"Error parsing bounding box in file {annotation_file} on line: {line}")
                        else:
                            print(f"Invalid format in annotation file {annotation_file} on line: {line}")
            else:
                print(f"Warning: Annotation file for {image_name} not found.")
    
    # Generate class_names mapping (you can choose how to assign class IDs)
    class_names = list(class_names)  # Convert to list
    class_names_mapping = {name: idx for idx, name in enumerate(class_names)}  # Assign unique ID to each class
    return pd.DataFrame(data), class_names_mapping

def convert_to_yolo_format(data, output_dir, class_names_mapping):
    """Convert annotations to YOLO format and save to a txt file."""
    
    # Ensure that the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for index, row in data.iterrows():
        # Get the class ID from the class_names_mapping
        class_id = class_names_mapping[row['class_name']]
        
        # Load image to get dimensions
        img = cv2.imread(row['image_path'])
        h, w, _ = img.shape
        
        # Calculate YOLO format values
        x_center = ((row['x_min'] + row['x_max']) / 2) / w
        y_center = ((row['y_min'] + row['y_max']) / 2) / h
        width = (row['x_max'] - row['x_min']) / w
        height = (row['y_max'] - row['y_min']) / h
        
        # Create a YOLO annotation string
        yolo_annotation = f"{class_id} {x_center} {y_center} {width} {height}\n"
        
        # Save the YOLO annotations in a txt file with the same name as the image
        txt_file_name = os.path.join(output_dir, os.path.basename(row['image_path']).replace('.jpg', '.txt'))
        
        # Write to the file
        with open(txt_file_name, 'w') as f:
            f.write(yolo_annotation)

# Update data_dir to point to the correct directory containing your images and annotations
data_dir = r"c:\Users\HS TRADER\Desktop\FYPN\yolov5\utils\dataset1"

# Load the data for each split and detect class names
train_data, class_names_mapping = load_annotations(data_dir, 'train')
test_data, _ = load_annotations(data_dir, 'test')  # We don't need to remap class IDs for the test data
valid_data, _ = load_annotations(data_dir, 'valid')

# Print class names and their mapped IDs
print("Detected class names and IDs:")
for class_name, class_id in class_names_mapping.items():
    print(f"Class name: {class_name}, Class ID: {class_id}")

# Convert train, test, and valid annotations to YOLO format
convert_to_yolo_format(train_data, r'C:\path\to\output\train', class_names_mapping)
convert_to_yolo_format(test_data, r'C:\path\to\output\test', class_names_mapping)
convert_to_yolo_format(valid_data, r'C:\path\to\output\valid', class_names_mapping)


#training
#cd C:\Users\HS TRADER\Desktop\FYPN\yolov5
#python train.py --img 416 --batch 16 --epochs 50 --data dataset\data.yaml --weights yolov5s.pt

#testing
#cd C:\Users\HS TRADER\Downloads\FYP\yolov5
#python val.py --weights runs/train/exp2/weights/best.pt --data data.yaml --img 640


#python train.py --img 416 --batch 16 --epochs 50 --data dataset1\data.yaml --weights yolov5s.pt
#python train.py --img 416 --batch 16 --epochs 50 --data "C:/Users/HS TRADER/Desktop/FYPN/dataset1/data.yaml" --weights yolov5s.pt