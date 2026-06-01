"""
YOLOv8 Object Detection Module
"""
import cv2
import numpy as np
from ultralytics import YOLO
import os


class YOLODetector:
    """YOLO Object Detector for real-time detection"""
    
    def __init__(self, model_name='yolov8n.pt', conf_threshold=0.5):
        """
        Initialize YOLO detector
        
        Args:
            model_name: YOLO model to use (nano, small, medium, large, xlarge)
            conf_threshold: Confidence threshold for detections
        """
        self.conf_threshold = conf_threshold
        self.model_name = model_name
        self.model = None
        self.device = self._check_device()
        self._load_model()
    
    def _check_device(self):
        """Check if CUDA is available"""
        try:
            import torch
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"Using device: {device}")
            return device
        except:
            return 'cpu'
    
    def _load_model(self):
        """Load YOLO model"""
        try:
            import torch
            
            # Monkey-patch torch.load to use weights_only=False for model loading.
            # torch 2.12.0+ defaults to weights_only=True, which blocks ultralytics
            # checkpoints that use pickling. This is a temporary workaround until
            # ultralytics updates to handle the new torch defaults.
            original_torch_load = torch.load
            
            def torch_load_with_weights_only_false(*args, **kwargs):
                """Wrapper that defaults weights_only to False for model checkpoints."""
                if 'weights_only' not in kwargs:
                    kwargs['weights_only'] = False
                return original_torch_load(*args, **kwargs)
            
            try:
                torch.load = torch_load_with_weights_only_false
                
                print(f"Loading YOLO model: {self.model_name}")
                self.model = YOLO(self.model_name)
                print(f"✓ Model loaded successfully!")
            finally:
                # Always restore the original torch.load
                torch.load = original_torch_load
        
        except Exception as e:
            print(f"✗ Error loading YOLO model: {e}")
            raise
    
    def detect(self, frame):
        """
        Run detection on frame
        
        Args:
            frame: Input frame (BGR)
        
        Returns:
            detections: Array of [x1, y1, x2, y2, conf, class_id]
            class_names: List of class names
        """
        try:
            results = self.model(frame, conf=self.conf_threshold, verbose=False)
            
            detections = []
            class_names = []
            
            if len(results) > 0:
                result = results[0]
                
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        
                        detections.append([
                            float(x1), float(y1), float(x2), float(y2),
                            float(conf), int(class_id)
                        ])
                        
                        # Get class name
                        if class_id < len(result.names):
                            class_names.append(result.names[class_id])
            
            return np.array(detections) if detections else np.empty((0, 6)), class_names
        
        except Exception as e:
            print(f"Error during detection: {e}")
            return np.empty((0, 6)), []
    
    def get_class_names(self):
        """Get list of class names"""
        if self.model and hasattr(self.model, 'names'):
            return self.model.names
        return []
