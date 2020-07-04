from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
def parse_province_data(data):
    provinces = df1["province"]
    provinces = list(set(provinces))
    province_list = []
    data = []
    res = {}
    for province in provinces:
        data_province = df1[df1["province"] == province]
        temp_sum = 0
        loc_counts = 0
        if province == "直辖市":
            city_names = data_province["city_name"]
            city_names = list(set(city_names))
            for city in city_names:
                data_citys = df1[df1["city_name"]==city]
                data_citys = data_citys["nhouse_price"]
                province_list.append(city)
                temp_sum = 0
                loc_counts = 0
                for data_city in data_citys:
                    if "价格待定" in data_city or "套" in data_city:
                        continue
                    elif data_city == "":
                        continue
                    else:
                        loc_counts += 1
                        data_city = data_city.split(",")
                        temp_sum += float(data_city[1])
                avg_price = temp_sum // loc_counts
                data.append(avg_price)

        else:
            province_list.append(province)
            data_province = data_province["nhouse_price"]
            for d in data_province:
                if "价格待定" in d or "套" in d:
                    continue
                elif d == "":
                    continue
                else:
                    loc_counts += 1
                    d = d.split(",")
                    temp_sum += float(d[1])
            avg_price = temp_sum // loc_counts
            data.append(avg_price)

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.style.use("ggplot")

    fig = plt.figure(figsize=(20,10))
    plt.subplot(3,1,1)
    plt.bar(x=province_list[:12],  # 指定条形图x轴的刻度值
            height=data[:12],# 指定条形图y轴的数值
            color='steelblue',# 指定条形图的填充色
            width=0.7
            )
    plt.ylabel("元/平米")
    data1 = data[:12]
    for a, b in zip(province_list[:12], data1):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    start = min(data[:31])
    end = max(data[:31])
    step = (end+1000 - start)//15
    plt.yticks(np.arange(start=start,stop=end,step=step))
    plt.title("2020房天下网站中国各省平均房价条形图")
    plt.subplot(3,1,2)
    plt.ylabel("元/平米")
    plt.bar(x=province_list[12:24],  # 指定条形图x轴的刻度值
            height=data[12:24],# 指定条形图y轴的数值
            color='steelblue',# 指定条形图的填充色
            width=0.7
            )
    data2 = data[12:24]
    for a, b in zip(province_list[12:24], data2):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    plt.yticks(np.arange(start=start,stop=end,step=step))
    plt.title("2020房天下网站中国各省平均房价条形图")
    plt.subplot(3,1,3)
    plt.bar(x=province_list[24:31],  # 指定条形图x轴的刻度值
            height=data[24:31],# 指定条形图y轴的数值
            color='steelblue',# 指定条形图的填充色
            width=0.7
            )
    plt.ylabel("元/平米")
    data3 = data[24:31]
    for a, b in zip(province_list[24:31], data3):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    plt.yticks(np.arange(start=start,stop=end,step=step))
    plt.title("2020房天下网站中国各省平均房价条形图")
    plt.savefig("1.png")
    plt.show()

new_house = pd.read_json("./newHouse.json",lines=True,encoding="utf8")
df = pd.DataFrame(new_house)
df1 = df[["city_name","province","nhouse_price"]]
parse_province_data(df1)

