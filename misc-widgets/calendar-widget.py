#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Calendar Widget SuperKaramba Widget  
#  Shows monthly calendar with current date highlighted
#  Compatible with Trinity Desktop / KDE 3.5

import karamba
import time
import calendar

def initWidget(widget):
    """Initialize the widget"""
    updateCalendar(widget)
    karamba.redrawWidget(widget)

def widgetUpdated(widget):
    """Called periodically to update calendar"""
    updateCalendar(widget)

def updateCalendar(widget):
    """Update calendar display"""
    try:
        # Get current date
        now = time.localtime()
        year = now.tm_year
        month = now.tm_mon
        today = now.tm_mday
        
        # Update month/year header
        month_name = calendar.month_name[month]
        karamba.changeText(widget, "month_year", "%s %d" % (month_name, year))
        
        # Generate calendar for current month
        cal = calendar.monthcalendar(year, month)
        
        # Format calendar weeks
        week_names = ["week1", "week2", "week3", "week4", "week5"]
        
        for i, week in enumerate(cal):
            if i < len(week_names):
                week_text = formatWeek(week, today)
                karamba.changeText(widget, week_names[i], week_text)
        
        # Clear unused week slots
        for i in range(len(cal), len(week_names)):
            karamba.changeText(widget, week_names[i], "")
        
        # Update today display
        weekday_name = calendar.day_name[now.tm_wday]
        today_text = "Today: %s, %s %d" % (weekday_name, month_name[:3], today)
        karamba.changeText(widget, "today_display", today_text)
        
        # Update status
        karamba.changeText(widget, "status_line", "Updated: %s" % time.strftime("%H:%M"))
        
    except Exception, e:
        karamba.changeText(widget, "month_year", "Error: %s" % str(e))

def formatWeek(week, today_date):
    """Format a week row with proper spacing and highlighting"""
    formatted_days = []
    
    for day in week:
        if day == 0:
            # Empty day slot
            formatted_days.append(" -")
        elif day == today_date:
            # Highlight today (we'll change color in the theme)
            formatted_days.append("%2d" % day)
        else:
            # Regular day
            formatted_days.append("%2d" % day)
    
    return " ".join(formatted_days)

def highlightToday(widget):
    """Highlight today's date by changing text colors"""
    try:
        now = time.localtime()
        today = now.tm_mday
        year = now.tm_year
        month = now.tm_mon
        
        # Get calendar for current month
        cal = calendar.monthcalendar(year, month)
        week_names = ["week1", "week2", "week3", "week4", "week5"]
        
        # Find today's position and highlight it
        for week_idx, week in enumerate(cal):
            if week_idx < len(week_names):
                week_text = ""
                for day in week:
                    if day == 0:
                        week_text += " - "
                    elif day == today:
                        # This would be highlighted in a real implementation
                        week_text += "%2d " % day
                    else:
                        week_text += "%2d " % day
                
                karamba.changeText(widget, week_names[week_idx], week_text.strip())
                
                # In a full implementation, you could change text color for today
                if today in week:
                    karamba.changeTextColor(widget, week_names[week_idx], 255, 255, 100)
                else:
                    karamba.changeTextColor(widget, week_names[week_idx], 180, 180, 180)
                    
    except:
        pass

def widgetClicked(widget, x, y, button):
    """Handle mouse clicks"""
    if button == 1:  # Left click - refresh calendar
        updateCalendar(widget)
        highlightToday(widget)
    elif button == 3:  # Right click - navigate months (future enhancement)
        # Could implement month navigation here
        pass

def widgetMouseMoved(widget, x, y, button):
    """Handle mouse movement"""
    pass

# Additional utility functions for calendar functionality

def getDayOfYear():
    """Get current day of the year"""
    now = time.localtime()
    return now.tm_yday

def getWeekNumber():
    """Get current week number"""
    now = time.localtime()
    # Simple week calculation
    return (now.tm_yday - 1) // 7 + 1

def isLeapYear(year):
    """Check if year is a leap year"""
    return calendar.isleap(year)

def getMonthInfo(year, month):
    """Get information about a specific month"""
    return {
        'name': calendar.month_name[month],
        'abbrev': calendar.month_abbr[month], 
        'days': calendar.monthrange(year, month)[1],
        'first_weekday': calendar.monthrange(year, month)[0]
    }

# Note: In a more advanced version, you could add features like:
# - Month navigation with arrow keys or clicks
# - Holiday highlighting  
# - Event/appointment markers
# - Different calendar systems
# - Custom color themes
# - Mini-calendar mode