# -*- coding: utf-8 -*-

import tablib


class ExcelWriter(object):
    """
    Excel写,支持多sheet,例子:
    ex = ExcelWriter("test.xls")
    ex.add_data("演员列表", ["姓名"], [["周星驰"], ["周润发"]])
    ex.add_data("影视列表", ["影视", "演员"], [["上海滩", "周润发"], ["大话西游", "周星驰"]])
    ex.save()

    """
    
    def __init__(self, xls_file):
        self.datas = []
        self.xls_file = xls_file
    
    def add_data(self, title, headers, rows):
        data = tablib.Dataset(title=title)
        data.headers = headers
        for row in rows:
            data.append(row)
        self.datas.append(data)
    
    def save(self):
        book = tablib.Databook(self.datas)
        with open(self.xls_file, 'wb') as f:
            f.write(book.xls)


class ExcelReader(object):
    """
    reader = ExcelReader("test.xls")
    print reader[1].headers
    for row in reader[1]:
        print row
    """
    
    def __init__(self, xls_file):
        self.xls_file = xls_file
        self.sheets = []
        self.__load_data()
    
    def __load_data(self):
        datas = tablib.Databook().load("xls", open(self.xls_file, "rb").read())
        self.sheets = datas.sheets()
    
    def __getitem__(self, index):
        assert index < len(self.sheets)
        return self.sheets[index]
    
    @property
    def sheet_count(self):
        return len(self.sheets)
