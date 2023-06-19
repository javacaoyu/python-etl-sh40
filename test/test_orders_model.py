from unittest import TestCase
from model.orders_model import OrdersModel

class TestOrdersModel(TestCase):

    def test_generate_sql(self):
        data = '{"discountRate": 1, "storeShopNo": "None", "dayOrderSeq": 37, "storeDistrict": "芙蓉区", ' \
               '"isSigned": 0, "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "undefined", ' \
               '"discount": 0, "storeID": 1766, "productCount": 1, "operatorName": "OperatorName", ' \
               '"operator": "NameStr", "storeStatus": "open", "storeOwnUserTel": 12345678910, ' \
               '"payType": "cash", "discountType": 2, "storeName": "亿户超市郭一一食品店", ' \
               '"storeOwnUserName": "OwnUserNameStr", "dateTS": 1542436490000, "smallChange": 0, ' \
               '"storeGPSName": "None", "erase": 0, "product": ' \
               '[{"count": 1, "name": "南京特醇", "unitID": 8, "barcode": "6901028300056", ' \
               '"pricePer": 12, "retailPrice": 12, "tradePrice": 11, "categoryID": 1}], ' \
               '"storeGPSAddress": "None", "orderID": "154243648991517662217", ' \
               '"moneyBeforeWholeDiscount": 12, "storeCategory": "normal", ' \
               '"receivable": 12, "faceID": "", "storeOwnUserId": 1694, ' \
               '"paymentChannel": 0, "paymentScenarios": "OTHER", "storeAddress": "StoreAddress", ' \
               '"totalNoDiscount": 12, "payedTotal": 12, "storeGPSLatitude": "undefined", ' \
               '"storeCreateDateTS": 1540793134000, "storeCity": "长沙市", "memberID": "0"}'
        model = OrdersModel(data)
        r = model.generate_insert_sql()
        excepted = "INSERT IGNORE INTO orders(order_id,store_id,store_name,store_status," \
                   "store_own_user_id,store_own_user_name,store_own_user_tel,store_category," \
                   "store_address,store_shop_no,store_province,store_city,store_district," \
                   "store_gps_name,store_gps_address,store_gps_longitude,store_gps_latitude," \
                   "is_signed,operator,operator_name,face_id,member_id,store_create_date_ts,origin," \
                   "day_order_seq,discount_rate,discount_type,discount,money_before_whole_discount," \
                   "receivable,erase,small_change,total_no_discount,pay_total,pay_type,payment_channel," \
                   "payment_scenarios,product_count,date_ts) VALUES('154243648991517662217', 1766, " \
                   "'亿户超市郭一一食品店', 'open', 1694, 'OwnUserNameStr', '12345678910', 'normal', " \
                   "'StoreAddress', NULL, '湖南省', '长沙市', '芙蓉区', NULL, NULL, NULL, NULL, 0, " \
                   "'NameStr', 'OperatorName', NULL, '0', '2018-10-29 14:05:34', NULL, 37, 1, 2, 0, " \
                   "12, 12, 0, 0, 12, 12, 'cash', 0, 'OTHER', 1, '2018-11-17 14:34:50')"

        self.assertEqual(excepted, r)

    def test_to_csv(self):
        data = '{"discountRate": 1, "storeShopNo": "None", "dayOrderSeq": 37, "storeDistrict": "芙蓉区", ' \
               '"isSigned": 0, "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "undefined", ' \
               '"discount": 0, "storeID": 1766, "productCount": 1, "operatorName": "OperatorName", ' \
               '"operator": "NameStr", "storeStatus": "open", "storeOwnUserTel": 12345678910, ' \
               '"payType": "cash", "discountType": 2, "storeName": "亿户超市郭一一食品店", ' \
               '"storeOwnUserName": "OwnUserNameStr", "dateTS": 1542436490000, "smallChange": 0, ' \
               '"storeGPSName": "None", "erase": 0, "product": [{"count": 1, "name": "南京特醇", ' \
               '"unitID": 8, "barcode": "6901028300056", "pricePer": 12, "retailPrice": 12, ' \
               '"tradePrice": 11, "categoryID": 1}], "storeGPSAddress": "None", ' \
               '"orderID": "154243648991517662217", "moneyBeforeWholeDiscount": 12, ' \
               '"storeCategory": "normal", "receivable": 12, "faceID": "", "storeOwnUserId": 1694, ' \
               '"paymentChannel": 0, "paymentScenarios": "OTHER", "storeAddress": "StoreAddress", ' \
               '"totalNoDiscount": 12, "payedTotal": 12, "storeGPSLatitude": "undefined", ' \
               '"storeCreateDateTS": 1540793134000, "storeCity": "长沙市", "memberID": "0"}'
        model = OrdersModel(data)
        r = model.to_csv()
        excepted = "1,None,37,芙蓉区,0,湖南省,0,undefined,0,1766,1,OperatorName,NameStr,open,12345678910," \
                   "cash,2,亿户超市郭一一食品店,OwnUserNameStr,1542436490000,0,None,0,None," \
                   "154243648991517662217,12,normal,12,,1694,0,OTHER,StoreAddress,12,12,undefined," \
                   "1540793134000,长沙市,0"

        self.assertEqual(excepted, r)
