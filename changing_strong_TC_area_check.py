## Library
import netCDF4 as nc
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from numpy import linspace
from numpy import meshgrid
from mpl_toolkits.axes_grid1 import make_axes_locatable  # divider = make_axes_locatable(gca); LIB
import read_bst_file2 as tc
import read_bst_file as tc2
from collections import Counter
from random import *
from matplotlib import gridspec


# pres=[]
# a=0
# for idx in range(848):
#     # print(TC[idx,3])
#     if TC[idx,3] == 50:
#         a+=1
#         pres.append(TC[idx,2])

"""
풍속 50m/s 일때 평균 기압은 986.6hPa.
"""
######################################################
"""
각 5년마다 태풍의 총 갯수
"""
TCs_yr = []
for yr in range(1980, 2020):
    letters = str(tc2.get_tc_lat_yr(yr))
    TCs_yr.append(letters.count("TC_count"))
######################################################

# MP = np.zeros([11, 17, 40])
# yr_idx = -1

# for y in range(1980, 2020):

#     NN = np.size(tc.get_tc_lon_yr(y))
#     TC = np.empty([NN, 4])
#     TC[:, 0] = tc.get_tc_lon_yr(y)
#     TC[:, 1] = tc.get_tc_lat_yr(y)
#     TC[:, 2] = tc.get_tc_pres_yr(y)
#     TC[:, 3] = tc.get_tc_wind_yr(y)
#     yr_idx += 1

#     for idx in range(NN):
#         lt_idx = -1
#         ln_idx = -1

#         for lt in range(0, 50, 5):
#             lt_idx += 1

#             if lt <= TC[idx, 1] < lt + 5:

#                 for ln in range(100, 180, 5):
#                     ln_idx += 1

#                     if ln <= TC[idx, 0] < ln + 5:

#                         if TC[idx, 2] <= 965 and TC[idx, 3] >= 50:
#                             MP[lt_idx, ln_idx, yr_idx] += 1


MP = np.zeros([10, 16, 40])  # lt, ln, yr
TOTAL_MP = np.zeros([10, 16, 40])

yr_idx = -1

for y in range(1980, 2019):
    yr_idx += 1
    TCnum = list(
        filter(lambda x: type(x) == list, tc2.get_tc_lon_yr(y))
    )  #  [i for i in A if isinstance(i, list)]
    NN = np.size(tc.get_tc_lon_yr(y))
    TC = np.empty([NN, 4])
    TC[:, 0] = tc.get_tc_lon_yr(y)
    TC[:, 1] = tc.get_tc_lat_yr(y)
    TC[:, 2] = tc.get_tc_pres_yr(y)
    TC[:, 3] = tc.get_tc_wind_yr(y)

    cc_idx = 0
    for i in range(len(TCnum)):  ## 해당년도 태풍 갯수
        for c_idx in range(TCnum[i][1]):  ## 같은 태풍 loop
            lt_idx = -1
            for lt in range(0, 50, 5):
                lt_idx += 1
                ln_idx = -1
                for ln in range(100, 180, 5):
                    ln_idx += 1
                    if (
                        lt <= TC[cc_idx + c_idx, 1] < lt + 5
                        and ln <= TC[cc_idx + c_idx, 0] < ln + 5
                    ):
                        if TC[cc_idx + c_idx, 2] <= 986.6 and TC[cc_idx + c_idx, 3] >= 50:
                            MP[lt_idx, ln_idx, yr_idx] = 1

        cc_idx = cc_idx + TCnum[i][1]
        TOTAL_MP[:, :, yr_idx] = TOTAL_MP[:, :, yr_idx] + MP[:, :, yr_idx]


#### 10년씩 평균 #####

MP_10year_mean = np.zeros([10, 16, 4])

for i in range(4):
    MP_10year_mean[:, :, i] = np.mean(TOTAL_MP[:, :, i * 10 : i * 10 + 10], axis=2)

############################################################################################
# plot
############################################################################################
fig = plt.figure(figsize=(5, 5))  ## 4,4 는 inch

for years in range(4):

    ax = fig.add_subplot(2, 2, years + 1)

    ######## MAP BASIC SETTING START ########

    map = Basemap(
        projection="merc", llcrnrlon=100, llcrnrlat=0, urcrnrlon=170, urcrnrlat=45, resolution="h"
    )
    llons, llats = np.meshgrid(range(100, 180, 5), range(0, 50, 5))
    x, y = map(llons, llats)

    map.fillcontinents(color="grey", lake_color="aqua")
    map.drawcoastlines()

    # draw lat lon label on map
    map.drawparallels(np.arange(0, 50, 10), labels=[1, 0, 0, 0])
    map.drawmeridians(np.arange(100, 180, 20), labels=[0, 0, 0, 1])
    ######## MAP BASIC SETTING END ########

    ######## DATA PLOT START ########

    map.contourf(
        x, y, MP_10year_mean[:, :, years], cmap="Reds", levels=[0, 3, 6, 9, 12, 15, 18, 21, 24]
    )
    cbar = map.colorbar()
    cbar.set_label("TCs", rotation=90, size=12)

    ######## DATA PLOT END ########

    # ######## COLORBAR SETTING START ########
    # # create an axes on the right side of ax. The width of cax will be 5%
    # # of ax and the padding between cax and ax will be fixed at 0.05 inch.

    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.1)
    #     pt,
    #     aspect=30,
    #     fraction=0.15,
    #     cax=cax,
    #     ticks=bounds,
    #     spacing="uniform",
    #     extend='both',
    #     extendfrac='auto',
    #     orientation="vertical",
    # )
    ######## COLORBAR SETTING END ########

    ######## TITLE SETTING START ########
    tcs = str(sum(TCs_yr[years * 10 : years * 10 + 10]))
    title1 = str(years * 10 + 1980)
    title2 = str(years * 10 + 1989)
    plt.title(title1 + "-" + title2 + "(" + "TCs = " + tcs + ")", fontsize=10)
    plt.suptitle("TCs Mean", fontsize=20)
    # plt.xlabel('',labelpad=10)
    # plt.ylabel('',labelpad=10)
    ######## TITLE SETTING END ########

"""
서브플롯 간격 조절
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.35)
wspace와hspace는 서브 플롯 사이에 예약 된 공간을 지정합니다. 축 너비와 높이의 비율입니다.
left,right,top 및bottom 매개 변수는 서브 플롯의 4면 위치를 지정합니다. 그것들은 그림의 너비와 높이의 분수입니다.
"""
"""
plt.subplots 함수를 써서 서브플롯을 할 경우에는
figure, axes = plt.subplots(2,2, constrained_layout=True) 이런식으로 서브풀롯 간격을 자동 적절간격 세팅
"""

fig.tight_layout()  # 자동 서브플롯 간격 안겹치게

plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, hspace=0.4, wspace=0.4)

plt.show()

