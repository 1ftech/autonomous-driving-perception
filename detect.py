from ultralytics import YOLO
import cv2

def detect():
    model = YOLO("yolov8/kitti_train/weights/best.pt")
    results = model.predict("data/kitti/2011_09_26/2011_09_26_drive_0001_sync/image_02/data/0000000000.png")
    results[0].show()

if __name__ == "__main__":
    detect()