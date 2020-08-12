import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import seaborn as sns 
from pandas import ExcelWriter

#import data set
data = pd.read_csv('./Financials.csv')

##xoá null với fill void 

data = data.dropna() 

##------- SORTING DATA 
#kéo tên cột, tạo list để iterate lại lúc sau 
data_header_list = data.columns.tolist() 
#Kết quả 
"""['Mã CK', 'Tên Công ty', 'Mã ngành', 'Ngành', 'Sàn GD', 'Năm', 'Kỳ', 'Date', 'Thời điểm', 'Doanh thu', 'Giá vốn', 'Khấu hao', 'LN gộp', 'CPBH', 'CPQL', 'Chênh lệch tỷ giá đã thực hiện', 'Chênh lệch tỷ giá chưa thực hiện', 'Chi phí lãi vay', 'Lãi tiền gửi, trái tức', 'Cổ tức', 'Lãi từ công ty liên doanh', 'LNTT', 'Thuế TNDN', 'LNST', 'LNST cổ đông công ty mẹ', 'Tổng tài sản', 'Phải thu khách hàng', 'Hàng tồn kho', 'Nguyên giá TSCĐ', 'Giá trị còn lại TSCĐ', 'Xây dựng CBDD', 'Tài sản DDDH', 'CP SXKD Dở dang', 'CP XDCB Dở dang', 'Tổng vay', 'Vay ngắn hạn', 'Vay dài hạn đến hạn trả', 'Vay dài hạn', 'Vay nợ khác', 'Nợ ngắn hạn', 'Nợ dài hạn', 'Vốn CSH', 'Vốn điều lệ', 'Chênh lệch tỷ giá', 'LN chưa phân phối', 'CFO', 'CFI', 'CFF', 'Lưu chuyển tiền thuần trong kỳ']""" 

sector_list = data['Ngành'].values.tolist() #tạo list Ngành để iterate 
sector_list = list(dict.fromkeys(sector_list)) #clean list ngành để tránh lặp lại value 

quarter_list = data['Thời điểm'].values.tolist() #tạo list Quý + Năm để iterate 
quarter_list = list(dict.fromkeys(quarter_list)) #clean list ngành để tránh lặp lại value 


## ----------- LÀM DATAFRAME MỚI CHO AGGREGATE DATA 
new_data = pd.DataFrame() #tạo DataFrame mới; tên 'new_data'
new_columns = ['Sector', 'Quarter', 'Agg Revenue', 'Agg Inventory'] 
for item in new_columns: 
    new_data[item] = item #tạo bốn columns mới: Sector, Quarter, Agg Revenue, Agg Inventory 

#tạo ra DataFrame aggregate của ngành bằng cách dùng list iteration với for loop: 
for sector in sector_list: 

    sectoral_div = data.loc[data['Ngành'] == sector, :] #cắt dataFrame theo ngành

    sectoral_div = sectoral_div.sort_values(['Thời điểm'], ascending=True) #sort theo thời điểm 

    #sectoral_div = sectoral_div.drop(['Mã CK', 'Sàn GD', 'Năm', 'Kỳ', 'Date'], axis=1)

    #vì cần tìm aggregate theo ngành VÀ theo thời điểm, slice dataframe một lần nữa theo thời điểm đã sort 
    for quarter_yearly in quarter_list: 
        temp_div = sectoral_div.loc[sectoral_div['Thời điểm'] == quarter_yearly]

        sum_revenue_quarter = temp_div.loc[:,'Doanh thu'].sum() #Tổng doanh thu theo ngành + quý 
        sum_inventory_quarter = temp_div.loc[:, 'Hàng tồn kho'].sum() #Tổng HTK theo ngành + quý 

        new_data = new_data.append(dict(zip(new_data.columns, [sector, quarter_yearly, sum_revenue_quarter, sum_inventory_quarter])), ignore_index=True) #tạo dictionary để thêm data vào DataFrame new_data; ignore index để reset 


## ---------- TÍNH CORRELATION GIỮA CÁC ĐIỂM 

#tạo list để lưu giá trị tính
corr_list1=[] 
corr_list2=[]
corr_list3=[]
corr_list4=[]

