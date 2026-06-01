#!/usr/bin/env python
"""
Demonstration script showing how to use the Object Detection and Tracking system
"""

from src.video_processor import VideoObjectDetectionTracker
from src.detector import YOLODetector
from pathlib import Path
import cv2


def demo_1_webcam_basic():
    """Demo 1: Basic webcam detection"""
    print("\n" + "="*60)
    print("DEMO 1: Basic Webcam Detection")
    print("="*60)
    print("This demo shows basic real-time detection with default settings")
    print("Press 'q' to exit\n")
    
    pipeline = VideoObjectDetectionTracker()
    pipeline.process_video(source=0, display=True, resize=True)


def demo_2_webcam_with_output():
    """Demo 2: Webcam with output video saving"""
    print("\n" + "="*60)
    print("DEMO 2: Webcam with Output Video Saving")
    print("="*60)
    print("This demo saves the tracked video to output/ folder")
    print("Press 'q' to exit\n")
    
    pipeline = VideoObjectDetectionTracker(model_name='yolov8n.pt')
    pipeline.process_video(
        source=0,
        output_path='output/webcam_demo.mp4',
        display=True,
        resize=True
    )


def demo_3_video_file():
    """Demo 3: Process video file from videos/ folder"""
    print("\n" + "="*60)
    print("DEMO 3: Video File Processing")
    print("="*60)
    
    videos_dir = Path('videos')
    if not videos_dir.exists():
        print("Videos directory not found. Create videos/ folder and add video files.")
        return
    
    # Find first video file
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    video_files = []
    for ext in video_extensions:
        video_files.extend(videos_dir.glob(f"*{ext}"))
    
    if not video_files:
        print("No video files found in videos/ folder")
        return
    
    video_file = video_files[0]
    print(f"Processing: {video_file.name}")
    print("Press 'q' to exit\n")
    
    pipeline = VideoObjectDetectionTracker(model_name='yolov8n.pt')
    pipeline.process_video(
        source=str(video_file),
        output_path=f'output/demo_{video_file.stem}_tracked.mp4',
        display=True,
        resize=True
    )


def demo_4_high_accuracy():
    """Demo 4: High accuracy mode with larger model"""
    print("\n" + "="*60)
    print("DEMO 4: High Accuracy Mode")
    print("="*60)
    print("Using larger YOLOv8 model for better accuracy")
    print("Press 'q' to exit\n")
    
    pipeline = VideoObjectDetectionTracker(
        model_name='yolov8m.pt',  # Medium model
        conf_threshold=0.4         # Lower threshold for more detections
    )
    pipeline.process_video(source=0, display=True, resize=False)


def demo_5_fast_mode():
    """Demo 5: Fast mode for real-time processing"""
    print("\n" + "="*60)
    print("DEMO 5: Fast Mode")
    print("="*60)
    print("Optimized for speed with nano model")
    print("Press 'q' to exit\n")
    
    pipeline = VideoObjectDetectionTracker(
        model_name='yolov8n.pt',   # Nano model (fastest)
        conf_threshold=0.6         # Higher threshold for fewer detections
    )
    pipeline.process_video(source=0, display=True, resize=True)


def demo_6_detector_only():
    """Demo 6: Using detector module only"""
    print("\n" + "="*60)
    print("DEMO 6: Object Detector Only")
    print("="*60)
    print("Using detector without tracking")
    print("Press 'q' to exit\n")
    
    detector = YOLODetector(model_name='yolov8n.pt', conf_threshold=0.5)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Cannot open webcam")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Resize for faster processing
            height, width = frame.shape[:2]
            scale = min(1280 / width, 720 / height)
            if scale < 1:
                frame = cv2.resize(frame, (int(width*scale), int(height*scale)))
            
            # Detect objects
            detections, class_names = detector.detect(frame)
            
            # Draw detections
            for i, det in enumerate(detections):
                x1, y1, x2, y2, conf, class_id = det
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                label = f"{class_names[i] if i < len(class_names) else 'Unknown'}: {conf:.2f}"
                cv2.putText(frame, label, (int(x1), int(y1)-10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Display
            cv2.imshow('Object Detection (No Tracking)', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()


def main():
    """Main demo runner"""
    demos = [
        ("Basic Webcam Detection", demo_1_webcam_basic),
        ("Webcam with Output Video", demo_2_webcam_with_output),
        ("Video File Processing", demo_3_video_file),
        ("High Accuracy Mode", demo_4_high_accuracy),
        ("Fast Mode", demo_5_fast_mode),
        ("Detector Only (No Tracking)", demo_6_detector_only),
    ]
    
    while True:
        print("\n" + "="*60)
        print("OBJECT DETECTION & TRACKING DEMOS")
        print("="*60)
        
        for i, (name, _) in enumerate(demos, 1):
            print(f"{i}. {name}")
        
        print(f"{len(demos)+1}. Exit")
        print("="*60)
        
        try:
            choice = int(input("\nSelect demo (1-{}): ".format(len(demos)+1)))
            
            if choice == len(demos) + 1:
                print("Exiting...")
                break
            
            if 1 <= choice <= len(demos):
                demos[choice-1][1]()
            else:
                print("Invalid choice")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except ValueError:
            print("Invalid input")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    main()
