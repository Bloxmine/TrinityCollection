#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Network Monitor SuperKaramba Widget
#  Shows network upload/download speeds and totals
#  Compatible with Trinity Desktop / KDE 3.5

import karamba
import time
import os

# Global variables to track previous values
last_rx_bytes = 0
last_tx_bytes = 0
last_update_time = 0
current_interface = "eth0"

def initWidget(widget):
    """Initialize the widget"""
    global current_interface
    current_interface = findActiveInterface()
    karamba.changeText(widget, "interface_name", "Interface: %s" % current_interface)
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called when widget needs to be updated"""
    global last_rx_bytes, last_tx_bytes, last_update_time, current_interface
    
    try:
        current_time = time.time()
        
        # Get network statistics
        net_stats = getNetworkStats(current_interface)
        
        if net_stats and last_update_time > 0:
            # Calculate time difference
            time_diff = current_time - last_update_time
            
            if time_diff > 0:
                # Calculate speeds (bytes per second)
                rx_speed = (net_stats['rx_bytes'] - last_rx_bytes) / time_diff
                tx_speed = (net_stats['tx_bytes'] - last_tx_bytes) / time_diff
                
                # Update speed displays
                karamba.changeText(widget, "download_speed", 
                                  "▼ Download: %s" % formatSpeed(rx_speed))
                karamba.changeText(widget, "upload_speed", 
                                  "▲ Upload: %s" % formatSpeed(tx_speed))
        
        if net_stats:
            # Update total statistics
            karamba.changeText(widget, "total_download", 
                              "Total Down: %s" % formatBytes(net_stats['rx_bytes']))
            karamba.changeText(widget, "total_upload", 
                              "Total Up: %s" % formatBytes(net_stats['tx_bytes']))
            
            # Store current values for next calculation
            last_rx_bytes = net_stats['rx_bytes']
            last_tx_bytes = net_stats['tx_bytes']
            
        last_update_time = current_time
        
        # Update timestamp
        current_time_str = time.strftime("%H:%M:%S")
        karamba.changeText(widget, "last_update", "Updated: %s" % current_time_str)
        
    except Exception, e:
        karamba.changeText(widget, "download_speed", "Error: %s" % str(e))

def findActiveInterface():
    """Find the most active network interface"""
    try:
        interfaces = []
        f = open('/proc/net/dev', 'r')
        lines = f.readlines()[2:]  # Skip header lines
        f.close()
        
        for line in lines:
            parts = line.split(':')
            if len(parts) >= 2:
                interface = parts[0].strip()
                # Skip loopback interface
                if interface != 'lo':
                    stats = parts[1].split()
                    rx_bytes = int(stats[0])
                    if rx_bytes > 0:  # Interface has activity
                        interfaces.append((interface, rx_bytes))
        
        if interfaces:
            # Return interface with most activity
            interfaces.sort(key=lambda x: x[1], reverse=True)
            return interfaces[0][0]
        else:
            return "eth0"  # fallback
            
    except:
        return "eth0"

def getNetworkStats(interface):
    """Get network statistics for specified interface"""
    try:
        f = open('/proc/net/dev', 'r')
        lines = f.readlines()
        f.close()
        
        for line in lines:
            if interface + ':' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    stats = parts[1].split()
                    return {
                        'rx_bytes': int(stats[0]),
                        'tx_bytes': int(stats[8])
                    }
        
        return None
        
    except:
        return None

def formatSpeed(bytes_per_sec):
    """Format speed in human readable format"""
    if bytes_per_sec < 1024:
        return "%.1f B/s" % bytes_per_sec
    elif bytes_per_sec < 1024 * 1024:
        return "%.1f KB/s" % (bytes_per_sec / 1024)
    elif bytes_per_sec < 1024 * 1024 * 1024:
        return "%.1f MB/s" % (bytes_per_sec / (1024 * 1024))
    else:
        return "%.1f GB/s" % (bytes_per_sec / (1024 * 1024 * 1024))

def formatBytes(bytes_total):
    """Format total bytes in human readable format"""
    if bytes_total < 1024:
        return "%d B" % bytes_total
    elif bytes_total < 1024 * 1024:
        return "%.1f KB" % (bytes_total / 1024)
    elif bytes_total < 1024 * 1024 * 1024:
        return "%.1f MB" % (bytes_total / (1024 * 1024))
    else:
        return "%.1f GB" % (bytes_total / (1024 * 1024 * 1024))

def widgetClicked(widget, x, y, button):
    """Handle mouse clicks - cycle through interfaces"""
    global current_interface
    if button == 1:  # Left click
        current_interface = findActiveInterface()
        karamba.changeText(widget, "interface_name", "Interface: %s" % current_interface)

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass