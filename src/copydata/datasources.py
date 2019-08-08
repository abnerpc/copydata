
class BaseDataSource:
    config = None

    def __init__(self, config):
        self.config = config

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


MAP_TYPE_DATASOURCE = {
    "http": HttpDataSource,
    "database": DatabaseDataSource,
}


def get_data_source(_type, config):
    _class = MAP_TYPE_DATASOURCE.get(_type)
    if _class:
        return _class(config)
