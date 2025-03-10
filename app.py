import random
import math
from pathlib import Path
from nicegui import ui
from typing import List, Optional
import colorsys


class WheelSpinner:
    def __init__(self, names_file='names.txt'):
        self.names = self._load_names(names_file)
        self.min_rotations = 5
        self.max_rotations = 8
        self.result: Optional[str] = None
        self.is_spinning = False
        self.rotation_angle = 0
        self.colors = self._generate_colors(len(self.names))
        self.timer = None
        self.idle_timer = None
        self.spin_speed = 0
        self.max_speed = 30
        self.prev_slice_index = -1  # To track when we cross a slice boundary
        self.idle_rotation_speed = 5  # Degrees per second for idle rotation
        self.frame_rate = 60  # Animation frame rate
        
    def _load_names(self, names_file) -> List[str]:
        path = Path(names_file)
        if path.exists():
            with open(path, 'r') as f:
                return [name.strip() for name in f.readlines() if name.strip()]
        return ["No names found"]
    
    def _generate_colors(self, count: int) -> List[str]:
        """Generate visually distinct colors for the wheel slices"""
        colors = []
        for i in range(count):
            hue = i / count
            # Generate pastel colors with high saturation and value
            r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
            # Convert to hex format
            hex_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            colors.append(hex_color)
        return colors
    
    def start_idle_rotation(self, update_wheel_rotation):
        """Start a slow idle rotation of the wheel"""
        if self.idle_timer is not None:
            return
            
        self.update_wheel_rotation = update_wheel_rotation
        # Use the same frame rate for consistency
        self.idle_timer = ui.timer(1/self.frame_rate, self._update_idle_animation)
        
    def _update_idle_animation(self):
        """Handle the slow idle rotation animation"""
        if self.is_spinning:
            return
            
        # Rotate slowly (degrees per frame)
        self.rotation_angle += self.idle_rotation_speed / self.frame_rate
        # Don't take modulo 360 here, to avoid jumps in rotation
        self.update_wheel_rotation(self.rotation_angle)
    
    def start_spin(self, update_wheel_rotation, result_display, spin_button):
        """
        Start spinning the wheel using a timer for animation.
        """
        if not self.names or self.is_spinning:
            return
            
        # If idle animation is running, stop it during the spin
        if self.idle_timer:
            self.idle_timer.cancel()
            self.idle_timer = None
            
        self.is_spinning = True
        spin_button.disable()
        
        # Determine how far to spin (in degrees)
        rotations = random.uniform(self.min_rotations, self.max_rotations)
        self.total_rotation = rotations * 360
        
        # Calculate the final position
        slice_angle = 360 / len(self.names)
        
        # The final angle needs to point to a specific name
        # We first determine the final index, then calculate the exact angle needed
        self.final_index = random.randint(0, len(self.names) - 1)
        
        # Calculate the center angle for the final slice
        slice_center = self.final_index * slice_angle + slice_angle / 2
        
        # The marker is at the right side (90 degrees in our coordinate system)
        # So we need to rotate so the slice center is at the marker
        self.final_angle = self.total_rotation + (90 - slice_center)
        
        # Start with current rotation
        self.start_angle = self.rotation_angle % 360
        
        # Animation parameters
        self.spin_duration = 10.0  # total time in seconds
        self.elapsed_time = 0
        self.deceleration = 3  # Higher values mean faster deceleration
        
        # Reset previous slice for tick sound
        self.prev_slice_index = -1
        
        # Store callback functions
        self.update_wheel_rotation = update_wheel_rotation
        self.result_display = result_display
        self.spin_button = spin_button
        
        # Start the animation timer
        self.timer = ui.timer(1/self.frame_rate, self._update_spin_animation)
        
    def _update_spin_animation(self):
        """Handle each animation frame during spinning"""
        if not self.is_spinning:
            return
            
        # Increment time
        self.elapsed_time += 1/self.frame_rate
        
        # Calculate progress (0 to 1)
        progress = min(1.0, self.elapsed_time / self.spin_duration)
        
        # Apply easing function (ease-out cubic)
        # This makes the wheel start fast and gradually slow down
        # First 20% of animation: acceleration
        # Last 80% of animation: deceleration
        if progress < 0.2:
            # Accelerate (0-0.2 mapped to 0-1)
            t_accel = progress * 5  # Scale 0-0.2 to 0-1
            # Ease-in function (start slow, then accelerate)
            speed_factor = t_accel * t_accel
            # Calculate angle based on acceleration
            angle_delta = speed_factor * (self.final_angle * 0.2)
            current_angle = self.start_angle + angle_delta
        else:
            # Decelerate (0.2-1 mapped to 0-1)
            t_decel = (progress - 0.2) / 0.8  # Scale 0.2-1 to 0-1
            # Ease-out function (start fast, then decelerate)
            t_eased = 1 - math.pow(1 - t_decel, self.deceleration)
            # Start from 20% of total rotation, go to 100%
            angle_delta = (self.final_angle * 0.2) + t_eased * (self.final_angle * 0.8)
            current_angle = self.start_angle + angle_delta
        
        # Update the wheel position
        self.rotation_angle = current_angle
        
        # Update UI - don't use modulo 360 to avoid jumps
        self.update_wheel_rotation(current_angle)
        
        # Get the current selected name based on the angle
        current_index = self._get_index_from_angle(current_angle)
        self.result = self.names[current_index]
        
        # Check if we crossed a slice boundary for tick sound
        if current_index != self.prev_slice_index:
            self.play_tick_sound()
            self.prev_slice_index = current_index
        
        # Check if animation is complete
        if progress >= 1.0:
            # Stop the timer
            self.timer.cancel()
            self.timer = None
            
            # Set final result
            self.is_spinning = False
            self.result_display.set_text(f"Selected: {self.result}")
            ui.notify(f"Selected: {self.result}", color="positive")
            self.spin_button.enable()
            
            # Restart idle animation
            self.start_idle_rotation(self.update_wheel_rotation)
            
    def play_tick_sound(self):
        """Play a tick sound when crossing a slice boundary"""
        # Add JavaScript to play a tick sound
        ui.run_javascript('''
        const audio = new Audio("data:audio/mp3;base64,//uQxAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAAFAAAGUACFhYWFhYWFhYWFhYWFhYWFhYWFvb29vb29vb29vb29vb29vb29vb3r6+vr6+vr6+vr6+vr6+vr6+vr6/////////////////////////////////8AAAA8TEFNRTMuOTlyAm4AAAAALgkAABRGJAKTQgAARgABllTUjPJjAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//sQxAADwAABpAAAACAAADSAAAAETEFNRTMuOTkuNVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVU=");
        audio.play();
        ''')
        
    def spin(self):
        """Legacy generator method - no longer used"""
        pass
    
    def _get_index_from_angle(self, angle: float) -> int:
        """
        Determine which slice (name index) is at the marker position given the wheel's rotation angle.
        The marker is at the right side (90 degrees in our coordinate system).
        """
        # Normalize angle to 0-360
        normalized_angle = angle % 360
        
        # The marker is at the right (90 degrees)
        marker_angle = 90
        
        # Calculate the angle relative to the marker (in the wheel's reference frame)
        relative_angle = (marker_angle - normalized_angle) % 360
        
        # Determine which slice this angle falls into
        slice_angle = 360 / len(self.names)
        index = int(relative_angle / slice_angle)
        
        # Ensure index is within bounds
        return index % len(self.names)

