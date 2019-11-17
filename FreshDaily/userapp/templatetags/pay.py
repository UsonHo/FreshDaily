#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Uson

from django import template
register = template.Library()
@register.filter

def uson_pay(state, ispay):
    if ispay == 'ispay':
        if state:
            return '已支付'
        else:
            return '未支付'
    elif ispay == 'ispay_do':
        if state:
            return '已付款'
        else:
            return '未付款'
    elif ispay == 'ispay_go':
        if state:
            return '查看物流'
        else:
            return '去付款'