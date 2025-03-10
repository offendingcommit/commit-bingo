import random
import math
from pathlib import Path
from nicegui import ui
from typing import List, Optional, Literal
import colorsys
from config import config


class WheelSpinner:
    def __init__(self, options_file=None):
        # Use config for file name if not specified
        self.options_file = options_file or config['wheel'].OPTIONS_FILE
        self.options = self._load_options(self.options_file)
        
        # Get animation settings from config
        self.min_rotations = config['wheel'].MIN_ROTATIONS
        self.max_rotations = config['wheel'].MAX_ROTATIONS
        self.result: Optional[str] = None
        self.is_spinning = False
        self.rotation_angle = 0
        
        # Generate colors based on configured color mode
        self.color_mode = config['wheel'].COLOR_MODE
        self.colors = self._generate_colors(len(self.options))
        
        # Animation timers
        self.timer = None
        self.idle_timer = None
        
        # Animation settings from config
        self.spin_speed = 0
        self.max_speed = config['wheel'].MAX_SPEED
        self.prev_slice_index = -1  # To track when we cross a slice boundary
        self.idle_rotation_speed = config['wheel'].IDLE_ROTATION_SPEED
        self.frame_rate = config['wheel'].FRAME_RATE
        
    def _load_options(self, options_file) -> List[str]:
        path = Path(options_file)
        if path.exists():
            with open(path, 'r') as f:
                return [name.strip() for name in f.readlines() if name.strip()]
        return ["No options found"]
    
    def _generate_colors(self, count: int) -> List[str]:
        """Generate colors for wheel slices based on the configured color mode"""
        colors = []
        
        # RGB mode - generate colors using HSV color space
        if self.color_mode == 'RGB':
            for i in range(count):
                hue = i / count
                # Generate pastel colors with high saturation and value
                r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
                # Convert to hex format
                hex_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
                colors.append(hex_color)
                
        # Custom mode - alternate between predefined colors
        elif self.color_mode == 'CUSTOM':
            custom_colors = config['wheel'].CUSTOM_COLORS
            for i in range(count):
                # Cycle through the custom colors
                color_index = i % len(custom_colors)
                colors.append(custom_colors[color_index])
                
        # Fallback to RGB mode if invalid mode specified
        else:
            return self._generate_colors(count)
            
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
        if not self.options or self.is_spinning:
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
        slice_angle = 360 / len(self.options)
        
        # The final angle needs to point to a specific name
        # We first determine the final index, then calculate the exact angle needed
        self.final_index = random.randint(0, len(self.options) - 1)
        
        # Calculate the center angle for the final slice
        slice_center = self.final_index * slice_angle + slice_angle / 2
        
        # The marker is at the right side (90 degrees in our coordinate system)
        # So we need to rotate so the slice center is at the marker
        self.final_angle = self.total_rotation + (90 - slice_center)
        
        # Start with current rotation
        self.start_angle = self.rotation_angle % 360
        
        # Animation parameters from config
        self.spin_duration = config['wheel'].SPIN_DURATION
        self.elapsed_time = 0
        self.deceleration = config['wheel'].DECELERATION
        
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
        self.result = self.options[current_index]
        
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
        slice_angle = 360 / len(self.options)
        index = int(relative_angle / slice_angle)
        
        # Ensure index is within bounds
        return index % len(self.options)

