# SuperKaramba Widget Configuration Guide

This guide explains how to customize and configure the TrinityCollection SuperKaramba widgets.

## Basic Configuration

### Positioning Widgets
Each `.theme` file contains position settings:
```
x: 50          # X coordinate on screen
y: 50          # Y coordinate on screen  
w: 200         # Widget width
h: 120         # Widget height
```

### Widget Behavior
```
layer: onbottom    # Widget layer (onbottom, normal, ontop)
hidden: false      # Start hidden (true/false)
locked: false      # Lock position (true/false)
ontop: false       # Always on top (true/false)
sticky: false      # Show on all desktops (true/false)
interval: 1000     # Update interval in milliseconds
```

## Color Customization

### Text Colors
Colors are specified as RGB values (0-255):
```
color: 255,255,255    # White text
color: 255,0,0        # Red text
color: 0,255,0        # Green text
color: 0,0,255        # Blue text
```

### Bar Colors
Progress bars can be customized:
```
bar {
    color: 0,255,0    # Green bar
    # or
    color: 255,150,0  # Orange bar
}
```

## Font Settings

### Font Configuration
```
font: Arial           # Font family
fontsize: 14         # Font size in points
shadow: 1            # Text shadow (0=none, 1=light, 2=heavy)
```

### Text Alignment
```
alignment: left      # left, center, right
```

## Widget-Specific Customizations

### CPU Monitor
Edit `cpu-monitor.py` to change:
- Update frequency (default: every second)
- CPU cores to monitor
- Warning thresholds

### Memory Monitor  
Edit `memory-monitor.py` to customize:
- Memory calculation method
- Display units (MB/GB)
- Swap monitoring

### Network Monitor
Edit `network-monitor.py` to modify:
- Default network interface
- Speed calculation method
- Data unit formatting

### Digital Clock
Edit `digital-clock.py` to change:
- Default time format (12/24 hour)
- Date format
- Time zone handling

### Weather Widget
Edit `weather-widget.py` to configure:
- Default city/location
- Temperature units (C/F)
- Update interval
- Weather data source (currently simulated)

## Advanced Configuration

### Python Script Modifications

#### Adding New Display Elements
In the `.theme` file, add new text or bar elements:
```
text {
    x: 10
    y: 100
    w: 180
    h: 15
    font: Arial
    fontsize: 11
    color: 200,200,200
    value: "New Element"
    name: new_element
}
```

Then update the Python script to control it:
```python
karamba.changeText(widget, "new_element", "Updated text")
```

#### Changing Update Intervals
Modify the `interval` value in `.theme` files:
- 1000 = 1 second
- 5000 = 5 seconds  
- 60000 = 1 minute
- 300000 = 5 minutes

#### Custom Data Sources
Replace the data collection functions in Python scripts:
```python
def getCustomData():
    # Your custom data collection logic
    return data

def widgetUpdated(widget):
    data = getCustomData()
    karamba.changeText(widget, "display_element", str(data))
```

## Troubleshooting

### Widget Won't Start
1. Check file permissions (should be readable)
2. Verify Python script syntax
3. Check SuperKaramba error console

### No Data Displayed
1. Ensure required system files exist (`/proc/*`)
2. Check file permissions for system monitoring
3. Verify Python script logic

### Performance Issues
1. Increase update intervals
2. Reduce number of active widgets
3. Simplify data collection logic

### Color/Font Issues
1. Verify color values are 0-255
2. Check if fonts are installed on system
3. Test with basic fonts (Arial, sans-serif)

## Creating New Widgets

### Basic Template
1. Create `.theme` file with layout
2. Create `.py` file with logic
3. Implement required functions:
   - `initWidget(widget)`
   - `widgetUpdated(widget)` 
   - `widgetClicked(widget, x, y, button)`

### Example Skeleton
```python
import karamba

def initWidget(widget):
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    # Update widget data
    karamba.changeText(widget, "text_element", "New value")

def widgetClicked(widget, x, y, button):
    # Handle clicks
    pass
```

## Tips and Best Practices

1. **Test incrementally** - Make small changes and test
2. **Use descriptive names** - Name elements clearly in .theme files
3. **Handle errors gracefully** - Wrap data collection in try/except
4. **Consider performance** - Don't update too frequently
5. **Follow KDE conventions** - Use familiar colors and layouts
6. **Document changes** - Comment your modifications

## Integration with Trinity Desktop

### Autostart Widgets
1. Copy widget folders to `~/.trinity/share/apps/superkaramba/`
2. Add to Trinity autostart via Control Center
3. Or create desktop shortcuts

### Theme Integration
- Use Trinity color schemes in widget colors
- Match desktop wallpaper colors
- Consider screen resolution and widget placement