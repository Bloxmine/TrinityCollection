#!/bin/bash

# TrinityCollection SuperKaramba Widgets Installation Script
# Compatible with Trinity Desktop Environment

echo "=== TrinityCollection SuperKaramba Widgets Installer ==="
echo ""

# Check if running Trinity Desktop
if [ -z "$TDE_FULL_SESSION" ] && [ -z "$KDE_FULL_SESSION" ]; then
    echo "Warning: Trinity Desktop Environment not detected."
    echo "These widgets are designed for Trinity Desktop (TDE)."
    echo ""
fi

# Define installation directory
INSTALL_DIR="$HOME/.trinity/share/apps/superkaramba"
if [ ! -d "$HOME/.trinity" ]; then
    # Fallback to KDE directory if Trinity not found
    INSTALL_DIR="$HOME/.kde/share/apps/superkaramba"
fi

# Create installation directory if it doesn't exist
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Creating SuperKaramba directory: $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
fi

# Function to install widget category
install_category() {
    local category=$1
    local description=$2
    
    if [ -d "$category" ]; then
        echo "Installing $description..."
        cp -r "$category" "$INSTALL_DIR/"
        echo "  ✓ $description installed"
    else
        echo "  ✗ $description directory not found"
    fi
}

echo "Installing widgets to: $INSTALL_DIR"
echo ""

# Install each category
install_category "system-monitors" "System Monitor Widgets"
install_category "clocks" "Clock Widgets"  
install_category "weather" "Weather Widget"
install_category "misc-widgets" "Miscellaneous Widgets"

echo ""
echo "Installation completed!"
echo ""

# Check if SuperKaramba is available
if command -v superkaramba >/dev/null 2>&1; then
    echo "SuperKaramba found in PATH."
    echo "You can now start widgets through the SuperKaramba application."
elif [ -f "/opt/trinity/bin/superkaramba" ]; then
    echo "Trinity SuperKaramba found at /opt/trinity/bin/superkaramba"
elif [ -f "/usr/bin/superkaramba" ]; then
    echo "SuperKaramba found at /usr/bin/superkaramba"  
else
    echo "Warning: SuperKaramba not found in common locations."
    echo "Please ensure SuperKaramba is installed with your Trinity Desktop."
fi

echo ""
echo "To use the widgets:"
echo "1. Open SuperKaramba (usually in Trinity's Utilities menu)"
echo "2. Click 'Open Theme' and browse to the installed widget folders"
echo "3. Select the .theme file for the widget you want to use"
echo "4. The widget will appear on your desktop"
echo ""

# Offer to create desktop shortcuts
read -p "Create desktop shortcuts for easy widget access? (y/n): " create_shortcuts

if [ "$create_shortcuts" = "y" ] || [ "$create_shortcuts" = "Y" ]; then
    DESKTOP_DIR="$HOME/Desktop"
    
    if [ ! -d "$DESKTOP_DIR" ]; then
        mkdir -p "$DESKTOP_DIR"
    fi
    
    # Create shortcuts for each main widget
    create_shortcut() {
        local widget_name=$1
        local widget_path=$2
        local widget_desc=$3
        
        cat > "$DESKTOP_DIR/$widget_name.desktop" << EOF
[Desktop Entry]
Name=$widget_desc
Comment=SuperKaramba Widget - $widget_desc
Exec=superkaramba "$INSTALL_DIR/$widget_path"
Icon=superkaramba
Type=Application
Categories=Utility;
EOF
        chmod +x "$DESKTOP_DIR/$widget_name.desktop"
        echo "  ✓ Created shortcut: $widget_desc"
    }
    
    echo ""
    echo "Creating desktop shortcuts..."
    
    # Create shortcuts for key widgets
    if [ -f "$INSTALL_DIR/system-monitors/cpu-monitor.theme" ]; then
        create_shortcut "cpu-monitor" "system-monitors/cpu-monitor.theme" "CPU Monitor"
    fi
    
    if [ -f "$INSTALL_DIR/system-monitors/memory-monitor.theme" ]; then
        create_shortcut "memory-monitor" "system-monitors/memory-monitor.theme" "Memory Monitor"
    fi
    
    if [ -f "$INSTALL_DIR/clocks/digital-clock.theme" ]; then
        create_shortcut "digital-clock" "clocks/digital-clock.theme" "Digital Clock"
    fi
    
    if [ -f "$INSTALL_DIR/weather/weather-widget.theme" ]; then
        create_shortcut "weather-widget" "weather/weather-widget.theme" "Weather Widget"
    fi
    
    echo "Desktop shortcuts created!"
fi

echo ""
echo "Installation complete! Enjoy your new SuperKaramba widgets!"
echo ""
echo "For configuration help, see CONFIGURATION.md"
echo "For more information, see README.md"