import unicodedata
import tkinter as tk
from shapely.geometry import Polygon
import numpy as np

# NTSC 采用CIE1931标准色坐标面积为0.1582，CIE1976,NTSC标准面积为0.0744；
# CIE1931的x,y坐标转化为CIE1976的u'，v‘坐标
# u’ = 4*x/(12*y-2*x+3)；u’ = 9*y/(12*y-2*x+3);x=（27 u'/ 4）/ [（9 u'/ 2）-12 v'+ 9];y=（3 v'）/ [（9 u'/ 2）-12 v'+ 9]
# NTSC1931 RGB 标准坐标
NTSC_xy = [[0.67, 0.33], [0.21, 0.71], [0.14, 0.08]]
NTSC_uv = [[0.477, 0.528], [0.076, 0.576], [0.152, 0.196]]
# BT2020色域RGB标准坐标
BT2020_xy = [[0.708, 0.292], [0.17, 0.797], [0.131, 0.046]]
BT2020_uv = [[0.557, 0.517], [0.056, 0.587], [0.159, 0.126]]
# DCI—P3色域RGB标准坐标
DCIP3_xy = [[0.68, 0.32], [0.265, 0.69], [0.15, 0.06]]
DCIP3_uv = [[0.496, 0.526], [0.099, 0.578], [0.175, 0.158]]


def is_number(s):
    try:

        float(s)

        return True

    except ValueError:

        pass

    try:

        unicodedata.numeric(s)

        return True

    except (TypeError, ValueError):

        pass

    return False


def Cal_area_2poly(data1, data2):
    """
    任意两个图形的相交面积的计算
    :param data1: 当前物体
    :param data2: 待比较的物体
    :return: 当前物体与待比较的物体的面积交集
    """

    poly1 = Polygon(data1).convex_hull  # Polygon：多边形对象
    poly2 = Polygon(data2).convex_hull

    if not poly1.intersects(poly2):
        inter_area = 0  # 如果两四边形不相交
    else:
        inter_area = poly1.intersection(poly2).area  # 相交面积
    return inter_area


def xyz_to_rgb():
    x_r = float(Var_rx.get())
    y_r = float(Var_ry.get())
    x_g = float(Var_gx.get())
    y_g = float(Var_gy.get())
    x_b = float(Var_bx.get())
    y_b = float(Var_by.get())
    wx = float(Var_wx.get())
    wy = float(Var_wy.get())

    X_W = wx / wy
    Y_W = 1
    Z_W = (1 - wx - wy) / wy

    M = create_tran_matrix(x_r, y_r, x_g, y_g, x_b, y_b)
    white_xyz = np.array([X_W, Y_W, Z_W])

    rgb_ratio = np.dot(M, white_xyz)
    red_ratio, green_ratio, blue_ratio = rgb_ratio
    print(red_ratio, green_ratio, blue_ratio)

    entry_red.set("{:.4f}".format(red_ratio))

    entry_green.set("{:.4f}".format(green_ratio))

    entry_blue.set("{:.4f}".format(blue_ratio))


def create_tran_matrix(x_r, y_r, x_g, y_g, x_b, y_b):
    X_r = x_r / y_r
    Y_r = 1
    Z_r = (1 - x_r - y_r) / y_r

    X_g = x_g / y_g
    Y_g = 1
    Z_g = (1 - x_g - y_g) / y_g

    X_b = x_b / y_b
    Y_b = 1
    Z_b = (1 - x_b - y_b) / y_b

    X_rgb = np.array([[X_r, X_g, X_b], [Y_r, Y_g, Y_b], [Z_r, Z_g, Z_b]])
    return np.linalg.inv(X_rgb)


def Calc_gamut():
    # try:
    if is_number(Var_rx.get()) and is_number(Var_ry.get()) and is_number(Var_bx.get()) and is_number(
            Var_by.get()) and is_number(Var_gx.get()) and is_number(Var_gy.get()):
        x1 = float(Var_rx.get())
        y1 = float(Var_ry.get())
        x2 = float(Var_gx.get())
        y2 = float(Var_gy.get())
        x3 = float(Var_bx.get())
        y3 = float(Var_by.get())
        # CIE1931坐标转化为CIE1976坐标
        u1 = 4 * x1 / (12 * y1 - 2 * x1 + 3)
        v1 = 9 * y1 / (12 * y1 - 2 * x1 + 3)
        u2 = 4 * x2 / (12 * y2 - 2 * x2 + 3)
        v2 = 9 * y2 / (12 * y2 - 2 * x2 + 3)
        u3 = 4 * x3 / (12 * y3 - 2 * x3 + 3)
        v3 = 9 * y3 / (12 * y3 - 2 * x3 + 3)
        Var_ru.set('{:.3}'.format(u1))
        Var_rv.set('{:.3}'.format(v1))
        Var_gu.set('{:.3}'.format(u2))
        Var_gv.set('{:.3}'.format(v2))
        Var_bu.set('{:.3}'.format(u3))
        Var_bv.set('{:.3}'.format(v3))
        sample = [[x1, y1], [x2, y2], [x3, y3]]
        sample1 = [[u1, v1], [u2, v2], [u3, v3]]
        S_sample = Cal_area_2poly(sample, sample)
        S_sample1 = Cal_area_2poly(sample1, sample1)
        print(sample, sample1)
        print('NTSC1931:%3f,NTSC1976:%3f' % (S_sample, S_sample1))
        # print(type(x1))
        S_NTSC_xy = Cal_area_2poly(NTSC_xy, NTSC_xy)
        S_NTSC_uv = Cal_area_2poly(NTSC_uv, NTSC_uv)

        S_DCIP3_xy = Cal_area_2poly(DCIP3_xy, DCIP3_xy)
        S_DCIP3_uv = Cal_area_2poly(DCIP3_uv, DCIP3_uv)
        S_BT2020_xy = Cal_area_2poly(BT2020_xy, BT2020_xy)
        S_BT2020_uv = Cal_area_2poly(BT2020_uv, BT2020_uv)
        BT2020_xy_OVERLAY = Cal_area_2poly(sample, BT2020_xy)
        BT2020_uv_OVERLAY = Cal_area_2poly(sample1, BT2020_uv)
        DCIP3_xy_OVERLAY = Cal_area_2poly(sample, DCIP3_xy)
        DCIP3_uv_OVERLAY = Cal_area_2poly(sample1, DCIP3_uv)
        NTSC_gamut_xy = S_sample / S_NTSC_xy
        NTSC_gamut_uv = S_sample1 / S_NTSC_uv
        DCIP3_gamut_xy = DCIP3_xy_OVERLAY / S_DCIP3_xy
        DCIP3_gamut_uv = DCIP3_uv_OVERLAY / S_DCIP3_uv
        BT2020_gamut_xy = BT2020_xy_OVERLAY / S_BT2020_xy
        BT2020_gamut_uv = BT2020_uv_OVERLAY / S_BT2020_uv
        result1.set('{:.2%}'.format(NTSC_gamut_xy))
        result2.set('{:.2%}'.format(DCIP3_gamut_xy))
        result3.set('{:.2%}'.format(BT2020_gamut_xy))
        result4.set('{:.2%}'.format(NTSC_gamut_uv))
        result5.set('{:.2%}'.format(DCIP3_gamut_uv))
        result6.set('{:.2%}'.format(BT2020_gamut_uv))
    # else:
    #     # print('请输入正确的坐标')
    #     Var_rx.set('')
    #     Var_ry.set('')
    #     Var_gx.set('')
    #     Var_gy.set('')
    #     Var_bx.set('')
    #     Var_by.set('')
    # except:
    elif is_number(Var_ru.get()) and is_number(Var_rv.get()) and is_number(Var_bu.get()) and is_number(
            Var_bv.get()) and is_number(Var_gu.get()) and is_number(Var_gv.get()):
        u1 = float(Var_ru.get())
        v1 = float(Var_rv.get())
        u2 = float(Var_gu.get())
        v2 = float(Var_gv.get())
        u3 = float(Var_bu.get())
        v3 = float(Var_bv.get())
        # CIE1976坐标转化为CIE1931坐标
        x1 = (27 * u1 / 4) / ((9 * u1 / 2) - 12 * v1 + 9)
        y1 = (3 * v1) / ((9 * u1 / 2) - 12 * v1 + 9)
        x2 = (27 * u2 / 4) / ((9 * u2 / 2) - 12 * v2 + 9)
        y2 = (3 * v2) / ((9 * u2 / 2) - 12 * v2 + 9)
        x3 = (27 * u3 / 4) / ((9 * u3 / 2) - 12 * v3 + 9)
        y3 = (3 * v3) / ((9 * u3 / 2) - 12 * v3 + 9)

        Var_rx.set('{:.3}'.format(x1))
        Var_ry.set('{:.3}'.format(y1))
        Var_gx.set('{:.3}'.format(x2))
        Var_gy.set('{:.3}'.format(y2))
        Var_bx.set('{:.3}'.format(x3))
        Var_by.set('{:.3}'.format(y3))
        sample = [[x1, y1], [x2, y2], [x3, y3]]
        sample1 = [[u1, v1], [u2, v2], [u3, v3]]
        S_sample = Cal_area_2poly(sample, sample)
        S_sample1 = Cal_area_2poly(sample1, sample1)
        print(sample, sample1)
        print('NTSC1931:%3f,NTSC1976:%3f' % (S_sample, S_sample1))
        # print(type(x1))
        S_NTSC_xy = Cal_area_2poly(NTSC_xy, NTSC_xy)
        S_NTSC_uv = Cal_area_2poly(NTSC_uv, NTSC_uv)

        S_DCIP3_xy = Cal_area_2poly(DCIP3_xy, DCIP3_xy)
        S_DCIP3_uv = Cal_area_2poly(DCIP3_uv, DCIP3_uv)
        S_BT2020_xy = Cal_area_2poly(BT2020_xy, BT2020_xy)
        S_BT2020_uv = Cal_area_2poly(BT2020_uv, BT2020_uv)
        BT2020_xy_OVERLAY = Cal_area_2poly(sample, BT2020_xy)
        BT2020_uv_OVERLAY = Cal_area_2poly(sample1, BT2020_uv)
        DCIP3_xy_OVERLAY = Cal_area_2poly(sample, DCIP3_xy)
        DCIP3_uv_OVERLAY = Cal_area_2poly(sample1, DCIP3_uv)
        NTSC_gamut_xy = S_sample / S_NTSC_xy
        NTSC_gamut_uv = S_sample1 / S_NTSC_uv
        DCIP3_gamut_xy = DCIP3_xy_OVERLAY / S_DCIP3_xy
        DCIP3_gamut_uv = DCIP3_uv_OVERLAY / S_DCIP3_uv
        BT2020_gamut_xy = BT2020_xy_OVERLAY / S_BT2020_xy
        BT2020_gamut_uv = BT2020_uv_OVERLAY / S_BT2020_uv
        result1.set('{:.2%}'.format(NTSC_gamut_xy))
        result2.set('{:.2%}'.format(DCIP3_gamut_xy))
        result3.set('{:.2%}'.format(BT2020_gamut_xy))
        result4.set('{:.2%}'.format(NTSC_gamut_uv))
        result5.set('{:.2%}'.format(DCIP3_gamut_uv))
        result6.set('{:.2%}'.format(BT2020_gamut_uv))
    # else:
    #     # print('请输入正确的坐标')
    #     Var_ru.set('')
    #     Var_rv.set('')
    #     Var_gu.set('')
    #     Var_gv.set('')
    #     Var_bu.set('')
    #     Var_bv.set('')


