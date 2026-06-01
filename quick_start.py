"""
Quick start scripts for common use cases
"""
from src.video_processor import VideoObjectDetectionTracker
import os


def run_webcam_demo():
    """Run real-time detection and tracking with webcam"""
    print("Starting Webcam Demo (Object Detection & Tracking)")
    print("Press 'q' to quit")
    
    pipeline = VideoObjectDetectionTracker(
        model_name='yolov8n.pt',  # Fastest model
        conf_threshold=0.5
    )
    
    pipeline.process_video(
        source=0,  # Default webcam
        output_path=None,  # Don't save output
        display=True,
        resize=True
    )


def run_video_demo():
    """Run detection and tracking on a sample video"""
    video_dir = 'videos'
    
    # Find first video file
    if os.path.exists(video_dir):
        video_files = [f for f in os.listdir(video_dir) 
                      if f.lower().endswith(('.mp4', '.avi', '.mov'))]
        
        if video_files:
            video_path = os.path.join(video_dir, video_files[0])
            output_path = os.path.join('output', f'tracked_{video_files[0]}')
            
            print(f"Processing: {video_path}")
            
            pipeline = VideoObjectDetectionTracker(
                model_name='yolov8s.pt',  # Small model for better accuracy
                conf_threshold=0.5
            )
            
            pipeline.process_video(
                source=video_path,
                output_path=output_path,
                display=True,
                resize=True
            )
        else:
            print(f"No video files found in '{video_dir}' directory")
            print("Place your video files (.mp4, .avi, .mov) in the 'videos' folder")
    else:
        print(f"'{video_dir}' directory not found")
        print("Please create a 'videos' folder and add video files")


def run_custom_video(video_path, model='yolov8n.pt', conf=0.5, output_path=None):
    """
    Run detection and tracking on custom video
    
    Args:
        video_path: Path to video file
        model: YOLO model to use
        conf: Confidence threshold
        output_path: Path to save output (optional)
    """
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return
    
    print(f"Processing: {video_path}")
    print(f"Model: {model}, Confidence: {conf}")
    
    pipeline = VideoObjectDetectionTracker(
        model_name=model,
        conf_threshold=conf
    )
    
    pipeline.process_video(
        source=video_path,
        output_path=output_path,
        display=True,
        resize=True
    )


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'webcam':
            run_webcam_demo()
        elif sys.argv[1] == 'video':
            run_video_demo()
        elif sys.argv[1].endswith(('.mp4', '.avi', '.mov')):
            run_custom_video(sys.argv[1])
        else:
            print("Usage:")
            print("  python quick_start.py webcam         - Run webcam demo")
            print("  python quick_start.py video          - Run video demo")
            print("  python quick_start.py <video.mp4>    - Run on specific video")
    else:
        print("Quick Start Script")
        print("="*50)
        print("Choose an option:")
        print("1. Webcam (type 'python quick_start.py webcam')")
        print("2. Video (type 'python quick_start.py video')")
        print("3. Custom video (type 'python quick_start.py path/to/video.mp4')")
