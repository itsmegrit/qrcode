from pymongo import MongoClient
import pymongo
import requests
from django.http import HttpResponse


client = pymongo.MongoClient(
    'mongodb+srv://ngtphongg:25251325@cluster0.yrdmc9z.mongodb.net/test')
dbname = client['QLSV']

GiangVien = dbname['GiangVien']
DkMonHoc = dbname['DKMonHoc']
MonHoc = dbname['MonHoc']
query1 = {}

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
])
for i in result:
    print(i['diemdanh'])
