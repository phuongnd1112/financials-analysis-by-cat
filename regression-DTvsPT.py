import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split 

#import data với DataFrame
data = pd.read_csv('./Financials.csv')

#xoá null với fill void 
data = data.dropna() 


## ---------- SORTING DATA 

#kéo tên cột, tạo list để iterate lại lúc sau 
data_header_list = data.columns.tolist() 
#Kết quả 
"""['Mã CK', 'Tên Công ty', 'Mã ngành', 'Ngành', 'Sàn GD', 'Năm', 'Kỳ', 'Date', 'Thời điểm', 'Doanh thu', 'Giá vốn', 'Khấu hao', 'LN gộp', 'CPBH', 'CPQL', 'Chênh lệch tỷ giá đã thực hiện', 'Chênh lệch tỷ giá chưa thực hiện', 'Chi phí lãi vay', 'Lãi tiền gửi, trái tức', 'Cổ tức', 'Lãi từ công ty liên doanh', 'LNTT', 'Thuế TNDN', 'LNST', 'LNST cổ đông công ty mẹ', 'Tổng tài sản', 'Phải thu khách hàng', 'Hàng tồn kho', 'Nguyên giá TSCĐ', 'Giá trị còn lại TSCĐ', 'Xây dựng CBDD', 'Tài sản DDDH', 'CP SXKD Dở dang', 'CP XDCB Dở dang', 'Tổng vay', 'Vay ngắn hạn', 'Vay dài hạn đến hạn trả', 'Vay dài hạn', 'Vay nợ khác', 'Nợ ngắn hạn', 'Nợ dài hạn', 'Vốn CSH', 'Vốn điều lệ', 'Chênh lệch tỷ giá', 'LN chưa phân phối', 'CFO', 'CFI', 'CFF', 'Lưu chuyển tiền thuần trong kỳ']""" 


sector_list = data['Ngành'].values.tolist() #tạo list Ngành để iterate 
sector_list = list(dict.fromkeys(sector_list)) #clean list ngành để tránh lặp lại value 

quarter_list = data['Thời điểm'].values.tolist() #tạo list Quý + Năm để iterate 
quarter_list = list(dict.fromkeys(quarter_list)) #clean list ngành để tránh lặp lại value 

# --------- SECTOR SORT 
data_sector = pd.DataFrame()
columns_list = ['Ngành', 'Thời điểm', 'Agg doanh thu', 'Agg phải thu khách hàng']
for column in columns_list: 
    data_sector[column] = column

for sector in sector_list: 
    temp = data.loc[data['Ngành'] == sector, :]

    temp = temp.sort_values('Thời điểm', ascending = False) 

    for quarter in quarter_list: 
        temp_div = temp.loc[temp['Thời điểm'] == quarter]

        sum_revenue_quarter = temp_div.loc[:,'Doanh thu'].sum() 
        sum_receivables_quarter = temp_div.loc[:,'Phải thu khách hàng'].sum() 

        data_sector = data_sector.append(dict(zip(data_sector.columns, [sector, quarter, sum_revenue_quarter, sum_receivables_quarter])), ignore_index=True)

print(data_sector.head())

train_r2 = []
test_r2 = [] 

# --------- EXPLORE CORRELATIONS AND REGRESSION 
for sector in sector_list: 
    sec_div = data_sector.loc[data_sector['Ngành'] == sector, :] 

    x = sec_div[['Agg phải thu khách hàng']]
    y = sec_div[['Agg doanh thu']]

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8) 
    #fit model 
    model = LinearRegression() 
    model.fit(x, y)
    train_predictions = model.predict(x_train) 
    test_predictions = model.predict(x_test)
    train_score = model.score(x_train, y_train) 
    test_score = model.score(x_test, y_test) 

    train_r2.append(train_score) 
    test_r2.append(test_score)

crit = pd.DataFrame() 
crit['Ngành'] = sector_list  
crit['R2 Train'] = train_r2
crit['R2 Test'] = test_r2 
crit.to_excel('./regression2 .xlsx')

''' UNCOMMENT TO GRAPH 
    b_patch = mpatches.Patch(color='blue', label='Dữ liệu doanh thu và phải thu thật')
    r_patch = mpatches.Patch(color='red', label='Regression Model Fit')

    #graph model to fit linear regression 
    sns.set() 
    plt.figure(figsize = [10,10])
    plt.scatter(x_train, y_train, color='blue', alpha = 0.4)
    plt.plot(x_train, train_predictions, color = 'red', alpha = 1.0) 
    plt.xlabel('Phải thu khách hàng')
    plt.ylabel('Doanh thu')
    plt.title('Phải thu khách hàng & doanh thu của ngành ' + str(sector))
    plt.legend(handles = [b_patch, r_patch])
    plt.savefig('./receivables_regression /regression_fit/'+str(sector)) 

    
    sns.set()  
    plt.figure(figsize = [10,10]) 
    plt.scatter(y_test, test_predictions, color = 'green', alpha = 0.5) 
    plt.xlabel('Doanh Thu Thật')
    plt.ylabel('Doanh Thu Tính Bởi Hồi Quy Tuyến Tính') 
    plt.title('Doanh Thu Thật vs Doanh Thu Tính Dựa Trên Model của Ngành ' + str(sector)) 
    plt.savefig('./receivables_regression /regression_compare/'+str(sector)) ''' 


