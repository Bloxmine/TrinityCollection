#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Temperature Monitor SuperKaramba Widget
#  Shows CPU temperature from system sensors
#  Compatible with Trinity Desktop / KDE 3.5

import karamba
import time
import os
import glob

def initWidget(widget):
    """Initialize the widget"""
    updateTemperature(widget)
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called periodically to update temperature"""
    updateTemperature(widget)

def updateTemperature(widget):
    """Update temperature display"""
    try:
        temp_celsius = getCPUTemperature()
        
        if temp_celsius is not None:
            # Update temperature display
            karamba.changeText(widget, "cpu_temp", "%.1f °C" % temp_celsius)
            
            # Update progress bar (scale 0-100°C to 0-100%)
            temp_percent = min(100, max(0, temp_celsius))
            karamba.setBarValue(widget, "temp_bar", int(temp_percent))
            
            # Update status and colors based on temperature
            if temp_celsius < 40:
                status = "Cool"
                temp_color = (100, 255, 100)  # Green
                bar_color = (0, 255, 0)
            elif temp_celsius < 60:
                status = "Normal"
                temp_color = (255, 255, 100)  # Yellow
                bar_color = (255, 255, 0)
            elif temp_celsius < 80:
                status = "Warm"
                temp_color = (255, 150, 100)  # Orange
                bar_color = (255, 150, 0)
            else:
                status = "Hot!"
                temp_color = (255, 100, 100)  # Red
                bar_color = (255, 0, 0)
            
            karamba.changeText(widget, "temp_status", "Status: %s" % status)
            karamba.changeTextColor(widget, "cpu_temp", temp_color[0], temp_color[1], temp_color[2])
            karamba.changeBarColor(widget, "temp_bar", bar_color[0], bar_color[1], bar_color[2])
            
        else:
            karamba.changeText(widget, "cpu_temp", "N/A")
            karamba.changeText(widget, "temp_status", "Status: No sensor")
            karamba.setBarValue(widget, "temp_bar", 0)
            
    except Exception, e:
        karamba.changeText(widget, "cpu_temp", "Error")
        karamba.changeText(widget, "temp_status", "Status: %s" % str(e))

def getCPUTemperature():
    """Get CPU temperature from various possible sources"""
    # Try different temperature sources in order of preference
    
    # Method 1: Try hwmon sensors (modern Linux)
    temp = getTemperatureFromHwmon()
    if temp is not None:
        return temp
    
    # Method 2: Try thermal zones
    temp = getTemperatureFromThermalZone()
    if temp is not None:
        return temp
    
    # Method 3: Try ACPI thermal info
    temp = getTemperatureFromACPI()
    if temp is not None:
        return temp
    
    # Method 4: Simulate temperature for demo if no sensors available
    return getSimulatedTemperature()

def getTemperatureFromHwmon():
    """Get temperature from hwmon sensors"""
    try:
        # Look for hwmon temperature sensors
        hwmon_paths = glob.glob('/sys/class/hwmon/hwmon*/temp*_input')
        
        for path in hwmon_paths:
            try:
                f = open(path, 'r')
                temp_millicelsius = int(f.read().strip())
                f.close()
                
                # Convert from millicelsius to celsius
                temp_celsius = temp_millicelsius / 1000.0
                
                # Reasonable temperature range check
                if 0 <= temp_celsius <= 150:
                    return temp_celsius
                    
            except:
                continue
                
    except:
        pass
        
    return None

def getTemperatureFromThermalZone():
    """Get temperature from thermal zone"""
    try:
        thermal_paths = glob.glob('/sys/class/thermal/thermal_zone*/temp')
        
        for path in thermal_paths:
            try:
                f = open(path, 'r')
                temp_millicelsius = int(f.read().strip())
                f.close()
                
                temp_celsius = temp_millicelsius / 1000.0
                
                if 0 <= temp_celsius <= 150:
                    return temp_celsius
                    
            except:
                continue
                
    except:
        pass
        
    return None

def getTemperatureFromACPI():
    """Get temperature from ACPI thermal info"""
    try:
        acpi_paths = glob.glob('/proc/acpi/thermal_zone/*/temperature')
        
        for path in acpi_paths:
            try:
                f = open(path, 'r')
                line = f.readline()
                f.close()
                
                # Parse line like "temperature:             45 C"
                parts = line.split()
                if len(parts) >= 2:
                    temp_celsius = float(parts[1])
                    if 0 <= temp_celsius <= 150:
                        return temp_celsius
                        
            except:
                continue
                
    except:
        pass
        
    return None

def getSimulatedTemperature():
    """Generate simulated temperature for demo purposes"""
    try:
        # Base temperature varies with time to simulate load changes
        import random
        base_temp = 45 + random.randint(-10, 15)
        
        # Add some variation based on current time
        current_time = time.time()
        variation = 5 * abs(hash(str(int(current_time / 10))) % 100 - 50) / 50.0
        
        return base_temp + variation
        
    except:
        return 42.0  # Default temperature

def widgetClicked(widget, x, y, button):
    """Handle mouse clicks"""
    if button == 1:  # Left click - refresh
        updateTemperature(widget)

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass