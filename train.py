from ultralytics import YOLO
import os

def train():
    model = YOLO("yolov8n.pt")
    model.train(
        data="data/kitti.yaml",
        epochs=50,
        imgsz=(375, 1242),
        batch=8,
        project="yolov8",
        name="kitti_train",
        exist_ok=True,
    )

if __name__ == "__main__":
    train()