from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from sms.models import CustomerInfo
import os
import uuid
import json


def upload_file(request):
    if request.method == 'GET':
        return render(request, 'upload_file.html')
    user = request.POST.get('user')
    avatar = request.FILES.get('customer_excel')
    file_name = os.path.join('static', 'imgs', avatar.name)
    with open(file_name, 'wb') as f:
        for line in avatar.chunks():
            f.write(line)
    data = xlrd.open_workbook(file_name)
    table = data.sheet_by_index(0)
    nrows = table.nrows  # 获得行数
    data_list = []
    try:
        for i in range(1, nrows):
            rows = table.row_values(i)
            obj_list = CustomerInfo(
                name=rows[0],
                age=rows[1],
                email=rows[2],
                company=rows[3],
            )
            data_list.append(obj_list)
        CustomerInfo.objects.bulk_create(data_list)
    except Exception as e:
        return HttpResponse('批量添加失败{}'.format(e))
    return redirect('/index/')


def upload_img(request):
    if request.method == 'GET':
        return render(request, 'upload_img.html')
    user = request.POST.get('user')
    avatar = request.FILES.get('avatar_img')
    file_name = str(uuid.uuid4()) + '.' + avatar.name.rsplit('.', maxsplit=1)[1]
    img_file_path = os.path.join('static', 'imgs', file_name)
    with open(img_file_path, 'wb') as f:
        for line in avatar.chunks():
            f.write(line)
    return HttpResponse('上传成功')


def form_data_upload(request):
    img_upload = request.FILES.get('img_upload')
    print(img_upload, type(img_upload))
    file_name = str(uuid.uuid4()) + '.' + img_upload.name.rsplit('.', maxsplit=1)[1]
    img_file_path = os.path.join('static', 'imgs', file_name)
    with open(img_file_path, 'wb') as f:
        for line in img_upload.chunks():
            f.write(line)
    return HttpResponse(img_file_path)


def iframe_upload_img(request):
    if request.method == 'GET':
        return render(request, 'iframe_upload_img.html')
    print(request.POST)
    return HttpResponse('成功')


def upload_iframe(request):
    ret = {'status': True, 'data': None}
    try:
        avatar = request.FILES.get('avatar')
        file_name = str(uuid.uuid4()) + '.' + avatar.name.rsplit('.', maxsplit=1)[1]
        img_file_path = os.path.join('static', 'imgs', file_name)
        with open(img_file_path, 'wb') as f:
            for line in avatar.chunks():
                f.write(line)
        ret['data'] = os.path.join('/', img_file_path)
    except Exception as e:
        ret['status'] = False
        ret['error'] = '上传失败'
    # return JsonResponse(ret)
    return HttpResponse(json.dumps(ret))


import xlrd, xlwt


def index(request):
    book_list = CustomerInfo.objects.all()  # 读取客户表中的所有信息
    paginator = Paginator(book_list, 20)  # 每页显示20条
    try:
        current_num = int(request.GET.get('page', 1))
        book_list = paginator.page(current_num)
    except EmptyPage:
        book_list = paginator.page(1)
    if paginator.num_pages > 9:
        if current_num - 4 < 1:
            pageRange = range(1, 9)
        elif current_num + 4 > paginator.num_pages:
            pageRange = range(current_num - 4, paginator.num_pages + 1)
        else:
            pageRange = range(current_num - 4, current_num + 5)
    else:
        pageRange = paginator.page_range
    data = {'book_list': book_list, 'paginator': paginator, 'current_num': current_num, 'pageRange': pageRange}
    return render(request, 'index.html', data)
