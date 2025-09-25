#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  CPU Monitor SuperKaramba Widget
#  Shows CPU usage percentage and load average
#  Compatible with Trinity Desktop / KDE 3.5

import karamba
import os
import time

cpu_last_idle = 0
cpu_last_total = 0

def initWidget(widget):
    """Initialize the widget"""
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called when widget needs to be updated"""
    try:
        # Get CPU usage
        cpu_percent = getCPUUsage()
        
        # Get load average
        load_avg = getLoadAverage()
        
        # Update the display
        karamba.changeText(widget, "cpu_usage", "CPU Usage: %.1f%%" % cpu_percent)
        karamba.changeText(widget, "load_avg", "Load Average: %.2f" % load_avg)
        karamba.setBarValue(widget, "cpu_bar", int(cpu_percent))
        
        # Update timestamp
        current_time = time.strftime("%H:%M:%S")
        karamba.changeText(widget, "last_update", "Updated: %s" % current_time)
        
    except Exception, e:
        karamba.changeText(widget, "cpu_usage", "Error: %s" % str(e))

def getCPUUsage():
    """Calculate CPU usage percentage"""
    global cpu_last_idle, cpu_last_total
    
    try:
        # Read /proc/stat for CPU stats
        f = open('/proc/stat', 'r')
        line = f.readline()
        f.close()
        
        # Parse the first line (overall CPU stats)
        cpu_times = [int(x) for x in line.split()[1:]]
        
        # Calculate totals
        idle_time = cpu_times[3]  # idle time
        total_time = sum(cpu_times)
        
        # Calculate differences
        idle_diff = idle_time - cpu_last_idle
        total_diff = total_time - cpu_last_total
        
        # Calculate usage percentage
        if total_diff > 0:
            cpu_usage = 100.0 * (total_diff - idle_diff) / total_diff
        else:
            cpu_usage = 0.0
            
        # Store current values for next calculation
        cpu_last_idle = idle_time
        cpu_last_total = total_time
        
        return cpu_usage
        
    except:
        return 0.0

def getLoadAverage():
    """Get system load average"""
    try:
        # Read load average from /proc/loadavg
        f = open('/proc/loadavg', 'r')
        load_data = f.readline().split()
        f.close()
        
        # Return 1-minute load average
        return float(load_data[0])
        
    except:
        return 0.0

# Widget refresh interval (in milliseconds)
karamba.acceptDrops(widget)

# This gets called everytime our widget is updated
# The update interval is specified in the .theme file
def widgetClicked(widget, x, y, button):
    """Handle mouse clicks"""
    pass

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass