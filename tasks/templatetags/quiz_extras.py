from django import template

register = template.Library()


@register.filter
def get_option(question, option):
    """
    Returns option text based on option letter
    """
    return {
        "A": question.option_a,
        "B": question.option_b,
        "C": question.option_c,
        "D": question.option_d,
    }.get(option, "")
