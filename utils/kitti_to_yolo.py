# Converts KITTI's tracklet_labels.xml → YOLO .txt files
import os
import xml.etree.ElementTree as ET

def parse_kitti_labels(xml_path, output_dir, img_width=1242, img_height=375):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    for frame in root.findall('.//frame'):
        frame_id = int(frame.attrib['id'])
        with open(f"{output_dir}/{frame_id:06d}.txt", 'w') as f:
            for obj in frame.findall('.//object'):
                class_name = obj.find('type').text
                bbox = obj.find('.//bbox2D')
                x1 = float(bbox.find('x1').text)
                y1 = float(bbox.find('y1').text)
                x2 = float(bbox.find('x2').text)
                y2 = float(bbox.find('y2').text)
                
                # Convert to YOLO format
                cx = (x1 + x2) / 2 / img_width
                cy = (y1 + y2) / 2 / img_height
                w = (x2 - x1) / img_width
                h = (y2 - y1) / img_height
                
                class_id = {"Car": 2, "Cyclist": 1, "Tram": 7}.get(class_name, -1)
                if class_id != -1:
                    f.write(f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n")

# Usage
parse_kitti_labels(
    xml_path="data/kitti/2011_09_26/2011_09_26_drive_0001_sync/tracklet_labels.xml",
    output_dir="data/labels"
)