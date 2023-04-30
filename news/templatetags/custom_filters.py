from django import template

register = template.Library()


@register.filter()
def censor(value):
    b_w = ('текст')
    if not isinstance(value, str):
        raise TypeErrorError(f"unresolved type '{type(value)}' expected type 'str")
    for w in value.split():
       if w.lower() in b_w:
          value = value.replace(w, f"{w[0]}{'*' * (len(w) - 1)}")
    return value



