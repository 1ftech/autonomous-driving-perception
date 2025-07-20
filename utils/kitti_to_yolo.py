import os
import xml.etree.ElementTree as ET
from tqdm import tqdm
import argparse

def convert_kitti_to_yolo(xml_path, output_dir, img_width=1242, img_height=375):
    """Convert KITTI annotation to YOLO format"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    frame_id = os.path.splitext(os.path.basename(xml_path))[0]
    output_path = os.path.join(output_dir, f"{frame_id}.txt")
    
    with open(output_path, 'w') as f:
        for obj in root.findall('.//object'):
            class_name = obj.find('type').text
            bbox = obj.find('.//bndbox')
            xmin = float(bbox.find('xmin').text)
            ymin = float(bbox.find('ymin').text)
            xmax = float(bbox.find('xmax').text)
            ymax = float(bbox.find('ymax').text)
            
            # Convert to YOLO format
            x_center = (xmin + xmax) / 2 / img_width
            y_center = (ymin + ymax) / 2 / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height
            
            # Class mapping (adjust as needed)
            class_id = {
                "Pedestrian": 0,
                "Cyclist": 1,
                "Car": 2,
                "Tram": 3
            }.get(class_name, -1)
            
            if class_id != -1:
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def process_dataset(xml_dir, output_dir):
    """Process all XML files in a directory"""
    os.makedirs(output_dir, exist_ok=True)
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    
    for xml_file in tqdm(xml_files, desc=f"Processing {os.path.basename(xml_dir)}"):
        convert_kitti_to_yolo(
            os.path.join(xml_dir, xml_file),
            output_dir
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--kitti_root', type=str, required=True, 
                       help='Root directory of KITTI dataset')
    parser.add_argument('--output_root', type=str, required=True,
                       help='Root output directory for YOLO labels')
    args = parser.parse_args()

    # Process both train and val sets
    for split in ['train', 'val']:
        xml_dir = os.path.join(args.kitti_root, 'tracklet_labels', split)
        output_dir = os.path.join(args.output_root, split)
        process_dataset(xml_dir, output_dir)
)