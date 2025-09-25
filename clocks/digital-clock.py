#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Digital Clock SuperKaramba Widget
#  Shows current time and date
#  Compatible with Trinity Desktop / KDE 3.5

import karamba
import time

use_24_hour = True

def initWidget(widget):
    """Initialize the widget"""
    updateClock(widget)
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called every second to update the clock"""
    updateClock(widget)

def updateClock(widget):
    """Update the time and date display"""
    global use_24_hour
    
    try:
        # Get current time
        current_time = time.localtime()
        
        # Format time based on 12/24 hour preference
        if use_24_hour:
            time_str = time.strftime("%H:%M:%S", current_time)
            format_str = "24-hour format"
        else:
            time_str = time.strftime("%I:%M:%S %p", current_time)
            format_str = "12-hour format"
        
        # Format date
        date_str = time.strftime("%A, %B %d, %Y", current_time)
        
        # Update displays
        karamba.changeText(widget, "time_display", time_str)
        karamba.changeText(widget, "date_display", date_str)
        karamba.changeText(widget, "format_display", format_str)
        
        # Change color based on time of day
        hour = current_time.tm_hour
        if 6 <= hour < 12:  # Morning - green
            karamba.changeTextColor(widget, "time_display", 0, 255, 100)
        elif 12 <= hour < 18:  # Afternoon - blue
            karamba.changeTextColor(widget, "time_display", 100, 150, 255)
        elif 18 <= hour < 22:  # Evening - orange
            karamba.changeTextColor(widget, "time_display", 255, 150, 0)
        else:  # Night - purple
            karamba.changeTextColor(widget, "time_display", 200, 100, 255)
            
    except Exception, e:
        karamba.changeText(widget, "time_display", "Error: %s" % str(e))

def widgetClicked(widget, x, y, button):
    """Handle mouse clicks - toggle 12/24 hour format"""
    global use_24_hour
    
    if button == 1:  # Left click
        use_24_hour = not use_24_hour
        updateClock(widget)

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass