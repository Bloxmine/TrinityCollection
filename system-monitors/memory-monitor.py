#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Memory Monitor SuperKaramba Widget
#  Shows RAM and Swap usage
#  Compatible with Trinity Desktop / KDE 3.5

import karamba
import time

def initWidget(widget):
    """Initialize the widget"""
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called when widget needs to be updated"""
    try:
        # Get memory information
        ram_info = getMemoryInfo()
        swap_info = getSwapInfo()
        
        # Update RAM display
        ram_used_mb = (ram_info['total'] - ram_info['free'] - ram_info['buffers'] - ram_info['cached']) / 1024
        ram_total_mb = ram_info['total'] / 1024
        ram_percent = (ram_used_mb / ram_total_mb) * 100 if ram_total_mb > 0 else 0
        
        karamba.changeText(widget, "ram_usage", 
                          "RAM: %dMB / %dMB (%.1f%%)" % (ram_used_mb, ram_total_mb, ram_percent))
        karamba.setBarValue(widget, "ram_bar", int(ram_percent))
        
        # Update Swap display
        if swap_info['total'] > 0:
            swap_used_mb = swap_info['used'] / 1024
            swap_total_mb = swap_info['total'] / 1024
            swap_percent = (swap_info['used'] / swap_info['total']) * 100
            
            karamba.changeText(widget, "swap_usage", 
                              "Swap: %dMB / %dMB (%.1f%%)" % (swap_used_mb, swap_total_mb, swap_percent))
            karamba.setBarValue(widget, "swap_bar", int(swap_percent))
        else:
            karamba.changeText(widget, "swap_usage", "Swap: Not Available")
            karamba.setBarValue(widget, "swap_bar", 0)
        
        # Update timestamp
        current_time = time.strftime("%H:%M:%S")
        karamba.changeText(widget, "last_update", "Updated: %s" % current_time)
        
    except Exception, e:
        karamba.changeText(widget, "ram_usage", "Error: %s" % str(e))

def getMemoryInfo():
    """Parse /proc/meminfo for memory statistics"""
    mem_info = {}
    
    try:
        f = open('/proc/meminfo', 'r')
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0].rstrip(':').lower()
                value = int(parts[1])  # Value in KB
                mem_info[key] = value
        f.close()
        
        # Ensure we have required fields
        required_fields = ['memtotal', 'memfree', 'buffers', 'cached']
        for field in required_fields:
            if field not in mem_info:
                mem_info[field] = 0
                
        return {
            'total': mem_info['memtotal'],
            'free': mem_info['memfree'],
            'buffers': mem_info['buffers'],
            'cached': mem_info['cached']
        }
        
    except:
        return {'total': 0, 'free': 0, 'buffers': 0, 'cached': 0}

def getSwapInfo():
    """Parse /proc/meminfo for swap statistics"""
    try:
        f = open('/proc/meminfo', 'r')
        swap_total = 0
        swap_free = 0
        
        for line in f:
            if line.startswith('SwapTotal:'):
                swap_total = int(line.split()[1])  # KB
            elif line.startswith('SwapFree:'):
                swap_free = int(line.split()[1])   # KB
                
        f.close()
        
        return {
            'total': swap_total,
            'used': swap_total - swap_free,
            'free': swap_free
        }
        
    except:
        return {'total': 0, 'used': 0, 'free': 0}

def widgetClicked(widget, x, y, button):
    """Handle mouse clicks"""
    pass

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass