from django.shortcuts import render
from django.http import HttpResponse
import pymongo
# Create your views here.


def index(request):
    return render(request, 'pages/home.html')


client = pymongo.MongoClient(
    'mongodb+srv://ngtphongg:25251325@cluster0.yrdmc9z.mongodb.net/test')
# Define DB Name
dbname = client['managediemdanh']

# Define Collection
collection = dbname['sinhvien']

sinhvien = collection.find({})

for r in sinhvien:
    print(r['tensinhvien'])
