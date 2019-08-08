
class BaseDataSource:
    pass

    def get_data(self):
        pass

    def put_data(self, data):
        pass

    def copy(self, origin_datasource):
        for data in origin_datasource.get_data():
            self.put_data(data)

class HttpDataSource(BaseDataSource):
    pass

class DatabaseDataSource(BaseDataSource):
    pass
