target_barcode_table_cols_define = \
     "code varchar(50) NOT NULL COMMENT '商品条码', " \
     "name varchar(200) DEFAULT '' COMMENT '商品名称', " \
     "spec varchar(200) DEFAULT '' COMMENT '商品规格', " \
     "trademark varchar(100) DEFAULT '' COMMENT '商标', " \
     "addr varchar(200) DEFAULT '' COMMENT '厂家地址', " \
     "units varchar(50) DEFAULT '' COMMENT '单位', " \
     "factory_name varchar(200) DEFAULT '' COMMENT '厂家名称', " \
     "trade_price varchar(20) DEFAULT '0.0000' COMMENT '进价', " \
     "retail_price varchar(20) DEFAULT '0.0000' COMMENT '零售价格', " \
     "updateAt timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间', " \
     "wholeunit varchar(50) DEFAULT NULL COMMENT '计量单位', " \
     "wholenum int(11) DEFAULT NULL," \
     "img varchar(500) DEFAULT NULL COMMENT '图片', " \
     "src varchar(20) DEFAULT NULL COMMENT '图片地址', " \
     "PRIMARY KEY (`code`)"

print(target_barcode_table_cols_define)