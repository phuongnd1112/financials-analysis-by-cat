import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import seaborn as sns 
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


## ----------- LÀM DATAFRAME MỚI CHO AGGREGATE DATA 

new_data = pd.DataFrame() #tạo DataFrame mới; tên 'new_data' 
new_columns = ['Sector', 'Quarter', 'Agg Revenue', 'Agg Inventory'] 
for item in new_columns: 
    new_data[item] = item #tạo bốn columns mới: Sector, Quarter, Agg Revenue, Agg Inventory 

#tạo ra DataFrame aggregate của ngành bằng cách dùng list iteration với for loop: 
for sector in sector_list: 

    sectoral_div = data.loc[data['Ngành'] == sector, :] #cắt dataFrame theo ngành

    sectoral_div = sectoral_div.sort_values(['Thời điểm'], ascending=False) #sort theo thời điểm 

    #sectoral_div = sectoral_div.drop(['Mã CK', 'Sàn GD', 'Năm', 'Kỳ', 'Date'], axis=1)

    #vì cần tìm aggregate theo ngành VÀ theo thời điểm, slice dataframe một lần nữa theo thời điểm đã sort 
    for quarter_yearly in quarter_list: 
        temp_div = sectoral_div.loc[sectoral_div['Thời điểm'] == quarter_yearly]

        sum_revenue_quarter = temp_div.loc[:,'Doanh thu'].sum() #Tổng doanh thu theo ngành + quý 
        sum_inventory_quarter = temp_div.loc[:, 'Hàng tồn kho'].sum() #Tổng HTK theo ngành + quý 

        new_data = new_data.append(dict(zip(new_data.columns, [sector, quarter_yearly, sum_revenue_quarter, sum_inventory_quarter])), ignore_index=True) #tạo dictionary để thêm data vào DataFrame new_data; ignore index để reset 


## -------- TRAIN REGRESSION MODEL VOI SCIKITLEARN 

for sector in sector_list: 
    temp = new_data.loc[new_data['Sector'] == sector, :] #slice dataFrame theo ngành để iterate 

    temp['AggInvt -2'] = new_data['Agg Inventory'].shift(-2)
    temp = temp[['Agg Revenue', 'AggInvt -2']].fillna(0).astype(float) #xoá na nếu có 

    #SINGLE FEATURE REGRESSION MODEL 
    feature = temp[['AggInvt -2']] #variable x 
    outcome = temp[['Agg Revenue']] #variable y

    feature_train, feature_test, outcome_train, outcome_test = train_test_split(feature, outcome, train_size = 0.8) #cắt list data thành dữ liệu train và test để so sánh model 

    single_model = LinearRegression() 
    single_model.fit(feature_train, outcome_train) 
    single_model.score(feature_test, outcome_test) 
    y_fit = single_model.predict(feature_train) 
    test_predictions = single_model.predict(feature_test) 

    #tạo label patch cho graph 
    r_patch = mpatches.Patch(color='red', label = 'Dữ Liệu HTK Lag 2 Quý và Doanh Thu Thật')
    b_patch = mpatches.Patch(color='blue', label = 'Hồi Quy Tuyến Tính')

    #graph 1 - AggInt-2 và Agg Revenue có linear relationship không? 
    sns.set() 
    plt.figure(figsize = [10,10])
    plt.scatter(feature, outcome, color = 'red')
    plt.plot(feature_train, y_fit, color = 'blue')
    plt.xlabel('Tổng Hàng Tồn Kho Toàn Ngành, Lag 2 Quý')
    plt.ylabel('Tổng Doanh Thu Toàn Nghành Theo Quý')
    plt.title('Linear Regression của HTK Lag 2 Quý vs Doanh Thu Toàn Ngành ' + str(sector))
    plt.legend(handles = [r_patch, b_patch])
    plt.savefig('./RegressionGraphs/regression_fit/' + str(sector)) #xem dự liệu tại folder regression_fit

    #graph 2 - compare giá trị outcome của model regression hoàn hảo vs outcome của set thật 
    sns.set() 
    plt.figure(figsize = [10,10])
    plt.scatter(outcome_test, test_predictions, color='green')
    plt.xlabel('Kết Quả Doanh Thu Thật')
    plt.ylabel('Kết Quả Doanh Thu Tính Bằng Hồi Quy Tuyến Tính')
    plt.title('Kết Quả Doanh Thu Thật vs Tính Bằng Hồi Quy Tuyến Tính')
    plt.savefig('./RegressionGraphs/regression_compare/' + str(sector)) #xem dữ liệu tại folder regression_compare
