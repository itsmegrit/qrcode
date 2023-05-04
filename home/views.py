from imaplib import _Authenticator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
import pymongo
from django.http import JsonResponse
from pymongo import MongoClient
import cv2 as cv
import traceback
from pyzbar import pyzbar

# Create your views here.
client = pymongo.MongoClient(
    'mongodb+srv://ngtphongg:25251325@cluster0.yrdmc9z.mongodb.net/test')
dbname = client['QLSV']

# def Left_Menu(request):
#     NamHoc=dbname['NamHoc']
#     nam = list(NamHoc.find())
#     return render(request, 'home/LeftMenu.html', {'nam': nam})

# def ManageMonHoc(request):

#     GiangVien = dbname['GiangVien']
#     DkMonHoc = dbname['DKMonHoc']
#     MonHoc = dbname['MonHoc']

#         # Kết hợp bảng customers và orders
#     result = DkMonHoc.aggregate([
#     {
#         '$lookup':
#             {
#                 'from': 'GiangVien',
#                 'localField': 'magv',
#                 'foreignField': 'magv',
#                 'as': 'tenGV'
#             }
#     },
#     {
#         '$lookup':
#             {
#                 'from': 'MonHoc',
#                 'localField': 'mamonhoc',
#                 'foreignField': 'mamonhoc',
#                 'as': 'tenMonHoc'
#             }
#     },
#     {    '$unwind': '$tenGV',
#     },
#     {
#         '$unwind':'$tenMonHoc',
#     }
# ])
#     return render(request, 'home/TableMonHoc.html',{'result':result})


def DanhSachNhomLop(request, maMH):

    ma = maMH

    GiangDay = dbname['GiangDay1']
    NhomLop = dbname['NhomLop']
    MonHoc = dbname['MonHoc']

    # Kết hợp bảng customers và orders
    result = GiangDay.aggregate([
        {
            '$lookup':
            {
                'from': 'NhomLop',
                'localField': 'manhomlop',
                'foreignField': 'manhomlop',
                'as': 'Nhom'
            }
        },
        {
            '$lookup':
            {
                'from': 'MonHoc',
                'localField': 'mamonhoc',
                'foreignField': 'mamonhoc',
                'as': 'MonHoc'
            }
        },
        {'$unwind': '$Nhom',
         },
        {
            '$unwind': '$MonHoc',
        },
        {
            "$match": {
                "MonHoc.mamonhoc": ma
            }
        }
    ])
    return render(request, 'home/TableNhomLop.html', {'result': result})


def DanhSachSinhVien(request, maNhom):

    ma = maNhom

    ThamGiaNhom = dbname['ThamGiaNhom']
    SinhVien = dbname['SinhVien']
    NhomLop = dbname['NhomLop']

    # Kết hợp bảng customers và orders
    result = ThamGiaNhom.aggregate([
        {
            '$lookup':
            {
                'from': 'NhomLop',
                'localField': 'manhomlop',
                'foreignField': 'manhomlop',
                'as': 'Nhom'
            }
        },
        {
            '$lookup':
            {
                'from': 'SinhVien',
                'localField': 'masinhvien',
                'foreignField': 'masinhvien',
                'as': 'SV'
            }
        },
        {'$unwind': '$Nhom',
         },
        {
            '$unwind': '$SV',
        },
        {
            "$match": {
                "Nhom.manhomlop": ma
            }
        }
    ])
    return render(request, 'home/TableDSSV.html', {'result': result})


def QRcode(request, maNhom):
    ma = maNhom
    cap = cv.VideoCapture(0)
    ListMaSV = []
    while True:
        ret, frame = cap.read()
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            text = "{}".format(barcodeData)
            if text not in ListMaSV:
                ListMaSV.append(text)
            cv.putText(frame, text, (x-10, y - 10), cv.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 0, 255), 1)
        cv.imshow('Doc Ma Vach - Ma QR', frame)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
    ThamGiaNhom = dbname['ThamGiaNhom']
    NhomLop = dbname['NhomLop']
    for i in ListMaSV:
        ThamGiaNhom.update_many(
            {'masinhvien': i, 'manhomlop': ma},
            {'$set': {'diemdanh': '1'}}
        )
    ThamGiaNhom = dbname['ThamGiaNhom']
    SinhVien = dbname['SinhVien']
    NhomLop = dbname['NhomLop']

    # Kết hợp bảng customers và orders
    result = ThamGiaNhom.aggregate([
        {
            '$lookup':
            {
                'from': 'NhomLop',
                'localField': 'manhomlop',
                'foreignField': 'manhomlop',
                'as': 'Nhom'
            }
        },
        {
            '$lookup':
            {
                'from': 'SinhVien',
                'localField': 'masinhvien',
                'foreignField': 'masinhvien',
                'as': 'SV'
            }
        },
        {'$unwind': '$Nhom',
         },
        {
            '$unwind': '$SV',
        },
        {
            "$match": {
                "Nhom.manhomlop": ma
            }
        }
    ])
    print(ListMaSV)
    return render(request, 'home/TableDSSV.html', {'result': result})


def login_view(request):
    GiangVien = dbname['GiangVien']
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        query = {'username': username, 'password': password}
        tk = GiangVien.find(query, {'magv': 1})
        tk = list(tk)
        for i in tk:
            ma = i['magv']
        if len(tk) != 0:
            DkMonHoc = dbname['DKMonHoc']
            MonHoc = dbname['MonHoc']
            # Kết hợp bảng customers và orders
            result = DkMonHoc.aggregate([
                {
                    '$lookup':
                    {
                        'from': 'GiangVien',
                        'localField': 'magv',
                        'foreignField': 'magv',
                        'as': 'tenGV'
                    }
                },
                {
                    '$lookup':
                    {
                        'from': 'MonHoc',
                        'localField': 'mamonhoc',
                        'foreignField': 'mamonhoc',
                        'as': 'tenMonHoc'
                    }
                },
                {'$unwind': '$tenGV',
                 },
                {
                    '$unwind': '$tenMonHoc',
                },
                {
                    '$match': {
                        'tenGV.magv': ma
                    }
                }
            ])
            return render(request, 'home/TableMonHoc.html', {'result': result})
        else:
            error_message = 'Tên đăng nhập hoặc mật khẩu không đúng.'
            print("Bug1")
    else:
        error_message = ''
        print("Bug2")
    return render(request, 'home/Login.html', {'error_message': error_message})


def connectDB(collection_name):
    client = pymongo.MongoClient(
        'mongodb+srv://ngtphongg:25251325@cluster0.yrdmc9z.mongodb.net/test')
    db = client['QLSV']
    return db[collection_name]


def returnNMHList():
    collection = connectDB('NhomMH')
    nmh = list(collection.find({}))
    return nmh


def returnNMHList_id(NMH):
    collection = connectDB('NhomMH')
    nmh = collection.find_one({'maNMH': 1})
    return nmh


def returnMHList():
    collection = connectDB('MonHoc')
    mh = list(collection.find({}))
    return mh


def nhomLop_view(request):
    return render(request, 'home/QLNhomLop.html', {"nmh": returnNMHList()})


def connect(collection_name):
    client = pymongo.MongoClient(
        'mongodb+srv://Asahi:anhneem2p@cluster0.htoumkm.mongodb.net/?retryWrites=true&w=majority')
    db = client['table1']
    return db[collection_name]


def returnSVList():
    collection = connect('sinhvien')
    sv = list(collection.find({}))
    return sv


def returnGVList():
    collection = connectDB('GiangVien')
    gv = list(collection.find({}))
    return gv


def TableSV(request):
    return render(request, "home/TableSV.html", {"sv": returnSVList()})


def TableGV(request):
    return render(request, "home/TableGV.html", {"sv": returnSVList()})


def QLNhomLop(request):
    return render(request, 'home/QLNhomLop.html', {"nmh": returnNMHList()})


def QLMonHoc(request):
    return render(request, "home/QLMonHoc.html", {"sv": returnSVList()})


def returnNewMHH():
    collection = connectDB('NhomMH')
    return collection.find({}).sort({"maNMH": -1}).limit(1).first()


def addNhomLop(tenMH, tenGV, hocKy, namHoc):
    collection = connectDB('NhomMH')
    diemDanhcollection = connectDB('diemDanh')
    try:
        maNMH = 2
        collection.insert_one(
            {"tenMH": tenMH, "tenGV": tenGV, "danhSachSV": [{"MSSV": "3120410396", "tenSV": "Nguyễn Thanh Phong"}, {"MSSV": "3120410542", "tenSV": "Trần Minh Toàn"}], "hocKy": hocKy, "namHoc": namHoc, "maNMH": maNMH})
        nhomMH = collection.find_one({"maNMH": maNMH})
        dssv = nhomMH['danhSachSV']

        for sinh_vien in dssv:
            sinh_vien['diemDanh'] = False

        diemDanhcollection.insert_one({
            "maNMH": nhomMH['_id'],
            "danhSachDiemDanh": [
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "1"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "2"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "3"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "4"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "5"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "6"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "7"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "8"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "9"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "10"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "11"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "12"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "13"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "14"}
                },
                {
                    "danhSachSV": dssv,
                    "buoi": {"$numberInt": "15"}
                }
            ]
        }
        )
        return True
    except Exception:
        traceback.print_exc()
        return False


def themNhomLop(request):
    tenMH = request.POST.get('subject-select')
    namHoc = request.POST.get('year-entry')
    hocKy = request.POST.get('semester-select')
    tenGV = request.POST.get('teacher-select')

    if addNhomLop(tenMH, tenGV, hocKy, namHoc) == True:
        print("added")
    else:
        print("not added")
    return render(request, "home/AddNhomLop.html", {"nmh": returnNMHList(), "gv": returnGVList(), "mh": returnMHList()})


def NMH_DSSV(request, NMH):
    nmh = returnNMHList_id(NMH)
    return render(request, 'home/NMH_DSSV.html', {"nmh": nmh})
