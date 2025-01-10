from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional, Union, List, Literal, BinaryIO
from io import BufferedReader, BytesIO, IOBase

class StorageType(str, Enum):
    DATABASE = "db"
    FILESYSTEM = "fs"
    IPFS = "ipfs"

class StorageLocation(BaseModel):
    storage_type: StorageType
    path: str
    options: Dict[str, Any] = Field(default_factory=dict)

    @property
    def uri(self) -> str:
        """Get URI representation of location"""
        return f"{self.storage_type.value}://{self.path}"
    
    @classmethod
    def from_uri(cls, uri: str) -> "StorageLocation":
        """Create StorageLocation from URI string"""
        scheme, path = uri.split("://", 1)
        return cls(storage_type=StorageType(scheme), path=path)

class StorageMetadata(BaseModel):
    content_type: Optional[str] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    size: Optional[int] = None
    checksum: Optional[str] = None
    tags: Dict[str, str] = Field(default_factory=dict)
    custom: Dict[str, Any] = Field(default_factory=dict)

class StorageObject(BaseModel):
    location: StorageLocation
    data: Optional[Any] = None
    metadata: StorageMetadata = Field(default_factory=StorageMetadata)

class DatabaseReadOptions(BaseModel):
    """Options specific to database reads"""
    columns: Optional[List[str]] = None
    conditions: Optional[List[Dict[str, Any]]] = None
    order_by: Optional[str] = None
    order_direction: Optional[str] = "asc"
    limit: Optional[int] = None
    offset: Optional[int] = None
    # Added fields for QA/vector search
    query_vector: Optional[List[float]] = None
    query_col: Optional[str] = None  # Column to search against
    answer_col: Optional[str] = None  # Column to return as answer
    vector_col: Optional[str] = None  # Column containing vectors
    top_k: Optional[int] = Field(default=5, ge=1)  # Number of results for vector search
    include_similarity: Optional[bool] = Field(default=True)  # Include similarity scores

class IPFSOptions(BaseModel):
    """Options specific to IPFS operations"""
    # IPNS options
    ipns_operation: Optional[Literal["create", "update", "none"]] = Field(
        default="none", 
        description="Whether to create new IPNS record, update existing, or skip IPNS"
    )
    ipns_name: Optional[str] = Field(
        None, 
        description="IPNS name to update when ipns_operation is 'update'"
    )
    
    # Pinning options
    unpin_previous: bool = Field(
        default=False, 
        description="Unpin previous hash when updating"
    )
    previous_hash: Optional[str] = Field(
        None,
        description="Previous IPFS hash to unpin when unpin_previous is True"
    )
    
    # Read options 
    resolve_ipns: bool = Field(
        default=False, 
        description="Resolve IPNS name to IPFS hash"
    )

class StorageRequestType(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LIST = "list"
    SEARCH = "search"

class BaseStorageRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "storage_type": "db",
                "path": "users",
                "options": {}
            }
        }
    )
    request_type: StorageRequestType = Field(
        json_schema_extra={"literal": True}
    )
    storage_type: StorageType
    path: str
    options: Union[Dict[str, Any], DatabaseReadOptions] = Field(default_factory=dict)

    def model_dict(self):
        model_dict = self.dict()
        if isinstance(self.options, BaseModel):
            options = self.options.model_dump()
            model_dict['options'] = options
        model_dict['storage_type'] = self.storage_type.value
        model_dict['request_type'] = self.request_type.value
        return model_dict

class CreateStorageRequest(BaseStorageRequest):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "storage_type": "db",
                "path": "users",
                "data": {"name": "test"}
            }
        }
    )
    request_type: StorageRequestType = Field(
        default=StorageRequestType.CREATE,
        json_schema_extra={"literal": True}
    )
    data: Optional[Dict[str, Any]] = None
    file: Optional[IOBase] = None

class ReadStorageRequest(BaseStorageRequest):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    request_type: StorageRequestType = Field(
        default=StorageRequestType.READ,
        json_schema_extra={"literal": True}
    )

class UpdateStorageRequest(BaseStorageRequest):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "storage_type": "db",
                "path": "users",
                "data": {"name": "updated"}
            }
        }
    )
    request_type: StorageRequestType = Field(
        default=StorageRequestType.UPDATE,
        json_schema_extra={"literal": True}
    )
    data: Union[Dict[str, Any], bytes, BinaryIO]

class DeleteStorageRequest(BaseStorageRequest):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    request_type: StorageRequestType = Field(
        default=StorageRequestType.DELETE,
        json_schema_extra={"literal": True}
    )
    condition: Optional[Dict[str, Any]] = None

class ListStorageRequest(BaseStorageRequest):
    request_type: StorageRequestType = Field(
        default=StorageRequestType.LIST,
        json_schema_extra={"literal": True}
    )

class SearchStorageRequest(BaseStorageRequest):
    request_type: StorageRequestType = Field(
        default=StorageRequestType.SEARCH,
        json_schema_extra={"literal": True}
    )
    query: Any
    query_type: str = "text"
    limit: Optional[int] = None

class StorageRequest(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "request_type": "create",
                "storage_type": "db",
                "path": "users"
            }
        }
    )
    request_type: str = Field(json_schema_extra={"literal": True})

