"""
Utility functions for visualization and data processing
"""
import cv2
import numpy as np
from collections import deque


class TrackingVisualization:
    """Handle visualization of tracking results"""
    
    def __init__(self, max_track_history=30):
        """
        Initialize tracking visualization
        
        Args:
            max_track_history: Number of previous positions to display
        """
        self.max_track_history = max_track_history
        self.tracks_history = {}  # Store history of each track
    
    def update_history(self, track_id, centroid):
        """Update tracking history for a track"""
        if track_id not in self.tracks_history:
            self.tracks_history[track_id] = deque(maxlen=self.max_track_history)
        self.tracks_history[track_id].append(centroid)
    
    def draw_boxes_and_tracks(self, frame, detections, tracker_results):
        """
        Draw bounding boxes, tracking IDs, and track history
        
        Args:
            frame: Input frame
            detections: Detection results [x1, y1, x2, y2, conf, class]
            tracker_results: Tracker output with track IDs
        """
        output_frame = frame.copy()
        
        # Define color palette
        colors = self._generate_colors(100)
        
        # Draw detections with tracking IDs
        for detection in tracker_results:
            if len(detection) >= 5:
                x1, y1, x2, y2, track_id = int(detection[0]), int(detection[1]), \
                                           int(detection[2]), int(detection[3]), int(detection[4])
                
                # Get color based on track ID
                color = colors[track_id % len(colors)]
                
                # Draw bounding box
                cv2.rectangle(output_frame, (x1, y1), (x2, y2), color, 2)
                
                # Calculate centroid
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                
                # Update history
                self.update_history(track_id, (cx, cy))
                
                # Draw track ID
                label = f"ID: {track_id}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                cv2.rectangle(output_frame, (x1, y1 - label_size[1] - 5),
                            (x1 + label_size[0], y1), color, -1)
                cv2.putText(output_frame, label, (x1, y1 - 5),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                # Draw track history
                if track_id in self.tracks_history:
                    points = list(self.tracks_history[track_id])
                    for i in range(1, len(points)):
                        cv2.line(output_frame, points[i-1], points[i], color, 1)
                        cv2.circle(output_frame, points[i], 2, color, -1)
        
        return output_frame
    
    def _generate_colors(self, num_colors):
        """Generate distinct colors for track visualization"""
        colors = []
        for i in range(num_colors):
            hue = int((i / num_colors) * 180)
            saturation = 255
            value = 255
            hsv = np.uint8([[[hue, saturation, value]]])
            rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0][0]
            colors.append(tuple(map(int, rgb)))
        return colors


class VideoHandler:
    """Handle video input/output operations"""
    
    def __init__(self, source=0, output_path=None, fps=30, frame_width=1280, frame_height=720):
        """
        Initialize video handler
        
        Args:
            source: Video file path (string) or webcam index (int)
            output_path: Path to save output video
            fps: Frames per second for output
            frame_width: Frame width
            frame_height: Frame height
        """
        self.source = source
        self.output_path = output_path
        self.fps = fps
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.cap = None
        self.out = None
    
    def open_video(self):
        """Open video source (webcam or file)"""
        try:
            if isinstance(self.source, int):
                # Webcam input
                self.cap = cv2.VideoCapture(self.source)
            else:
                # Video file input
                self.cap = cv2.VideoCapture(self.source)
            
            if not self.cap.isOpened():
                raise ValueError(f"Cannot open video source: {self.source}")
            
            # Set video properties
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS)) or 30
            
            print(f"Video opened: {self.frame_width}x{self.frame_height} @ {self.fps} FPS")
            return True
        except Exception as e:
            print(f"Error opening video: {e}")
            return False
    
    def setup_output_video(self):
        """Setup video writer for output"""
        if self.output_path:
            try:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                self.out = cv2.VideoWriter(
                    self.output_path,
                    fourcc,
                    self.fps,
                    (self.frame_width, self.frame_height)
                )
                print(f"Output video setup: {self.output_path}")
                return True
            except Exception as e:
                print(f"Error setting up output video: {e}")
                return False
        return True
    
    def read_frame(self):
        """Read next frame"""
        if self.cap:
            ret, frame = self.cap.read()
            return ret, frame
        return False, None
    
    def write_frame(self, frame):
        """Write frame to output video"""
        if self.out:
            self.out.write(frame)
    
    def release(self):
        """Release video resources"""
        if self.cap:
            self.cap.release()
        if self.out:
            self.out.release()
        cv2.destroyAllWindows()


class FrameProcessor:
    """Process and resize frames for consistent model input"""
    
    @staticmethod
    def resize_frame(frame, max_width=1280, max_height=720):
        """Resize frame while maintaining aspect ratio"""
        height, width = frame.shape[:2]
        
        # Calculate scaling factor
        scale = min(max_width / width, max_height / height)
        
        if scale < 1:
            new_width = int(width * scale)
            new_height = int(height * scale)
            return cv2.resize(frame, (new_width, new_height))
        
        return frame
    
    @staticmethod
    def add_info_panel(frame, fps, num_tracks):
        """Add information panel to frame"""
        info_text = f"FPS: {fps:.1f} | Tracks: {num_tracks}"
        cv2.putText(frame, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        return frame
