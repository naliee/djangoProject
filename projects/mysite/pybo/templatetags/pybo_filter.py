from django import template

register = template.Library()

# 템플릿 필터 함수 생성 - 함수 정의 한 후 @register.filter애너테이션 적용
@register.filter
def sub(value, arg):
    return value - arg