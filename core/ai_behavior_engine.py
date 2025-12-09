
import numpy as np
import random
from dataclasses import dataclass
from typing import List, Tuple
import time

@dataclass
class HumanBehaviorProfile:
    """Realistic human behavior patterns"""
    attention_span: float  # seconds
    scroll_frequency: float
    pause_probability: float
    seek_probability: float
    mouse_movement_pattern: str
    interaction_style: str
    
class AIBehaviorEngine:
    """
    Uses statistical models to generate indistinguishable human behavior
    """
    
    def __init__(self):
        self.behavior_profiles = self._generate_behavior_profiles()
        self.current_profile = None
        
    def _generate_behavior_profiles(self) -> List[HumanBehaviorProfile]:
        """Generate 50+ unique human behavior profiles"""
        profiles = []
        
        # Different viewer archetypes
        archetypes = [
            # Engaged viewer
            {"attention": (120, 300), "scroll": 0.2, "pause": 0.1, "seek": 0.05, "mouse": "active", "style": "engaged"},
            # Casual viewer
            {"attention": (30, 90), "scroll": 0.6, "pause": 0.3, "seek": 0.2, "mouse": "moderate", "style": "casual"},
            # Distracted viewer
            {"attention": (15, 45), "scroll": 0.8, "pause": 0.5, "seek": 0.4, "mouse": "erratic", "style": "distracted"},
            # Binge watcher
            {"attention": (300, 600), "scroll": 0.1, "pause": 0.05, "seek": 0.01, "mouse": "minimal", "style": "focused"},
            # Skimmer
            {"attention": (10, 30), "scroll": 0.9, "pause": 0.7, "seek": 0.6, "mouse": "rapid", "style": "skimming"},
        ]
        
        for archetype in archetypes:
            for _ in range(10):  # 10 variations per archetype
                profiles.append(HumanBehaviorProfile(
                    attention_span=np.random.uniform(*archetype["attention"]),
                    scroll_frequency=archetype["scroll"] * np.random.uniform(0.8, 1.2),
                    pause_probability=archetype["pause"] * np.random.uniform(0.8, 1.2),
                    seek_probability=archetype["seek"] * np.random.uniform(0.8, 1.2),
                    mouse_movement_pattern=archetype["mouse"],
                    interaction_style=archetype["style"]
                ))
        
        return profiles
    
    def select_behavior_profile(self) -> HumanBehaviorProfile:
        """Select a random behavior profile for this session"""
        self.current_profile = random.choice(self.behavior_profiles)
        return self.current_profile
    
    def generate_mouse_trajectory(self, start: Tuple[int, int], end: Tuple[int, int], 
                                num_points: int = None) -> List[Tuple[int, int]]:
        """
        Generate realistic mouse movement using Bezier curves
        Humans don't move mouse in straight lines
        """
        if num_points is None:
            num_points = random.randint(20, 50)
        
        # Add random control points for natural curve
        control_points = []
        control_points.append(start)
        
        # Add 1-3 random control points
        for _ in range(random.randint(1, 3)):
            cx = random.randint(min(start[0], end[0]), max(start[0], end[0]))
            cy = random.randint(min(start[1], end[1]), max(start[1], end[1]))
            control_points.append((cx, cy))
        
        control_points.append(end)
        
        # Generate Bezier curve
        trajectory = []
        for i in range(num_points):
            t = i / (num_points - 1)
            point = self._bezier_curve(control_points, t)
            trajectory.append(point)
        
        return trajectory
    
    def _bezier_curve(self, control_points: List[Tuple[int, int]], t: float) -> Tuple[int, int]:
        """Calculate point on Bezier curve"""
        n = len(control_points) - 1
        x = sum(self._binomial_coeff(n, i) * (1-t)**(n-i) * t**i * control_points[i][0] 
                for i in range(n+1))
        y = sum(self._binomial_coeff(n, i) * (1-t)**(n-i) * t**i * control_points[i][1] 
                for i in range(n+1))
        return (int(x), int(y))
    
    def _binomial_coeff(self, n: int, k: int) -> int:
        """Calculate binomial coefficient"""
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1
        result = 1
        for i in range(min(k, n - k)):
            result = result * (n - i) // (i + 1)
        return result
    
    def generate_viewing_pattern(self, video_duration: int) -> List[dict]:
        """
        Generate realistic viewing pattern with pauses, seeks, etc.
        Returns list of actions with timestamps
        """
        if not self.current_profile:
            self.select_behavior_profile()
        
        actions = []
        current_time = 0
        
        while current_time < video_duration:
            # Determine watch duration before next action
            watch_duration = np.random.exponential(self.current_profile.attention_span)
            watch_duration = min(watch_duration, video_duration - current_time)
            
            actions.append({
                'action': 'watch',
                'timestamp': current_time,
                'duration': watch_duration
            })
            
            current_time += watch_duration
            
            if current_time >= video_duration:
                break
            
            # Decide next action based on probabilities
            rand = random.random()
            
            if rand < self.current_profile.pause_probability:
                pause_duration = np.random.exponential(3) + 1  # 1-10 seconds typically
                actions.append({
                    'action': 'pause',
                    'timestamp': current_time,
                    'duration': pause_duration
                })
                current_time += pause_duration
                
            elif rand < (self.current_profile.pause_probability + self.current_profile.seek_probability):
                # Random seek (forward or backward)
                seek_target = random.randint(max(0, int(current_time - 30)), 
                                            min(video_duration, int(current_time + 60)))
                actions.append({
                    'action': 'seek',
                    'timestamp': current_time,
                    'seek_to': seek_target
                })
                current_time = seek_target
        
        return actions
    
    def generate_typing_pattern(self, text: str) -> List[Tuple[str, float]]:
        """
        Generate realistic typing pattern with varying speeds and mistakes
        Returns list of (character, delay) tuples
        """
        pattern = []
        
        for i, char in enumerate(text):
            # Base typing speed: 40-80 WPM (converted to char delay)
            base_delay = np.random.uniform(0.1, 0.25)
            
            # Add natural variations
            if char == ' ':
                base_delay *= 1.5  # Longer pause at spaces
            elif i > 0 and text[i-1] == ' ':
                base_delay *= 1.2  # Slight pause after space
            elif char.isupper():
                base_delay *= 1.1  # Shift key delay
            
            # Random thinking pauses
            if random.random() < 0.05:
                base_delay += np.random.uniform(0.5, 2.0)
            
            pattern.append((char, base_delay))
            
            # Simulate typos (5% chance)
            if random.random() < 0.05:
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                pattern.append((wrong_char, base_delay * 0.8))
                pattern.append(('\b', 0.15))  # Backspace
                pattern.append((char, base_delay))
        
        return pattern
    
    def calculate_engagement_score(self, actions: List[dict]) -> float:
        """
        Calculate engagement score that mimics real user
        DoodStream likely tracks this
        """
        total_watch_time = sum(a['duration'] for a in actions if a['action'] == 'watch')
        total_pauses = sum(1 for a in actions if a['action'] == 'pause')
        total_seeks = sum(1 for a in actions if a['action'] == 'seek')
        
        # Natural engagement score calculation
        engagement = (total_watch_time / 60) * 10  # Base score from watch time
        engagement -= total_pauses * 2  # Penalize too many pauses
        engagement -= total_seeks * 1.5  # Penalize excessive seeking
        
        return max(0, min(100, engagement))


