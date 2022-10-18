'''
많이 쓰는 기능들
- 특정 년도 태풍들 or 특정 태풍들의 특정위도에서의 강도 list
- 특정 년도 태풍들 or 특정 태풍들의 LMI 강도 list
- 특정 년도 태풍들 or 특정 태풍들의 강도 dataframe

- 특정 년도 태풍들 or 특정 태풍들의 평균 트랙(시작/LMI/소멸 위치표시)


- 특정 년도 태풍들의 (발생시각{date} / 중위도도달시각{date} / 소멸시각{date}) --> date로 배경장 그리기
'''

#Intensity
class RSMC_I:
    def __init__(self, *args, t): # t=0이면 년도로 호출, t=1이면 태풍번호로 호출

        self.args = args
        self.t = t
        self.idxs = []

        #년도로 호출
        if t == 0:
            if len(args) < 3:
                self.sidx = args[0]
                self.eidx = args[-1]
                yrs = self.sidx
                for i in range(self.eidx-self.sidx+1):
                    self.idxs.append(yrs)             
                    yrs += 1

            elif len(args) >= 3:
                for i in range(len(args)):
                    self.idxs.append(args[i]) 

            return print("선택 년도: ",self.idxs)
        #태풍번호로 호출
        elif t == 1:
            if len(args) < 3:
                self.sidx = args[0]
                self.eidx = args[-1]
                yrs = self.sidx
                for i in range(self.eidx-self.sidx+1):
                    self.idxs.append(yrs)             
                    yrs += 1

            elif len(args) >= 3:
                for i in range(len(args)):
                    self.idxs.append(args[i]) 

            return print("선택 태풍번호: ",self.idxs)

    def __call__(self):
        return print("선택 년도: ",self.idxs)



    def LMI(self):
        yr_idx = self.idxs
        pLMI = []
        LMI = []
        
        with open("E:/CSL/bst_all_82.txt", "r") as f:
            for i in range(len(yr_idx)):
                yrs = yr_idx[i]

                if i == 0 :
                    line = f.readline()
                    TC_info_line = line.split()
                    TC_number = int(TC_info_line[1])
                    TC_count_num = int(TC_info_line[2])

                while TC_number != ((yrs % 100) * 100 + 1):
                    for a in range(TC_count_num):
                        line = f.readline()

                    line = f.readline()
                    TC_info_line = line.split()
                    TC_number = int(TC_info_line[1])
                    TC_count_num = int(TC_info_line[2])

                idx = int(TC_number / 100)

                if idx < 30:
                    idx += 2000
                else:
                    idx += 1900
                

                while True and yrs == idx:

                    wspd = []
                    import numpy as np
                    for i in range(TC_count_num):
                        data = f.readline()
                        spd = round(int(data.split()[6])*0.514, 2) #wspd(m/s)
                        wspd.append(spd)
                    pLMI.append(np.max(wspd))

                    line = f.readline()
                    if not line:
                        break
                    TC_info_line = line.split()
                    TC_number = int(TC_info_line[1])
                    TC_count_num = int(TC_info_line[2])

                    idx = int(TC_number / 100)
                    if idx < 30:
                        idx += 2000
                    else:
                        idx += 1900
                LMI.append(np.mean(pLMI))
        return (yr_idx, LMI)








    def LAT():

    def df():



#Track
class RSMC_T:


#Datetime
class RSMC_D:
