from django.urls import path
from . import views
from .views import DanhSachNhomLop

urlpatterns = [
    path('', views.login_view),
    path('login/', views.login_view),
    path('login/<slug:maMH>/', views.DanhSachNhomLop, name='DanhSachNhomLop'),
    path('diemdanh/<slug:maNhom>/', views.QRcode, name='QRcode'),
    path('monhoc/<slug:maNhom>/', views.DanhSachSinhVien, name='DanhSachSinhVien'),
    path('home/nhomLop/', views.nhomLop_view, name='nhomLop'),
    path('home/TableSV/', views.TableSV, name='TableSV'),
    path('home/TableGV', views.TableGV, name='TableGV'),
    path('home/nhomLop/QLMonHoc', views.QLMonHoc, name='QLMonHoc'),
    path('home/nhomLop/QLNhomLop', views.QLNhomLop, name='QLNhomLop'),
    path('home/nhomLop/AddNhomLop',
         views.themNhomLop, name='themNhomLop'),
]
