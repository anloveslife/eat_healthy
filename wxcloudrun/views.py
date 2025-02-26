import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters


logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')

def bmi_calculator(request, _):
    """
    获取BMI 不需要存储就不要调用model
    """
    height = request.GET.get('height') #m
    weight = request.GET.get('weight') #kg
    #初始化默认
    rsp = JsonResponse({'code': -1, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if not height or not weight:
        return rsp
    #执行逻辑
    if request.method == 'GET' or request.method == 'get':
        rsp = cal_bmi(float(height), float(weight))
    else:
        rsp = JsonResponse({'code': -2, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    return rsp

def cal_bmi(height, weight):
    """
    计算bmi
    """    
    bmi = weight / (height**2)
    bmi_class = ""
    if bmi < 18.4:
        bmi_class = "偏瘦"
    elif bmi < 24.0:
        bmi_class = "正常"
    elif bmi < 28.0:
        bmi_class = "过重"
    else:
        bmi_class = "肥胖"
    if bmi_class:
        return JsonResponse({'code': 0, 'bmi': bmi, 'bmi_class': bmi_class},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -10, 'bmi': -1, 'bmi_class': bmi_class},
                    json_dumps_params={'ensure_ascii': False})
         


def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})
