# Spinner Project Context

## Project Overview
The Spinner is a wheel-based random selector built with Python and NiceGUI. It displays a colorful wheel divided into slices, each containing an option from a provided list. When spun, it randomly selects one option with an animated rotation.

## Current Features
- Interactive spinning wheel with continuous idle rotation
- Two-phase spinning animation (acceleration + deceleration)
- Marker on the right side indicating the selected option
- Audio feedback (tick sounds) when crossing slice boundaries
- Customizable options through text file
- Environment-based configuration system
- Multiple color themes support

## Configuration System
- All settings can be adjusted through:
  1. Environment variables
  2. Direct modification of `config.py`
- Two color modes available:
  - `RGB`: Generates colors across the spectrum based on HSV color space
  - `CUSTOM`: Alternates between predefined hex color values

## Technical Implementation Details
### Wheel Animation
- Continuous idle rotation when not actively spinning
- Acceleration phase: First 20% of animation duration
- Deceleration phase: Last 80% of animation duration
- Total animation duration: Configurable (default 10 seconds)
- Frame rate: Configurable (default 60fps)

### Text Rendering
- Text positioned along radial lines
- Right-aligned text for better visibility at wheel edge
- Automatic truncation with ellipsis when text would be too tall for the slice
- Text size and character ratio are configurable

### UI Components
- Main wheel with slices and option labels
- Marker icon (configurable NiceGUI icon)
- Result display showing the selected option
- Control buttons (Spin, Reload options)

### Data Storage
- Options stored in a text file (default: options.txt)
- One option per line
- UI for editing options

## Implemented Enhancements
1. **NiceGUI Icon Marker**: Replaced SVG triangle with configurable NiceGUI icon
2. **Configuration System**: Created `config.py` with environment variable support
3. **Color Modes**: Added RGB and custom color palette options
4. **Text Improvements**:
   - Right-aligned text for better visibility
   - Text truncation with ellipsis for tall slices
   - Automatic text color adjustment for optimal contrast with background
5. **Accessibility**: 
   - Optimal text contrast with dynamic grayscale shading based on background color
   - Configurable contrast ratio to meet WCAG AA standards
   - Enhanced readability for people with color blindness or low vision
   - Perceptual luminance algorithm accounts for human perception of brightness
6. **Click Handling**: Added ability to click anywhere on wheel to spin