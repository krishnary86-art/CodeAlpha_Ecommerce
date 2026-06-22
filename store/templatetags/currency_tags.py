from django import template

register = template.Library()


@register.filter
def inr(value):
    """Format a number as Indian Rupees with comma grouping."""
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return value

    if amount == int(amount):
        amount = int(amount)

    parts = f'{amount:,.2f}'.split('.')
    integer_part = parts[0]
    decimal_part = parts[1]

    if decimal_part == '00':
        formatted = integer_part
    else:
        formatted = f'{integer_part}.{decimal_part}'

    return f'₹{formatted}'
