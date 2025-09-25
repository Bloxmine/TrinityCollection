#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Analog Clock SuperKaramba Widget
#  Shows analog clock with hour, minute, and second hands
#  Compatible with Trinity Desktop / KDE 3.5

import karamba
import time
import math

def initWidget(widget):
    """Initialize the widget"""
    drawClockFace(widget)
    updateClock(widget)
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called every second to update the clock"""
    updateClock(widget)

def drawClockFace(widget):
    """Draw the analog clock face"""
    try:
        # Create clock face circle
        points = []
        center_x, center_y = 75, 75
        radius = 65
        
        # Generate circle points
        for i in range(61):  # More points for smoother circle
            angle = (i * 6) * (math.pi / 180)  # Convert to radians
            x = center_x + radius * math.sin(angle)
            y = center_y - radius * math.cos(angle)
            points.append((int(x), int(y)))
        
        # Draw clock face outline
        karamba.createPolygon(widget, points, "clock_face")
        
        # Draw hour markers (small lines)
        for hour in range(12):
            angle = hour * 30 * (math.pi / 180)  # 30 degrees per hour
            inner_radius = 55
            outer_radius = 60
            
            x1 = center_x + inner_radius * math.sin(angle)
            y1 = center_y - inner_radius * math.cos(angle)
            x2 = center_x + outer_radius * math.sin(angle)
            y2 = center_y - outer_radius * math.cos(angle)
            
            # Note: In real SuperKaramba, you'd use createLine, but we'll simulate with small polygons
            marker_points = [(int(x1), int(y1)), (int(x2), int(y2))]
            karamba.createPolygon(widget, marker_points, "marker_%d" % hour)
        
        # Draw center dot
        center_points = []
        for i in range(9):  # Small circle for center
            angle = (i * 40) * (math.pi / 180)
            x = center_x + 3 * math.sin(angle)
            y = center_y + 3 * math.cos(angle)
            center_points.append((int(x), int(y)))
        
        karamba.createPolygon(widget, center_points, "center_dot")
        
    except:
        pass  # If drawing fails, continue with basic functionality

def updateClock(widget):
    """Update the clock hands"""
    try:
        # Get current time
        current_time = time.localtime()
        hour = current_time.tm_hour % 12  # Convert to 12-hour format
        minute = current_time.tm_min
        second = current_time.tm_sec
        
        center_x, center_y = 75, 75
        
        # Calculate angles (0 degrees = 12 o'clock, clockwise)
        second_angle = second * 6 * (math.pi / 180)      # 6 degrees per second
        minute_angle = (minute + second/60.0) * 6 * (math.pi / 180)  # 6 degrees per minute
        hour_angle = (hour + minute/60.0) * 30 * (math.pi / 180)     # 30 degrees per hour
        
        # Remove old hands
        karamba.deletePolygon(widget, "hour_hand")
        karamba.deletePolygon(widget, "minute_hand")
        karamba.deletePolygon(widget, "second_hand")
        
        # Draw hour hand (short, thick)
        hour_length = 35
        hour_x = center_x + hour_length * math.sin(hour_angle)
        hour_y = center_y - hour_length * math.cos(hour_angle)
        hour_points = [(center_x, center_y), (int(hour_x), int(hour_y))]
        karamba.createPolygon(widget, hour_points, "hour_hand")
        
        # Draw minute hand (longer, medium thickness)
        minute_length = 50
        minute_x = center_x + minute_length * math.sin(minute_angle)
        minute_y = center_y - minute_length * math.cos(minute_angle)
        minute_points = [(center_x, center_y), (int(minute_x), int(minute_y))]
        karamba.createPolygon(widget, minute_points, "minute_hand")
        
        # Draw second hand (longest, thin)
        second_length = 55
        second_x = center_x + second_length * math.sin(second_angle)
        second_y = center_y - second_length * math.cos(second_angle)
        second_points = [(center_x, center_y), (int(second_x), int(second_y))]
        karamba.createPolygon(widget, second_points, "second_hand")
        
    except Exception, e:
        # If analog display fails, show digital time as fallback
        time_str = time.strftime("%H:%M:%S")
        karamba.changeText(widget, "hour_12", time_str)

def widgetClicked(widget, x, y, button):
    """Handle mouse clicks"""
    pass

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass