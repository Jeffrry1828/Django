from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings
from django.utils.deconstruct import deconstructible


@deconstructible
class FdfsStorage(Storage):
    def open(self, name, mode='rb'):
        # 文件保存在fastdfs中，读取由fastdfs做，不需要django操作，此方法无用
        pass

    def save(self, name, content, max_length=None):
        # content:请求报文中的文件对象
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        ret = client.upload_by_buffer(content.read())
        if ret['Status'] != 'Upload successed.':
            raise Exception('文件保存失败')
        return ret['Remote file_id']

    def exists(self, name):
        return False

    def url(self, name):
        return settings.FDFS_URL + name
