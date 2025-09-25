#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Disk Usage Monitor SuperKaramba Widget
#  Shows disk space usage for various filesystems
#  Compatible with Trinity Desktop / KDE 3.5

import karamba
import time
import os

def initWidget(widget):
    """Initialize the widget"""
    updateDiskUsage(widget)
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called periodically to update disk usage information"""
    updateDiskUsage(widget)

def updateDiskUsage(widget):
    """Update disk usage displays"""
    try:
        # Get disk usage for key filesystems
        filesystems = [
            ('/', 'root_usage', 'root_bar'),
            ('/home', 'home_usage', 'home_bar')
        ]
        
        active_filesystems = 0
        
        for path, text_name, bar_name in filesystems:
            usage_info = getDiskUsage(path)
            
            if usage_info:
                active_filesystems += 1
                
                # Format the display string
                used_gb = usage_info['used'] / (1024.0 ** 3)
                total_gb = usage_info['total'] / (1024.0 ** 3)
                percent = usage_info['percent']
                
                display_text = "%s: %.1fGB / %.1fGB (%.1f%%)" % (
                    path, used_gb, total_gb, percent
                )
                
                karamba.changeText(widget, text_name, display_text)
                karamba.setBarValue(widget, bar_name, int(percent))
                
                # Change bar color based on usage level
                if percent > 90:
                    # Red for very high usage
                    karamba.changeBarColor(widget, bar_name, 255, 50, 50)
                elif percent > 75:
                    # Orange for high usage
                    karamba.changeBarColor(widget, bar_name, 255, 150, 0)
                elif percent > 50:
                    # Yellow for medium usage
                    karamba.changeBarColor(widget, bar_name, 255, 255, 50)
                else:
                    # Green for low usage
                    karamba.changeBarColor(widget, bar_name, 50, 255, 50)
            else:
                # Filesystem not available
                karamba.changeText(widget, text_name, "%s: Not Available" % path)
                karamba.setBarValue(widget, bar_name, 0)
        
        # Update summary
        karamba.changeText(widget, "summary_display", 
                          "Total: %d filesystems monitored" % active_filesystems)
        
        # Update timestamp
        current_time = time.strftime("%H:%M:%S")
        karamba.changeText(widget, "last_update", "Last updated: %s" % current_time)
        
    except Exception, e:
        karamba.changeText(widget, "root_usage", "Error: %s" % str(e))

def getDiskUsage(path):
    """Get disk usage statistics for a given path"""
    try:
        # Check if path exists
        if not os.path.exists(path):
            return None
            
        # Get disk usage using os.statvfs
        statvfs = os.statvfs(path)
        
        # Calculate sizes in bytes
        total_size = statvfs.f_frsize * statvfs.f_blocks
        free_size = statvfs.f_frsize * statvfs.f_available
        used_size = total_size - free_size
        
        # Calculate percentage
        if total_size > 0:
            percent_used = (used_size / float(total_size)) * 100
        else:
            percent_used = 0
            
        return {
            'total': total_size,
            'used': used_size,
            'free': free_size,
            'percent': percent_used
        }
        
    except:
        return None

def getFilesystemType(path):
    """Get filesystem type for a given path"""
    try:
        # Read /proc/mounts to get filesystem type
        f = open('/proc/mounts', 'r')
        for line in f:
            parts = line.split()
            if len(parts) >= 3 and parts[1] == path:
                f.close()
                return parts[2]  # filesystem type
        f.close()
        return "unknown"
        
    except:
        return "unknown"

def getAllMountPoints():
    """Get all mounted filesystems"""
    mount_points = []
    
    try:
        f = open('/proc/mounts', 'r')
        for line in f:
            parts = line.split()
            if len(parts) >= 3:
                device = parts[0]
                mount_point = parts[1]
                fs_type = parts[2]
                
                # Skip special filesystems
                if (not device.startswith('/dev/') and 
                    not mount_point.startswith('/media/') and
                    not mount_point.startswith('/mnt/')):
                    continue
                    
                # Skip common system filesystems
                if fs_type in ['proc', 'sysfs', 'devfs', 'tmpfs', 'devpts']:
                    continue
                    
                mount_points.append({
                    'device': device,
                    'mount_point': mount_point,
                    'fs_type': fs_type
                })
        f.close()
        
    except:
        pass
        
    return mount_points

def formatBytes(bytes_value):
    """Format bytes in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return "%.1f %s" % (bytes_value, unit)
        bytes_value /= 1024.0
    return "%.1f PB" % bytes_value

def widgetClicked(widget, x, y, button):
    """Handle mouse clicks"""
    if button == 1:  # Left click - refresh immediately
        updateDiskUsage(widget)
    elif button == 3:  # Right click - show additional info
        # Could cycle through different mount points
        pass

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass