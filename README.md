# TrinityCollection
Collection of Trinity Desktop (KDE3.5) themes and SuperKaramba widgets

A comprehensive collection of SuperKaramba widgets designed for Trinity Desktop Environment (TDE), the continuation of KDE 3.5.

## Widgets Included

### System Monitors
- **CPU Monitor** (`system-monitors/cpu-monitor.*`) - Real-time CPU usage display with load average
- **Memory Monitor** (`system-monitors/memory-monitor.*`) - RAM and swap usage with visual bars
- **Network Monitor** (`system-monitors/network-monitor.*`) - Network interface speed and data transfer statistics
- **Disk Usage** (`misc-widgets/disk-usage.*`) - Filesystem usage monitor for root and home partitions

### Clocks
- **Digital Clock** (`clocks/digital-clock.*`) - Customizable digital time display with date
- **Analog Clock** (`clocks/analog-clock.*`) - Traditional analog clock with hour, minute, and second hands

### Weather
- **Weather Widget** (`weather/weather-widget.*`) - Weather information display (demo version with simulated data)

### System Information & Utilities
- **System Info** (`misc-widgets/system-info.*`) - System details including hostname, kernel, uptime, and more
- **Temperature Monitor** (`misc-widgets/temperature-monitor.*`) - CPU temperature monitoring with thermal warnings
- **Battery Monitor** (`misc-widgets/battery-monitor.*`) - Battery status and charging information for laptops
- **Calendar Widget** (`misc-widgets/calendar-widget.*`) - Monthly calendar with current date highlighting

## Quick Installation

Run the installation script to automatically install widgets:
```bash
chmod +x install.sh
./install.sh
```

## Manual Installation

1. Copy the widget folder(s) you want to your SuperKaramba widgets directory
2. Open SuperKaramba (usually found in Trinity's utilities menu)
3. Click "Open Theme" and navigate to the `.theme` file
4. The widget will appear on your desktop

## Widget Features

### Interactive Elements
- **Click widgets** to refresh data or toggle display modes
- **CPU Monitor**: Shows real-time usage with colored progress bar
- **Memory Monitor**: Displays RAM and swap usage separately
- **Digital Clock**: Click to toggle between 12/24 hour format
- **Weather Widget**: Click to toggle Celsius/Fahrenheit, right-click to refresh

## Configuration

See `CONFIGURATION.md` for detailed customization options including:
- Colors, fonts, and positioning
- Update intervals and data sources  
- Creating custom widgets
- Troubleshooting guide
Each widget can be customized by editing the `.theme` file for:
- Position (x, y coordinates)
- Colors and fonts
- Update intervals
- Widget size

See `CONFIGURATION.md` for detailed customization instructions.

### Python Scripts
The `.py` files contain the logic for each widget and can be modified to:
- Change data sources
- Modify display formatting
- Add new features
- Adjust update frequencies

## Requirements
- Trinity Desktop Environment (TDE)
- SuperKaramba (included with TDE)
- Python 2.x (for script functionality)
- Linux system with /proc filesystem access

## Notes
- Weather widget uses simulated data for demonstration
- For real weather data, integrate with a weather API service
- All widgets are designed to be lightweight and efficient
- Compatible with KDE 3.5 SuperKaramba format

## License
These widgets are provided as-is for the Trinity Desktop community.

## Contributing
Feel free to submit improvements, bug fixes, or new widget designs!
