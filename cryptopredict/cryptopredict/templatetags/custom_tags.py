from django import template

register = template.Library()

@register.filter
def color_value(value):
    """Returns the value wrapped in red if negative, green if positive"""
    try:
        value = float(value)  # Ensure it's a number
    except ValueError:
        return value  # Return as is if not a number

    if value < 0:
        color = "red"
    elif value > 0:
        color = "green"
    else:
        color = "black"
    sign = "+" if value > 0 else ""  # Add "+" for positive values
    return f'<span style="color: {color};">{sign}{value}</span>'
