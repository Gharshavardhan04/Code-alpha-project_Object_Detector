#!/usr/bin/env python
"""
Quick test script for Object Detection and Tracking system
This script provides simple testing options without command-line complexity
"""
import cv2
import sys
from pathlib import Path
from src.video_processor import VideoObjectDetectionTracker


def print_menu():
    """Print menu options"""
    print("\n" + "="*60)
    print("OBJECT DETECTION AND TRACKING - QUICK TEST")
    print("="*60)
    print("\n1. Test with default webcam (ID: 0)")
    print("2. Test with specific webcam (enter ID)")
    print("3. Test with video file from videos/ folder")
    print("4. Test with custom video file path")
    print("5. Batch process all videos in videos/ folder")
    print("6. Exit")
    print("\n" + "="*60)


def test_webcam(webcam_id=0):
    """Test with webcam"""
    print(f"\nStarting webcam test (ID: {webcam_id})...")
    print("Controls:")
    print("  - Press 'q' to quit")
    print("  - Press 'p' to pause/resume")
    
    pipeline = VideoObjectDetectionTracker(
        model_name='yolov8n',
        conf_threshold=0.5
    )
    
    pipeline.process_video(
        source=webcam_id,
        output_path=None,
        display=True,
        resize=True
    )


def test_video_file(video_path):
    """Test with video file"""
    if not Path(video_path).exists():
        print(f"✗ Video file not found: {video_path}")
        return
    
    print(f"\nProcessing video: {video_path}")
    print("Controls:")
    print("  - Press 'q' to quit")
    print("  - Press 'p' to pause/resume")
    
    output_path = Path("output") / f"tracked_{Path(video_path).name}"
    
    pipeline = VideoObjectDetectionTracker(
        model_name='yolov8n',
        conf_threshold=0.5
    )
    
    pipeline.process_video(
        source=video_path,
        output_path=str(output_path),
        display=True,
        resize=True
    )
    
    print(f"\n✓ Output saved to: {output_path}")


def list_video_files():
    """List video files in videos/ folder"""
    videos_dir = Path("videos")
    if not videos_dir.exists():
        print("Videos directory not found. Creating it...")
        videos_dir.mkdir(exist_ok=True)
        print(f"Created: {videos_dir}")
        print("Please add video files to the 'videos' folder and try again.")
        return []
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    video_files = []
    for ext in video_extensions:
        video_files.extend(videos_dir.glob(f"*{ext}"))
        video_files.extend(videos_dir.glob(f"*{ext.upper()}"))
    
    return sorted(set(video_files))


def batch_process_videos():
    """Batch process all videos in videos/ folder"""
    video_files = list_video_files()
    
    if not video_files:
        print("No video files found in videos/ folder")
        return
    
    print(f"\nFound {len(video_files)} video file(s):")
    for i, video_file in enumerate(video_files, 1):
        print(f"  {i}. {video_file.name}")
    
    confirm = input("\nProcess all videos? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Batch processing cancelled")
        return
    
    from src.video_processor import BatchVideoProcessor
    
    processor = BatchVideoProcessor(model_name='yolov8n', conf_threshold=0.5)
    processor.process_batch(video_files, output_dir='output')


def main():
    """Main function"""
    try:
        while True:
            print_menu()
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                test_webcam(0)
            
            elif choice == '2':
                try:
                    webcam_id = int(input("Enter webcam ID (usually 0 or 1): "))
                    test_webcam(webcam_id)
                except ValueError:
                    print("✗ Invalid webcam ID")
            
            elif choice == '3':
                video_files = list_video_files()
                if video_files:
                    print("\nAvailable videos:")
                    for i, video_file in enumerate(video_files, 1):
                        print(f"  {i}. {video_file.name}")
                    
                    try:
                        idx = int(input("Select video number: ")) - 1
                        if 0 <= idx < len(video_files):
                            test_video_file(video_files[idx])
                        else:
                            print("✗ Invalid selection")
                    except ValueError:
                        print("✗ Invalid input")
                else:
                    print("No videos found in videos/ folder")
            
            elif choice == '4':
                video_path = input("Enter video file path: ").strip()
                test_video_file(video_path)
            
            elif choice == '5':
                batch_process_videos()
            
            elif choice == '6':
                print("Exiting...")
                sys.exit(0)
            
            else:
                print("✗ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