class AdaptiveTiming:
    """
    Learns from successful views and adapts timing patterns
    Makes detection through statistical analysis nearly impossible
    """
    
    def __init__(self):
        self.successful_timings = []
        self.failed_timings = []
        
    def record_attempt(self, timing_data: dict, success: bool):
        """Record timing data from attempt"""
        if success:
            self.successful_timings.append(timing_data)
        else:
            self.failed_timings.append(timing_data)
    
    def get_optimal_delay(self) -> float:
        """Calculate optimal delay based on past success"""
        if len(self.successful_timings) < 10:
            # Not enough data, use random delay
            return np.random.uniform(120, 600)
        
        # Analyze successful timings
        delays = [t['inter_view_delay'] for t in self.successful_timings[-50:]]
        
        # Use normal distribution around successful mean
        mean_delay = np.mean(delays)
        std_delay = np.std(delays)
        
        # Generate new delay from learned distribution
        optimal = np.random.normal(mean_delay, std_delay)
        
        # Ensure within reasonable bounds
        return max(60, min(1800, optimal))
    
    def should_rotate_proxy(self) -> bool:
        """Decide if proxy should be rotated based on patterns"""
        if len(self.successful_timings) < 5:
            return True
        
        # Analyze recent success rate
        recent = self.successful_timings[-10:] + self.failed_timings[-10:]
        success_rate = len([t for t in recent if t in self.successful_timings]) / len(recent)
        
        # Rotate if success rate drops below 70%
        return success_rate < 0.7
