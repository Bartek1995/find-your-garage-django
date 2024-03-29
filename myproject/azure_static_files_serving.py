import os
from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = os.environ.get('BLOB_STORAGE_ACCOUNT_NAME')
    account_key = os.environ.get('BLOB_STORAGE_ACCOUNT_KEY')
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = os.environ.get('BLOB_STORAGE_ACCOUNT_NAME')
    account_key = os.environ.get('BLOB_STORAGE_ACCOUNT_KEY')
    azure_container = 'static'
    expiration_secs = None