from django import template

register = template.Library()


@register.filter
def is_correct_choice(selected_option, correct_options):
    return selected_option in correct_options
