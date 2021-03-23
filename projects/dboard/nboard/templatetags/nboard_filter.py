from django import template
# nboard앱에서 사용할 템플릿 필터 작성 - 템플릿 필터는 반드시 앱디렉터리 하위에 생성

register = template.Library()

@register.filter
def sub(value, arg):
    # A|sub:B = A-B
    return value - arg