#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  System Information SuperKaramba Widget
#  Shows various system information
#  Compatible with Trinity Desktop / KDE 3.5

import karamba
import time
import os
import socket

def initWidget(widget):
    """Initialize the widget"""
    updateSystemInfo(widget)
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called periodically to update system information"""
    updateSystemInfo(widget)

def updateSystemInfo(widget):
    """Update all system information displays"""
    try:
        # Get hostname
        hostname = getHostname()
        karamba.changeText(widget, "hostname_display", "Hostname: %s" % hostname)
        
        # Get kernel information
        kernel_info = getKernelInfo()
        karamba.changeText(widget, "kernel_display", "Kernel: %s" % kernel_info)
        
        # Get uptime
        uptime_str = getUptime()
        karamba.changeText(widget, "uptime_display", "Uptime: %s" % uptime_str)
        
        # Get process count
        process_count = getProcessCount()
        karamba.changeText(widget, "processes_display", "Processes: %d" % process_count)
        
        # Get user count
        user_count = getUserCount()
        karamba.changeText(widget, "users_display", "Users: %d" % user_count)
        
        # Get architecture
        arch = getArchitecture()
        karamba.changeText(widget, "arch_display", "Architecture: %s" % arch)
        
        # Desktop environment
        desktop = getDesktopEnvironment()
        karamba.changeText(widget, "desktop_display", "Desktop: %s" % desktop)
        
        # Update timestamp
        current_time = time.strftime("%H:%M:%S")
        karamba.changeText(widget, "last_update", "Last updated: %s" % current_time)
        
    except Exception, e:
        karamba.changeText(widget, "hostname_display", "Error: %s" % str(e))

def getHostname():
    """Get system hostname"""
    try:
        return socket.gethostname()
    except:
        return "Unknown"

def getKernelInfo():
    """Get kernel version information"""
    try:
        # Try to read from /proc/version
        f = open('/proc/version', 'r')
        version_line = f.readline()
        f.close()
        
        # Extract kernel version
        parts = version_line.split()
        if len(parts) >= 3:
            return "%s %s" % (parts[0], parts[2])
        else:
            return "Linux"
            
    except:
        # Fallback to uname
        try:
            import platform
            return "%s %s" % (platform.system(), platform.release())
        except:
            return "Unknown"

def getUptime():
    """Get system uptime"""
    try:
        # Read uptime from /proc/uptime
        f = open('/proc/uptime', 'r')
        uptime_seconds = float(f.readline().split()[0])
        f.close()
        
        # Convert to human readable format
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        if days > 0:
            return "%d days, %d:%02d" % (days, hours, minutes)
        else:
            return "%d:%02d" % (hours, minutes)
            
    except:
        return "Unknown"

def getProcessCount():
    """Get number of running processes"""
    try:
        # Count entries in /proc that are numeric (PIDs)
        proc_entries = os.listdir('/proc')
        process_count = 0
        
        for entry in proc_entries:
            if entry.isdigit():
                process_count += 1
                
        return process_count
        
    except:
        return 0

def getUserCount():
    """Get number of logged in users"""
    try:
        # Parse /etc/passwd for user count
        # This gives total users, not currently logged in
        # For logged in users, we'd need to parse 'who' command output
        f = open('/etc/passwd', 'r')
        users = 0
        for line in f:
            if line.strip() and not line.startswith('#'):
                parts = line.split(':')
                if len(parts) >= 3:
                    # Count real users (UID >= 1000 typically)
                    try:
                        uid = int(parts[2])
                        if uid >= 1000 or uid == 0:  # Include root
                            users += 1
                    except:
                        pass
        f.close()
        return users
        
    except:
        return 0

def getArchitecture():
    """Get system architecture"""
    try:
        # Read from /proc/cpuinfo
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line.startswith('flags') or line.startswith('Features'):
                f.close()
                if 'lm' in line:  # Long mode = 64-bit
                    return "x86_64"
                else:
                    return "i386"
        f.close()
        
        # Fallback
        import platform
        return platform.machine()
        
    except:
        return "Unknown"

def getDesktopEnvironment():
    """Detect desktop environment"""
    try:
        # Check environment variables
        desktop = os.environ.get('DESKTOP_SESSION', '')
        if 'trinity' in desktop.lower() or 'kde' in desktop.lower():
            return "Trinity"
        
        xdg_current = os.environ.get('XDG_CURRENT_DESKTOP', '')
        if 'trinity' in xdg_current.lower():
            return "Trinity"
        elif 'kde' in xdg_current.lower():
            return "KDE"
        elif 'gnome' in xdg_current.lower():
            return "GNOME"
        elif 'xfce' in xdg_current.lower():
            return "XFCE"
        
        # Check for Trinity/KDE specific processes
        try:
            import subprocess
            ps_output = subprocess.check_output(['ps', 'aux'])
            if 'kdesktop' in ps_output or 'trinity' in ps_output:
                return "Trinity"
        except:
            pass
            
        return "Unknown"
        
    except:
        return "Unknown"

def widgetClicked(widget, x, y, button):
    """Handle mouse clicks - refresh on click"""
    if button == 1:  # Left click
        updateSystemInfo(widget)

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass