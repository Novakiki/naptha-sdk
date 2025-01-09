import pytest
from naptha_sdk.storage.schemas import (
    BaseStorageRequest,
    CreateStorageRequest,
    StorageType,
    StorageRequestType,
    ReadStorageRequest,
    UpdateStorageRequest,
    SearchStorageRequest
)

def test_base_storage_request():
    """Test base storage request with Pydantic V2 patterns."""
    request = BaseStorageRequest(
        request_type=StorageRequestType.READ,
        storage_type=StorageType.DATABASE,
        path="/test/path"
    )
    assert request.request_type == StorageRequestType.READ
    assert request.storage_type == StorageType.DATABASE

def test_create_storage_request():
    """Test create request with literal field."""
    request = CreateStorageRequest(
        storage_type=StorageType.DATABASE,
        path="/test/path",
        data={"test": "data"}
    )
    assert request.request_type == StorageRequestType.CREATE 

def test_read_storage_request():
    """Test read request with literal field."""
    request = ReadStorageRequest(
        storage_type=StorageType.DATABASE,
        path="/test/path"
    )
    assert request.request_type == StorageRequestType.READ

def test_update_storage_request():
    """Test update request with literal field."""
    request = UpdateStorageRequest(
        storage_type=StorageType.DATABASE,
        path="/test/path",
        data={"test": "data"}
    )
    assert request.request_type == StorageRequestType.UPDATE 

def test_search_storage_request():
    """Test search request with literal field."""
    request = SearchStorageRequest(
        storage_type=StorageType.DATABASE,
        path="/test/path",
        query="test query"
    )
    assert request.request_type == StorageRequestType.SEARCH
    assert request.query == "test query"
    assert request.query_type == "text" 