@ui.page('/')
def index():
    spinner = WheelSpinner()
    
    with ui.card().classes('w-full max-w-lg mx-auto'):
        ui.label('Name Spinner').classes('text-2xl text-center')
        
        # Create SVG for the wheel
        ui.element('div').classes('relative mx-auto my-4 w-80 h-80')
        
        # We'll use client-side JS to manage the wheel since NiceGUI's HTML handling has changed
        wheel_id = 'wheel-' + str(random.randint(10000, 99999))
        marker_id = 'marker-' + str(random.randint(10000, 99999))
        
        # Create the wheel with JavaScript
        ui.add_head_html(f'''
        <style>
            #{wheel_id} {{
                transition: transform 0.1s ease-out;
            }}
            .wheel-slice-text {{
                font-size: 4px;
                fill: black;
                text-anchor: middle;
                dominant-baseline: middle;
                font-weight: bold;
            }}
            #{marker_id} {{
                fill: red;
                position: absolute;
                top: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 20px;
                height: 10px;
            }}
        </style>
        ''')
        
        # Create the basic SVG structure
        with ui.element('div').classes('relative w-full h-full'):
            with ui.element('svg').classes('w-full h-full').props('viewBox="0 0 100 100"'):
                # Group for the wheel (will be centered and rotated)
                with ui.element('g').props(f'id="{wheel_id}" transform="translate(50, 50)"'):
                    # We'll add slices with JavaScript
                    pass
                
                # Marker triangle pointing to the winning slice (at 90 degrees - right side)
                ui.html(f'<path id="{marker_id}" d="M 95 50 L 100 55 L 100 45 Z" fill="red" />')
        
        # Result display
        result_display = ui.label('Click Spin to start').classes('text-xl text-center p-2 my-2 border rounded')
        
        # Create the wheel slices
        def create_wheel_slices():
            ui.run_javascript(f'''
            (() => {{
                const wheel = document.getElementById('{wheel_id}');
                wheel.innerHTML = '';  // Clear existing slices
                
                const names = {spinner.names};
                const colors = {spinner.colors};
                const sliceCount = names.length;
                const sliceAngle = 360 / sliceCount;
                
                for (let i = 0; i < sliceCount; i++) {{
                    // Calculate angles for this slice
                    const startAngle = i * sliceAngle;
                    const endAngle = (i + 1) * sliceAngle;
                    
                    // Convert to radians
                    const startRad = startAngle * Math.PI / 180;
                    const endRad = endAngle * Math.PI / 180;
                    
                    // Calculate points for slice path
                    const x1 = 50 * Math.sin(startRad);
                    const y1 = -50 * Math.cos(startRad);
                    const x2 = 50 * Math.sin(endRad);
                    const y2 = -50 * Math.cos(endRad);
                    
                    // Create arc path
                    const largeArc = sliceAngle > 180 ? 1 : 0;
                    const path = `M 0 0 L ${{x1}} ${{y1}} A 50 50 0 ${{largeArc}} 1 ${{x2}} ${{y2}} Z`;
                    
                    // Create slice
                    const slice = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    slice.setAttribute("d", path);
                    slice.setAttribute("fill", colors[i]);
                    slice.setAttribute("stroke", "white");
                    slice.setAttribute("stroke-width", "0.5");
                    slice.setAttribute("class", "wheel-slice");
                    wheel.appendChild(slice);
                    
                    // Calculate position for text
                    const textAngle = startAngle + sliceAngle / 2;
                    const textRad = textAngle * Math.PI / 180;
                    const textDistance = 30;  // Moved in a little for better visibility
                    const textX = textDistance * Math.sin(textRad);
                    const textY = -textDistance * Math.cos(textRad);
                    
                    // Make text radial (point toward center)
                    // For radial text, we want text to be perpendicular to the radius
                    const textRotate = textAngle + 270;  // Perpendicular to the radius
                    
                    // Add text
                    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                    text.setAttribute("x", textX);
                    text.setAttribute("y", textY);
                    text.setAttribute("transform", `rotate(${{textRotate}}, ${{textX}}, ${{textY}})`);
                    text.setAttribute("class", "wheel-slice-text");
                    text.textContent = names[i];
                    wheel.appendChild(text);
                }}
            }})();
            ''')
        
        # Create initial wheel
        create_wheel_slices()
        
        # Function to update wheel rotation
        def update_wheel_rotation(angle):
            # Use the actual angle value rather than taking modulo 360
            # This ensures continuous rotation without resets
            ui.run_javascript(f'''
            document.getElementById('{wheel_id}').setAttribute('transform', 'translate(50, 50) rotate({angle})');
            ''')
            
        # Start idle rotation animation
        spinner.start_idle_rotation(update_wheel_rotation)
        
        # Control panel
        with ui.row().classes('w-full justify-center'):
            def handle_spin():
                if not spinner.names:
                    ui.notify('No names loaded', color='negative')
                    return
                
                # Start the animated spin with timer
                spinner.start_spin(update_wheel_rotation, result_display, spin_button)
            
            spin_button = ui.button('Spin', icon='casino', on_click=handle_spin)
        
        # Option to reload names
        with ui.row().classes('w-full justify-center mt-4'):
            ui.button('Reload Names', icon='refresh', on_click=lambda: ui.navigate.to('/reload'))

@ui.page('/reload')
def reload_page():
    def save_names(names):
        with open('names.txt', 'w') as f:
            f.write('\n'.join(names))
        ui.notify('Names saved successfully', color='positive')
        ui.navigate.to('/')
    
    with ui.card().classes('w-full max-w-md mx-auto'):
        ui.label('Edit Names').classes('text-2xl text-center')
        
        # Load current names
        names = []
        try:
            with open('names.txt', 'r') as f:
                names = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            pass
        
        # Text area for editing names
        names_area = ui.textarea('Names (one per line)', value='\n'.join(names)).classes('w-full')
        
        with ui.row().classes('w-full justify-end'):
            ui.button('Cancel', on_click=lambda: ui.navigate.to('/'))
            ui.button('Save', on_click=lambda: save_names(names_area.value.split('\n')))

ui.run(title='Name Spinner', port=8080)