@ui.page('/')
def index():
    spinner = WheelSpinner()
    
    with ui.card().classes('w-full max-w-2xl mx-auto'):
        ui.label(config['server'].TITLE).classes('text-3xl mx-auto text-center')
        
        # Create SVG for the wheel
        ui.element('div').classes('relative mx-auto')
        
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
                font-size: {config['wheel'].TEXT_SIZE}px;
                text-anchor: end; /* Right-align text */
                dominant-baseline: middle;
                font-weight: {config['wheel'].TEXT_WEIGHT};
            }}
        </style>
        ''')
        with ui.row().classes("w-full") as wheel:
            # Create the basic SVG structure
            with ui.element('div').classes('relative w-full h-full'):
                with ui.element('svg').classes('w-full h-full').props('viewBox="0 0 100 100"'):
                    # Group for the wheel (will be centered and rotated)
                    with ui.element('g').props(f'id="{wheel_id}" transform="translate(50, 50)"'):
                        # We'll add slices with JavaScript
                        pass
                    
                # Marker icon pointing to the winning slice (at 90 degrees - right side)
                with ui.element('g').props(f'id="{marker_id}"'):
                    ui.icon(config['wheel'].MARKER_ICON, size=config['wheel'].MARKER_SIZE).style(
                        f'color: {config["wheel"].MARKER_COLOR}; position: absolute; right: -36px; top: 50%; transform: translateY(-50%);'
                    )
        
        
        
        # Result display
        result_display = ui.label('Click Spin to start').classes('w-full text-xl text-center p-2 my-2 border rounded')
        
        # Create the wheel slices
        def create_wheel_slices():
            # Get configuration values for JavaScript
            text_distance_factor = config['wheel'].TEXT_DISTANCE_FACTOR
            slice_stroke_color = config['wheel'].SLICE_STROKE_COLOR
            slice_stroke_width = config['wheel'].SLICE_STROKE_WIDTH
            text_contrast = config['wheel'].TEXT_CONTRAST
            
            ui.run_javascript(f'''
            (() => {{
                const wheel = document.getElementById('{wheel_id}');
                wheel.innerHTML = '';  // Clear existing slices
                
                // Function to calculate optimal text color shade for maximum readability
                function calculateOptimalTextColor(bgColor) {{
                    // Convert hex to RGB
                    let hex = bgColor.charAt(0) === '#' ? bgColor.substring(1, 7) : bgColor;
                    let r = parseInt(hex.substring(0, 2), 16);
                    let g = parseInt(hex.substring(2, 4), 16);
                    let b = parseInt(hex.substring(4, 6), 16);
                    
                    // Calculate perceptive luminance (YIQ equation)
                    // This accounts for human perception of brightness
                    let luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
                    
                    // Calculate the optimal grayscale value for contrast
                    // The farther from background luminance, the better the contrast
                    // We want at least a contrast ratio of 4.5:1 for WCAG AA compliance
                    
                    // For best contrast:
                    // - If background is darker than mid-gray, use a lighter shade
                    // - If background is lighter than mid-gray, use a darker shade
                    // - The intensity depends on how far from mid-gray the background is
                    
                    // Calculate the "opposite" luminance value
                    let targetLuminance;
                    if (luminance < 0.5) {{
                        // Dark background, find light text 
                        // Scale using the configurable contrast value
                        targetLuminance = Math.min(1.0, luminance + textContrast);
                    }} else {{
                        // Light background, find dark text
                        // Scale using the configurable contrast value
                        targetLuminance = Math.max(0.0, luminance - textContrast);
                    }}
                    
                    // Apply some additional correction to improve contrast
                    // Ensure the difference meets minimum WCAG AA standards
                    if (Math.abs(targetLuminance - luminance) < textContrast) {{
                        targetLuminance = luminance < 0.5 ? 1.0 : 0.0;
                    }}
                    
                    // Convert luminance back to grayscale color
                    const value = Math.round(targetLuminance * 255);
                    return `rgb(${{value}}, ${{value}}, ${{value}})`;
                }}
                
                const options = {spinner.options};
                const colors = {spinner.colors};
                const sliceCount = options.length;
                const sliceAngle = 360 / sliceCount;
                
                // Configuration values
                const textDistanceFactor = {text_distance_factor};  // How far text is from center (0-1)
                const strokeColor = '{slice_stroke_color}';
                const strokeWidth = {slice_stroke_width};
                const textContrast = {text_contrast};  // Contrast adjustment (higher = more contrast)
                
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
                    slice.setAttribute("stroke", strokeColor);
                    slice.setAttribute("stroke-width", strokeWidth);
                    slice.setAttribute("class", "wheel-slice");
                    wheel.appendChild(slice);
                    
                    // Calculate position for text - use textDistanceFactor to position text closer to edge
                    const textAngle = startAngle + sliceAngle / 2;
                    const textRad = textAngle * Math.PI / 180;
                    
                    // Text distance is now controlled by the config factor (closer to 1 = closer to edge)
                    const wheelRadius = 50;
                    const textDistance = wheelRadius * textDistanceFactor;
                    const textX = textDistance * Math.sin(textRad);
                    const textY = -textDistance * Math.cos(textRad);
                    
                    // Calculate the inner height of the slice at this distance from center
                    // The height is approximately the arc length at this radius
                    const sliceInnerHeight = 2 * Math.PI * textDistance * (sliceAngle / 360);
                    
                    // Estimate how many characters will fit in the slice height
                    // SVG text size is roughly proportional to the number of characters that fit vertically
                    // Get font size and character aspect ratio from config
                    const fontSizeInPx = {config['wheel'].TEXT_SIZE};
                    const charAspectRatio = {config['wheel'].TEXT_CHAR_RATIO}; // width/height ratio of typical character
                    const effectiveCharHeight = fontSizeInPx;
                    const estimatedMaxChars = Math.floor(sliceInnerHeight / (effectiveCharHeight * charAspectRatio));
                    
                    // Prepare text content - truncate with ellipsis if needed
                    let displayText = options[i];
                    if (displayText.length > estimatedMaxChars && estimatedMaxChars > 3) {{
                        displayText = displayText.substring(0, estimatedMaxChars - 3) + '...';
                    }}
                    
                    // Make text radial (point toward center)
                    // For right-aligned text, adjust the rotation
                    const textRotate = textAngle + 270;  // Perpendicular to the radius
                    
                    // Calculate optimal text color (black or white) based on background color
                    let textColor = calculateOptimalTextColor(colors[i]);
                    
                    console.log(textColor)
                    
                    // Add text
                    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                    text.setAttribute("x", textX);
                    text.setAttribute("y", textY);
                    text.setAttribute("transform", `rotate(${{textRotate}}, ${{textX}}, ${{textY}})`);
                    text.setAttribute("class", "wheel-slice-text");
                    text.setAttribute("fill", textColor); // Use calculated text color
                    text.textContent = displayText;
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
                if not spinner.options:
                    ui.notify('No options loaded', color='negative')
                    return
                
                # Start the animated spin with timer
                spinner.start_spin(update_wheel_rotation, result_display, spin_button)
            
            spin_button = ui.button('Spin', icon='casino', on_click=handle_spin)
        
            reload_button = ui.button('Reload options', icon='refresh', on_click=lambda: ui.navigate.to('/reload'))
            
        wheel.on("click", handle_spin)

@ui.page('/reload')
def reload_page():
    options_file = config['wheel'].OPTIONS_FILE
    
    def save_options(options):
        with open(options_file, 'w') as f:
            f.write('\n'.join(options))
        ui.notify('Options saved successfully', color='positive')
        ui.navigate.to('/')
    
    with ui.card().classes('w-full max-w-md mx-auto'):
        ui.label('Edit Options').classes('text-2xl text-center')
        
        # Load current options
        options = []
        try:
            with open(options_file, 'r') as f:
                options = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            pass
        
        # Text area for editing options
        options_area = ui.textarea('options (one per line)', value='\n'.join(options)).classes('w-full')
        
        with ui.row().classes('w-full justify-end'):
            ui.button('Cancel', on_click=lambda: ui.navigate.to('/'))
            ui.button('Save', on_click=lambda: save_options(options_area.value.split('\n')))

ui.run(title=config['server'].TITLE, port=config['server'].PORT)
