"""
Main video processing pipeline combining detection and tracking
"""
import cv2
import numpy as np
import time
from src.detector import YOLODetector
from src.tracker import SORTTracker
from src.utils import TrackingVisualization, VideoHandler, FrameProcessor


class VideoObjectDetectionTracker:
    """Main pipeline for object detection and tracking in videos"""
    
    def __init__(self, model_name='yolov8n.pt', conf_threshold=0.5, 
                 max_age=30, min_hits=3, iou_threshold=0.3):
        """
        Initialize detection and tracking pipeline
        
        Args:
            model_name: YOLO model to use
            conf_threshold: Confidence threshold for detections
            max_age: Max frames to keep track alive
            min_hits: Min hits to start tracking
            iou_threshold: IOU threshold for tracking association
        """
        print("Initializing detection and tracking pipeline...")
        
        self.detector = YOLODetector(model_name, conf_threshold)
        self.tracker = SORTTracker(max_age, min_hits, iou_threshold)
        self.visualizer = TrackingVisualization()
        self.frame_processor = FrameProcessor()
        
        self.frame_count = 0
        self.fps_history = []
        self.processing_times = []
    
    def process_video(self, source=0, output_path=None, display=True, resize=True):
        """
        Process video with detection and tracking
        
        Args:
            source: Video file path or webcam index (0 for default webcam)
            output_path: Path to save output video (optional)
            display: Whether to display results in real-time
            resize: Whether to resize frames for processing
        """
        # Setup video handler
        video_handler = VideoHandler(source, output_path)
        
        if not video_handler.open_video():
            print("Failed to open video source")
            return False
        
        if not video_handler.setup_output_video():
            print("Failed to setup output video")
            video_handler.release()
            return False
        
        print("Starting video processing...")
        print("Press 'q' to quit, 'p' to pause")
        
        paused = False
        
        try:
            while True:
                if not paused:
                    ret, frame = video_handler.read_frame()
                    
                    if not ret:
                        print("End of video or error reading frame")
                        break
                    
                    # Process frame
                    start_time = time.time()
                    
                    # Resize if needed
                    if resize:
                        frame = self.frame_processor.resize_frame(frame)
                    
                    # Run detection (returns tuple of detections array and class names)
                    detections, class_names = self.detector.detect(frame)
                    
                    # Run tracking
                    tracks = self.tracker.update(detections)
                    
                    # Visualize results
                    output_frame = self.visualizer.draw_boxes_and_tracks(frame, detections, tracks)
                    
                    # Calculate FPS
                    process_time = time.time() - start_time
                    self.processing_times.append(process_time)
                    fps = 1.0 / process_time if process_time > 0 else 0
                    self.fps_history.append(fps)
                    
                    # Add info panel
                    output_frame = self.frame_processor.add_info_panel(
                        output_frame, fps, len(self.tracker.trackers)
                    )
                    
                    # Write output
                    video_handler.write_frame(output_frame)
                    
                    # Display
                    if display:
                        cv2.imshow('Object Detection and Tracking', output_frame)
                    
                    self.frame_count += 1
                    
                    # Print progress every 30 frames
                    if self.frame_count % 30 == 0:
                        avg_fps = np.mean(self.fps_history[-30:])
                        print(f"Frame {self.frame_count} | FPS: {avg_fps:.1f} | Objects: {len(tracks)}")
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Quitting...")
                    break
                elif key == ord('p'):
                    paused = not paused
                    status = "PAUSED" if paused else "RESUMING"
                    print(f"{status}")
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        
        except Exception as e:
            print(f"Error during video processing: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Cleanup
            video_handler.release()
            
            # Print statistics
            self._print_statistics()
        
        return True
    
    def _print_statistics(self):
        """Print processing statistics"""
        if self.frame_count == 0:
            return
        
        print("\n" + "="*50)
        print("Processing Statistics")
        print("="*50)
        print(f"Total frames processed: {self.frame_count}")
        print(f"Average FPS: {np.mean(self.fps_history):.2f}")
        print(f"Min FPS: {np.min(self.fps_history):.2f}")
        print(f"Max FPS: {np.max(self.fps_history):.2f}")
        print(f"Average processing time: {np.mean(self.processing_times)*1000:.2f} ms")
        print("="*50)


class BatchVideoProcessor:
    """Process multiple videos in batch"""
    
    def __init__(self, model_name='yolov8n.pt', conf_threshold=0.5):
        """Initialize batch processor"""
        self.pipeline = VideoObjectDetectionTracker(model_name, conf_threshold)
    
    def process_batch(self, video_files, output_dir=None):
        """
        Process multiple video files
        
        Args:
            video_files: List of video file paths
            output_dir: Directory to save output videos
        """
        for i, video_file in enumerate(video_files):
            print(f"\n{'='*50}")
            print(f"Processing video {i+1}/{len(video_files)}: {video_file}")
            print(f"{'='*50}")
            
            output_path = None
            if output_dir:
                import os
                filename = os.path.basename(video_file)
                output_path = os.path.join(output_dir, f"tracked_{filename}")
            
            self.pipeline.process_video(video_file, output_path, display=True, resize=True)
