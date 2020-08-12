import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import seaborn as sns 
from pandas import ExcelWriter

data = pd.read_csv('./Financials.csv')

#delete null and fill void values 
data = data.dropna() 

#search columns and drop unecessary values 
data_header_list = data.columns.tolist() 

"""['Mã CK', 'Tên Công ty', 'Mã ngành', 'Ngành', 'Sàn GD', 'Năm', 'Kỳ', 'Date', 'Thời điểm', 'Doanh thu', 'Giá vốn', 'Khấu hao', 'LN gộp', 'CPBH', 'CPQL', 'Chênh lệch tỷ giá đã thực hiện', 'Chênh lệch tỷ giá chưa thực hiện', 'Chi phí lãi vay', 'Lãi tiền gửi, trái tức', 'Cổ tức', 'Lãi từ công ty liên doanh', 'LNTT', 'Thuế TNDN', 'LNST', 'LNST cổ đông công ty mẹ', 'Tổng tài sản', 'Phải thu khách hàng', 'Hàng tồn kho', 'Nguyên giá TSCĐ', 'Giá trị còn lại TSCĐ', 'Xây dựng CBDD', 'Tài sản DDDH', 'CP SXKD Dở dang', 'CP XDCB Dở dang', 'Tổng vay', 'Vay ngắn hạn', 'Vay dài hạn đến hạn trả', 'Vay dài hạn', 'Vay nợ khác', 'Nợ ngắn hạn', 'Nợ dài hạn', 'Vốn CSH', 'Vốn điều lệ', 'Chênh lệch tỷ giá', 'LN chưa phân phối', 'CFO', 'CFI', 'CFF', 'Lưu chuyển tiền thuần trong kỳ']""" 


sector_list = data['Ngành'].values.tolist()
sector_list = list(dict.fromkeys(sector_list))

quarter_list = data['Thời điểm'].values.tolist() 
quarter_list = list(dict.fromkeys(quarter_list))

new_data = pd.DataFrame() 
new_columns = ['Sector', 'Quarter', 'Agg Revenue', 'Agg Inventory'] 
for item in new_columns: 
    new_data[item] = item

for sector in sector_list: 

    sectoral_div = data.loc[data['Ngành'] == sector, :]

    sectoral_div = sectoral_div.sort_values(['Thời điểm'], ascending=True)

    sectoral_div = sectoral_div.drop(['Mã CK', 'Sàn GD', 'Năm', 'Kỳ', 'Date'], axis=1)

    for quarter_yearly in quarter_list: 
        temp_div = sectoral_div.loc[sectoral_div['Thời điểm'] == quarter_yearly]

        sum_revenue_quarter = temp_div.loc[:,'Doanh thu'].sum() 
        sum_inventory_quarter = temp_div.loc[:, 'Hàng tồn kho'].sum() 

        new_data = new_data.append(dict(zip(new_data.columns, [sector, quarter_yearly, sum_revenue_quarter, sum_inventory_quarter])), ignore_index=True)

#print(new_data)
#print(new_data.corr())
new_data['AggRevenue -1'] = new_data['Agg Revenue'].shift(-1)
new_data['AggInvt -1'] = new_data['Agg Inventory'].shift(-1)
new_data['AggRevenue -2'] = new_data['Agg Revenue'].shift(-2)
new_data['AggInvt -2'] = new_data['Agg Inventory'].shift(-2)
new_data['AggRevenue -3'] = new_data['Agg Revenue'].shift(-3)
new_data['AggInvt -3'] = new_data['Agg Inventory'].shift(-3)
#graphing sectoral relationship between revenue and inventory quarter-on-quarter
corr_list1=[]
corr_list2=[]
corr_list3=[]
corr_list4=[]

for sector in sector_list: 
    temp = new_data.loc[new_data['Sector'] == sector, :]

    temp['AggRevenue -1'] = new_data['Agg Revenue'].shift(-1)
    temp['AggInvt -1'] = new_data['Agg Inventory'].shift(-1)
    temp['AggRevenue -2'] = new_data['Agg Revenue'].shift(-2)
    temp['AggInvt -2'] = new_data['Agg Inventory'].shift(-2)
    temp['AggRevenue -3'] = new_data['Agg Revenue'].shift(-3)
    temp['AggInvt -3'] = new_data['Agg Inventory'].shift(-3)
    temp = temp.dropna()

    #corr = temp.corr()
    corr1 = np.corrcoef((temp['Agg Revenue']), (temp['Agg Inventory']))[0,1]
    corr2 = np.corrcoef((temp['Agg Revenue']), (temp['AggInvt -1']))[0,1]
    corr3 = np.corrcoef((temp['Agg Revenue']), (temp['AggInvt -2']))[0,1]
    corr4 = np.corrcoef((temp['Agg Revenue']), (temp['AggInvt -3']))[0,1]
    
    corr1 = float(corr1)
    corr2 = float(corr2)
    corr3 = float(corr3)
    corr4 = float(corr4)
    np.seterr(divide='ignore', invalid='ignore')
    corr_list1.append(corr1)
    corr_list2.append(corr2)
    corr_list3.append(corr3)
    corr_list4.append(corr4)

    plt.scatter(temp['AggInvt -2'], temp['Agg Revenue'])
    plt.show()

'''corr_data = pd.DataFrame() 
corr_data['Sector'] = sector_list
corr_data['Correlation0'] = corr_list1
corr_data['Correlation1'] = corr_list2
corr_data['Correlation2'] = corr_list3
corr_data['Correlation3'] = corr_list4
corr_data = corr_data.sort_values('Correlation0', ascending = False)
corr_data.to_excel('./correlation.xlsx')
print(corr_data)'''

'''
    writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
    df1.to_excel(writer, sheet_name = 'x1')
    df2.to_excel(writer, sheet_name = 'x2')
    writer.save()
    writer.close()
    corr.to_excel('./correlation.xlsx')'''


'''x = temp.loc[:, 'Quarter']
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