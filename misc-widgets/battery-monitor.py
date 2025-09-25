#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Battery Monitor SuperKaramba Widget
#  Shows battery status and charging information
#  Compatible with Trinity Desktop / KDE 3.5

import karamba
import time
import os
import glob

def initWidget(widget):
    """Initialize the widget"""
    updateBatteryStatus(widget)
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called periodically to update battery status"""
    updateBatteryStatus(widget)

def updateBatteryStatus(widget):
    """Update battery status display"""
    try:
        battery_info = getBatteryInfo()
        
        if battery_info:
            # Update battery percentage
            percentage = battery_info['percentage']
            status = battery_info['status']
            
            # Choose appropriate battery icon and status text
            if status == 'Charging':
                icon = "🔌"
                status_text = "%s %d%% Charging" % (icon, percentage)
                power_text = "AC Power Connected"
            elif status == 'Discharging':
                if percentage > 75:
                    icon = "🔋"
                elif percentage > 50:
                    icon = "🔋"
                elif percentage > 25:
                    icon = "🪫"
                else:
                    icon = "🪫"
                status_text = "%s %d%% Discharging" % (icon, percentage)
                power_text = "On Battery Power"
            elif status == 'Full':
                icon = "🔋"
                status_text = "%s %d%% Full" % (icon, percentage)
                power_text = "AC Power Connected"
            else:
                icon = "🔋"
                status_text = "%s %d%% %s" % (icon, percentage, status)
                power_text = "Status: %s" % status
            
            karamba.changeText(widget, "battery_status", status_text)
            karamba.changeText(widget, "power_status", power_text)
            karamba.setBarValue(widget, "battery_bar", percentage)
            
            # Update colors based on battery level and status
            if status == 'Charging':
                # Blue when charging
                text_color = (100, 150, 255)
                bar_color = (0, 150, 255)
            elif percentage > 50:
                # Green when battery is good
                text_color = (100, 255, 100)
                bar_color = (0, 255, 0)
            elif percentage > 20:
                # Yellow when battery is getting low
                text_color = (255, 255, 100)
                bar_color = (255, 255, 0)
            else:
                # Red when battery is critically low
                text_color = (255, 100, 100)
                bar_color = (255, 0, 0)
            
            karamba.changeTextColor(widget, "battery_status", 
                                   text_color[0], text_color[1], text_color[2])
            karamba.changeBarColor(widget, "battery_bar", 
                                  bar_color[0], bar_color[1], bar_color[2])
                                  
        else:
            # No battery detected (desktop system)
            karamba.changeText(widget, "battery_status", "🖥️ Desktop System")
            karamba.changeText(widget, "power_status", "No Battery Detected")
            karamba.setBarValue(widget, "battery_bar", 0)
            
    except Exception, e:
        karamba.changeText(widget, "battery_status", "Error: %s" % str(e))

def getBatteryInfo():
    """Get battery information from system"""
    # Try to find battery information in /sys/class/power_supply/
    try:
        battery_paths = glob.glob('/sys/class/power_supply/BAT*')
        
        for battery_path in battery_paths:
            try:
                # Read battery capacity
                capacity_file = os.path.join(battery_path, 'capacity')
                if os.path.exists(capacity_file):
                    f = open(capacity_file, 'r')
                    capacity = int(f.read().strip())
                    f.close()
                else:
                    continue
                
                # Read battery status
                status_file = os.path.join(battery_path, 'status')
                if os.path.exists(status_file):
                    f = open(status_file, 'r')
                    status = f.read().strip()
                    f.close()
                else:
                    status = 'Unknown'
                
                return {
                    'percentage': capacity,
                    'status': status
                }
                
            except:
                continue
                
        # Try alternative ACPI method
        return getBatteryInfoACPI()
        
    except:
        return None

def getBatteryInfoACPI():
    """Try to get battery info via ACPI"""
    try:
        # Look for ACPI battery info
        acpi_battery_paths = glob.glob('/proc/acpi/battery/BAT*')
        
        for battery_path in acpi_battery_paths:
            try:
                # Read battery state
                state_file = os.path.join(battery_path, 'state')
                info_file = os.path.join(battery_path, 'info')
                
                if not (os.path.exists(state_file) and os.path.exists(info_file)):
                    continue
                
                # Parse state file
                f = open(state_file, 'r')
                state_lines = f.readlines()
                f.close()
                
                f = open(info_file, 'r')
                info_lines = f.readlines()
                f.close()
                
                # Extract information
                charging_state = None
                remaining_capacity = None
                last_full_capacity = None
                
                for line in state_lines:
                    if 'charging state:' in line:
                        charging_state = line.split(':')[1].strip()
                    elif 'remaining capacity:' in line:
                        remaining_capacity = int(line.split(':')[1].strip().split()[0])
                
                for line in info_lines:
                    if 'last full capacity:' in line:
                        last_full_capacity = int(line.split(':')[1].strip().split()[0])
                
                if remaining_capacity is not None and last_full_capacity is not None:
                    percentage = int((remaining_capacity / float(last_full_capacity)) * 100)
                    
                    # Map ACPI charging state to standard status
                    if charging_state == 'charging':
                        status = 'Charging'
                    elif charging_state == 'discharging':
                        status = 'Discharging'
                    else:
                        status = 'Unknown'
                    
                    return {
                        'percentage': percentage,
                        'status': status
                    }
                    
            except:
                continue
                
    except:
        pass
        
    return None

def widgetClicked(widget, x, y, button):
    """Handle mouse clicks"""
    if button == 1:  # Left click - refresh
        updateBatteryStatus(widget)

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass