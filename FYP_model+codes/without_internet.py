import torch
import cv2
import sys
import os

# Set YOLOv5 path
path = r'C:/FYPN/yolov5'
sys.path.insert(0, path)

from models.common import DetectMultiBackend
from utils.general import non_max_suppression
from utils.torch_utils import select_device

# Load model
device = select_device('')
model = DetectMultiBackend(r'C:/FYPN/best1.pt', device=device)
model.eval()

# Setup video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img = cv2.resize(frame, (640, 640))
    img_tensor = torch.from_numpy(img).permute(2, 0, 1).float().div(255.0).unsqueeze(0).to(device)

    with torch.no_grad():
        pred = model(img_tensor)
        pred = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.45)

    for det in pred:
        if det is not None and len(det):
            for *xyxy, conf, cls in det:
                print(int(cls.item()))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