win = tk.Tk()
win.title('色域计算--Elric')

# win.geometry('300x300+500+200')
# win.resizable(0, 0)
Var_rx = tk.StringVar()
Var_ry = tk.StringVar()
Var_gx = tk.StringVar()
Var_gy = tk.StringVar()
Var_bx = tk.StringVar()
Var_by = tk.StringVar()
Var_ru = tk.StringVar()
Var_rv = tk.StringVar()
Var_gu = tk.StringVar()
Var_gv = tk.StringVar()
Var_bu = tk.StringVar()
Var_bv = tk.StringVar()
Var_wx = tk.StringVar()
Var_wy = tk.StringVar()
tk.Label(win, text='CIE1931').grid(row=0, column=1, columnspan=2)
tk.Label(win, text='CIE1976').grid(row=0, column=3, columnspan=2)
tk.Label(win, text='RGB占比').grid(row=0, column=5, columnspan=2)
tk.Label(win, text='x').grid(row=1, column=1)
tk.Label(win, text='y').grid(row=1, column=2)
tk.Label(win, text='u').grid(row=1, column=3)
tk.Label(win, text='v').grid(row=1, column=4)
tk.Label(win, text='R:').grid(row=2, column=0)
tk.Label(win, text='G:').grid(row=3, column=0)
tk.Label(win, text='B:').grid(row=4, column=0)
tk.Label(win, text='w:').grid(row=5, column=0)
tk.Entry(win, width=7, textvariable=Var_rx).grid(row=2, column=1)
tk.Entry(win, width=7, textvariable=Var_ry).grid(row=2, column=2)
tk.Entry(win, width=7, textvariable=Var_ru).grid(row=2, column=3)
tk.Entry(win, width=7, textvariable=Var_rv).grid(row=2, column=4)
tk.Entry(win, width=7, textvariable=Var_gx).grid(row=3, column=1)
tk.Entry(win, width=7, textvariable=Var_gy).grid(row=3, column=2)
tk.Entry(win, width=7, textvariable=Var_gu).grid(row=3, column=3)
tk.Entry(win, width=7, textvariable=Var_gv).grid(row=3, column=4)
tk.Entry(win, width=7, textvariable=Var_bx).grid(row=4, column=1)
tk.Entry(win, width=7, textvariable=Var_by).grid(row=4, column=2)
tk.Entry(win, width=7, textvariable=Var_bu).grid(row=4, column=3)
tk.Entry(win, width=7, textvariable=Var_bv).grid(row=4, column=4)
tk.Entry(win, width=7, textvariable=Var_wx).grid(row=5, column=1)
tk.Entry(win, width=7, textvariable=Var_wy).grid(row=5, column=2)
Var_rx.set('')
Var_ry.set('')
Var_ru.set('')
Var_rv.set('')

Var_gx.set('')
Var_gy.set('')
Var_gu.set('')
Var_gv.set('')

Var_bx.set('')
Var_by.set('')
Var_bu.set('')
Var_bv.set('')
Var_wx.set('')
Var_wy.set('')
tk.Button(win, width=10, text='Calc Gamut', command=Calc_gamut).grid(row=10, column=1)
tk.Button(win, width=10, text='RGB配比', command=xyz_to_rgb).grid(row=10, column=5)
result1 = tk.StringVar()
result2 = tk.StringVar()
result3 = tk.StringVar()
result4 = tk.StringVar()
result5 = tk.StringVar()
result6 = tk.StringVar()
entry_red = tk.StringVar()
entry_green = tk.StringVar()
entry_blue = tk.StringVar()
tk.Label(win, text='CIE1931').grid(row=6, column=0, columnspan=2)
tk.Label(win, text='CIE1976').grid(row=6, column=3, columnspan=2)
tk.Label(win, text='NTSC:\t').grid(row=7, column=0)
tk.Entry(win, width=7, textvariable=result1).grid(row=7, column=1)
tk.Label(win, text='DCI-P3:\t').grid(row=8, column=0)
tk.Entry(win, width=7, textvariable=result2).grid(row=8, column=1)
tk.Label(win, text='BT2020:\t').grid(row=9, column=0)
tk.Entry(win, width=7, textvariable=result3).grid(row=9, column=1)
tk.Label(win, text='NTSC:\t').grid(row=7, column=3)
tk.Entry(win, width=7, textvariable=result4).grid(row=7, column=4)
tk.Label(win, text='DCI-P3:\t').grid(row=8, column=3)
tk.Entry(win, width=7, textvariable=result5).grid(row=8, column=4)
tk.Label(win, text='BT2020:\t').grid(row=9, column=3)
tk.Entry(win, width=7, textvariable=result6).grid(row=9, column=4)
tk.Label(win, text='Ratio:').grid(row=1, column=5)
tk.Entry(win, width=7, textvariable=entry_red).grid(row=2, column=5)
tk.Entry(win, width=7, textvariable=entry_green).grid(row=3, column=5)
tk.Entry(win, width=7, textvariable=entry_blue).grid(row=4, column=5)
win.mainloop()
