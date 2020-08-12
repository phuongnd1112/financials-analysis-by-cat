# Phân tích financials của các công ty theo ngành ở Việt Nam 

Repo này có tổ hợp các file python dùng để phân tích, và các chart đã được vẽ để phân tích những chỉ số đó. 
Data: financials.csv

#1. Doanh Thu vs Hàng Tồn Kho 
Phân tích Doanh Thu vs Hàng Tồn Kho của một doanh nghiệp có thể cho thấy hiệu quả hoạt động của doanh nghiệp đó. 
--- phân tích qualitative --- 
Trong phân tích này, data được tính bằng tổng số theo quý, chia theo Ngành. Dữ liệu HTK cũng đã được làm lag đi 1-2-3 quý để cho thấy ảnh hưởng của sự thay đổi của HTK đối với Doanh Thu doanh nghiệp. 

- File Correlation-DTvsHTK cho thấy sự tương quan giữa Doanh Thu và HTK
    * xem chart tại 'no lag' (không lag quý) và lag-1/2/3 (lag quý tương ứng) 
    * xem bảng correlation từng độ lag tại correlation.xlsx 
- File Regression-DTvsHTK dùng regression training model của thư viện scikitlearn để dự đoán doanh thu, nếu biết trước được HTK 
    * folder regression-fit cho thấy model dự đoán 
    * folder regression-compare so sánh Doanh thu dự đoán của training model vs doanh thu thật của các doanh nghiệp

