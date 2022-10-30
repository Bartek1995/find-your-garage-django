import os
from django.core.files.storage import Storage
from azure.storage.blob import BlobServiceClient
from django.utils.deconstruct import deconstructible
import uuid


@deconstructible
class OverwriteStorage(Storage):
    container = 'avatars'
    account_name = os.environ.get('BLOB_STORAGE_ACCOUNT_NAME')
    account_key = os.environ.get('BLOB_STORAGE_ACCOUNT_KEY')

    def __init__(self, account_name=None, account_key=None, container=None):

        if account_name is not None:
            self.account_name = account_name

        if account_key is not None:
            self.account_key = account_key

        if container is not None:
            self.container = container

    def __getstate__(self):
        return dict(
            account_name=self.account_name,
            account_key=self.account_key,
            container=self.container
        )

    def _save(self, name, content):

        generated_filename = str(uuid.uuid4())
        file_extension = os.path.splitext(name)[1]
        blob_service = self._get_service()
        import mimetypes
        content.open()
        content_type = None
        if hasattr(content.file, 'content_type'):
            content_type = content.file.content_type
        else:
            content_type = mimetypes.guess_type(name)[0]
        content_str = content.read()

        blob_service.get_blob_client(container=self.container, blob=generated_filename + file_extension).upload_blob(
            data=content_str, blob_type="BlockBlob", overwrite=True, content_type=content_type)

        content.close()
        return generated_filename + file_extension

    def exists(self, name):
        """
        Returns True if a file referenced by the given name already exists in
        the storage system, or False if the name is available for a new file.
        """
        try:
            a = self._get_properties(name)
        except:
            return False

    def delete(self, name) -> None:
        blob_service = self._get_service()
        blob_service.get_blob_client(
            container=self.container, blob=name).delete_blob()

    def _get_service(self):
        if not hasattr(self, '_blob_service'):
            self._blob_service = BlobServiceClient(
                account_name=self.account_name, account_key=self.account_key, account_url=os.environ.get('BLOB_STORAGE_ACCOUNT_URL'))
        return self._blob_service

    def _open(self, name, mode='rb'):
        from django.core.files.base import ContentFile
        contents = self._get_service().get_blob(self.container, name)
        return ContentFile(contents)

    def _get_properties(self, name):
        blob_service_properties = self._get_service().get_blob_client(
            container=self.container, blob=name).get_blob_properties()
        print('asdas')
        return blob_service_properties

    def _get_container_url(self):
        if not hasattr(self, '_container_url'):
            base_url = '{protocol}://{host}/{container}'
            if self.cdn_host:
                base_url = self.cdn_host
            self._container_url = base_url.format({
                'protocol': 'http',
                'host': self._get_service()._get_host(),
                'container': self.container,
            })
        return self._container_url

    def url(self, name):
        url = f"https://{os.environ.get('BLOB_STORAGE_ACCOUNT_NAME')}.blob.core.windows.net/{self.container}/{name}"
        return url