#dùng for loop, iterate theo list ngành tìm correlation
for sector in sector_list: 
    temp = new_data.loc[new_data['Sector'] == sector, :] #slice data

    temp['AggInvt -1'] = new_data['Agg Inventory'].shift(-1) #tính lag quý bằng shift 
    temp['AggInvt -2'] = new_data['Agg Inventory'].shift(-2)
    temp['AggInvt -3'] = new_data['Agg Inventory'].shift(-3)
    temp = temp.dropna()

    plt.scatter(temp['AggInvt -2'], temp['Agg Revenue'])
    plt.show()

    #Tính correlation dùng numpy; [0,1] slice array 
    corr1 = np.corrcoef((temp['Agg Revenue']), (temp['Agg Inventory']))[0,1]
    corr2 = np.corrcoef((temp['Agg Revenue']), (temp['AggInvt -1']))[0,1]
    corr3 = np.corrcoef((temp['Agg Revenue']), (temp['AggInvt -2']))[0,1]
    corr4 = np.corrcoef((temp['Agg Revenue']), (temp['AggInvt -3']))[0,1]
    
    #float giá trị cho chắc 
    corr1 = float(corr1)
    corr2 = float(corr2)
    corr3 = float(corr3)
    corr4 = float(corr4)
    np.seterr(divide='ignore', invalid='ignore')
    #append list tạo sẵn với các correlation của quý lag tương ứng
    corr_list1.append(corr1)
    corr_list2.append(corr2)
    corr_list3.append(corr3)
    corr_list4.append(corr4)

#tạo ra bảng correlation mới 
corr_data = pd.DataFrame() 
corr_data['Sector'] = sector_list
corr_data['Correlation0'] = corr_list1
corr_data['Correlation1'] = corr_list2
corr_data['Correlation2'] = corr_list3
corr_data['Correlation3'] = corr_list4
corr_data = corr_data.sort_values('Correlation0', ascending = False)
corr_data.to_excel('./correlation.xlsx')
#CHECK FILE EXCEL ĐỂ XEM KẾT QUẢ 


'''UNCOMMENT ĐỂ GRAPH TỪNG SECTOR 
    x = temp.loc[:, 'Quarter']
    y1 = temp.loc[:, 'Agg Revenue']
    y2 = temp.loc[:, 'Agg Inventory']
    y3 = temp.loc[:, 'AggInvt -1']

    r_patch = mpatches.Patch(color='red', label='Doanh Thu')
    g_patch = mpatches.Patch(color='green', label='HTK')
    b_patch = mpatches.Patch(color='blue', label='HTK Lag 1 Quy')

    sns.set()
    plt.figure(figsize=(15,15))
    plt.plot(x, y1, color='red')
    plt.plot(x, y2, color='green')
    plt.plot(x, y3, color='blue')
    plt.title('Doanh Thu vs HTK Aggregate cua ' + sector)
    plt.legend(handles = [r_patch, g_patch, b_patch])
    plt.xlabel('Thời Điểm')
    plt.ylabel('Trieu VND')
    plt.savefig('./AggregateSector/lag-1/'+sector)

    sns.set()
    plt.figure(figsize=(15,15))
    plt.plot(x, y1, color='red')
    plt.plot(x, y2, color='green')
    plt.plot(x, y3, color='blue')
    plt.title('Doanh Thu vs HTK Aggregate cua ' + sector)
    plt.legend(handles = [r_patch, g_patch, b_patch])
    plt.xlabel('Thời Điểm')
    plt.ylabel('Trieu VND')
    plt.savefig('./AggregateSector/lag-2/'+sector)

    sns.set()
    plt.figure(figsize=(15,15))
    plt.plot(x, y1, color='red')
    plt.plot(x, y2, color='green')
    plt.plot(x, y4, color='purple')
    plt.title('Doanh Thu vs HTK Aggregate cua ' + sector)
    plt.legend(handles = [r_patch, g_patch, p_patch])
    plt.xlabel('Thời Điểm')
    plt.ylabel('Trieu VND')
    plt.savefig('./AggregateSector/lag-3/'+sector)'''