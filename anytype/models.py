from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Union, Any, Literal
from datetime import datetime
from enum import Enum

# Enums
class Color(str, Enum):
    GREY = "grey"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"
    PINK = "pink"
    PURPLE = "purple"
    BLUE = "blue"
    ICE = "ice"
    TEAL = "teal"
    LIME = "lime"

class PropertyFormat(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    FILES = "files"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    OBJECTS = "objects"

class FilterCondition(str, Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    CONTAINS = "contains"
    NCONTAINS = "ncontains"
    IN = "in"
    NIN = "nin"
    ALL = "all"
    EMPTY = "empty"
    NEMPTY = "nempty"

class FilterOperator(str, Enum):
    AND = "and"
    OR = "or"

class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"

class SortProperty(str, Enum):
    CREATED_DATE = "created_date"
    LAST_MODIFIED_DATE = "last_modified_date"
    LAST_OPENED_DATE = "last_opened_date"
    NAME = "name"

class IconFormat(str, Enum):
    EMOJI = "emoji"
    FILE = "file"
    ICON = "icon"

class ObjectLayout(str, Enum):
    BASIC = "basic"
    PROFILE = "profile"
    ACTION = "action"
    NOTE = "note"
    BOOKMARK = "bookmark"
    SET = "set"
    COLLECTION = "collection"
    PARTICIPANT = "participant"

class TypeLayout(str, Enum):
    BASIC = "basic"
    PROFILE = "profile"
    ACTION = "action"
    NOTE = "note"

class MemberRole(str, Enum):
    VIEWER = "viewer"
    EDITOR = "editor"
    OWNER = "owner"
    NO_PERMISSION = "no_permission"

class MemberStatus(str, Enum):
    JOINING = "joining"
    ACTIVE = "active"
    REMOVED = "removed"
    DECLINED = "declined"
    REMOVING = "removing"
    CANCELED = "canceled"

class ViewLayout(str, Enum):
    GRID = "grid"
    LIST = "list"
    GALLERY = "gallery"
    KANBAN = "kanban"
    CALENDAR = "calendar"
    GRAPH = "graph"

# Icon models
class EmojiIcon(BaseModel):
    format: Literal[IconFormat.EMOJI] = IconFormat.EMOJI
    emoji: str

class FileIcon(BaseModel):
    format: Literal[IconFormat.FILE] = IconFormat.FILE
    file: str

class NamedIcon(BaseModel):
    format: Literal[IconFormat.ICON] = IconFormat.ICON
    name: str
    color: Optional[Color] = None

Icon = Union[EmojiIcon, FileIcon, NamedIcon]

# Property value models
class TextPropertyValue(BaseModel):
    key: str
    text: Optional[str] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

class NumberPropertyValue(BaseModel):
    key: str
    number: Optional[float] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

class Tag(BaseModel):
    id: str
    key: str
    name: str
    color: Color
    object: Optional[str] = None

class SelectPropertyValue(BaseModel):
    key: str
    select: Optional[Tag] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

class MultiSelectPropertyValue(BaseModel):
    key: str
    multi_select: Optional[List[Tag]] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

class DatePropertyValue(BaseModel):
    key: str
    date: Optional[str] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

class FilesPropertyValue(BaseModel):
    key: str
    files: Optional[List[str]] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

class CheckboxPropertyValue(BaseModel):
    key: str
    checkbox: Optional[bool] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

class UrlPropertyValue(BaseModel):
    key: str
    url: Optional[str] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

class EmailPropertyValue(BaseModel):
    key: str
    email: Optional[str] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

class PhonePropertyValue(BaseModel):
    key: str
    phone: Optional[str] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

class ObjectsPropertyValue(BaseModel):
    key: str
    objects: Optional[List[str]] = None
    format: Optional[PropertyFormat] = None
    id: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None

PropertyWithValue = Union[
    TextPropertyValue,
    NumberPropertyValue,
    SelectPropertyValue,
    MultiSelectPropertyValue,
    DatePropertyValue,
    FilesPropertyValue,
    CheckboxPropertyValue,
    UrlPropertyValue,
    EmailPropertyValue,
    PhonePropertyValue,
    ObjectsPropertyValue
]

# Property link models for updates
class TextPropertyLink(BaseModel):
    key: str
    text: Optional[str] = None

class NumberPropertyLink(BaseModel):
    key: str
    number: Optional[float] = None

class SelectPropertyLink(BaseModel):
    key: str
    select: Optional[str] = None

class MultiSelectPropertyLink(BaseModel):
    key: str
    multi_select: Optional[List[str]] = None

class DatePropertyLink(BaseModel):
    key: str
    date: Optional[str] = None

class FilesPropertyLink(BaseModel):
    key: str
    files: Optional[List[str]] = None

class CheckboxPropertyLink(BaseModel):
    key: str
    checkbox: Optional[bool] = None

class UrlPropertyLink(BaseModel):
    key: str
    url: Optional[str] = None

class EmailPropertyLink(BaseModel):
    key: str
    email: Optional[str] = None

class PhonePropertyLink(BaseModel):
    key: str
    phone: Optional[str] = None

class ObjectsPropertyLink(BaseModel):
    key: str
    objects: Optional[List[str]] = None

PropertyLink = Union[
    TextPropertyLink,
    NumberPropertyLink,
    SelectPropertyLink,
    MultiSelectPropertyLink,
    DatePropertyLink,
    FilesPropertyLink,
    CheckboxPropertyLink,
    UrlPropertyLink,
    EmailPropertyLink,
    PhonePropertyLink,
    ObjectsPropertyLink
]

# Type model
class Type(BaseModel):
    id: str
    key: str
    name: str
    plural_name: str
    layout: TypeLayout
    icon: Optional[Icon] = None
    archived: bool = False
    object: Optional[str] = None
    properties: Optional[List[PropertyWithValue]] = None

# Object model
class Object(BaseModel):
    id: str
    name: Optional[str] = None
    icon: Optional[Icon] = None
    type: Optional[Type] = None
    space_id: str
    layout: Optional[ObjectLayout] = None
    archived: bool = False
    snippet: Optional[str] = None
    object: Optional[str] = None
    properties: Optional[List[PropertyWithValue]] = None

class ObjectWithBody(Object):
    markdown: Optional[str] = None

# Space model
class Space(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    icon: Optional[Icon] = None
    network_id: str
    gateway_url: str
    object: Optional[str] = None

# Member model
class Member(BaseModel):
    id: str
    identity: str
    name: Optional[str] = None
    global_name: Optional[str] = None
    icon: Optional[Icon] = None
    role: MemberRole
    status: MemberStatus
    object: Optional[str] = None

# Property model
class Property(BaseModel):
    id: str
    key: str
    name: str
    format: PropertyFormat
    object: Optional[str] = None

# Tag model
class Tag(BaseModel):
    id: str
    key: str
    name: str
    color: Color
    object: Optional[str] = None

# View models
class Filter(BaseModel):
    id: Optional[str] = None
    property_key: str
    condition: FilterCondition
    format: Optional[PropertyFormat] = None
    value: Optional[Any] = None

class Sort(BaseModel):
    id: Optional[str] = None
    property_key: str
    sort_type: Literal["asc", "desc", "custom"]
    format: Optional[PropertyFormat] = None

class View(BaseModel):
    id: str
    name: str
    layout: ViewLayout
    filters: Optional[List[Filter]] = None
    sorts: Optional[List[Sort]] = None

# Filter expression models
class TextFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    text: Optional[str] = None

class NumberFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    number: Optional[float] = None

class SelectFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    select: Optional[str] = None

class MultiSelectFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    multi_select: Optional[List[str]] = None

class DateFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    date: Optional[str] = None

class CheckboxFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    checkbox: Optional[bool] = None

class FilesFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    files: Optional[List[str]] = None

class UrlFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    url: Optional[str] = None

class EmailFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    email: Optional[str] = None

class PhoneFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    phone: Optional[str] = None

class ObjectsFilter(BaseModel):
    property_key: str
    condition: FilterCondition
    objects: Optional[List[str]] = None

class EmptyFilter(BaseModel):
    property_key: str
    condition: FilterCondition

FilterItem = Union[
    TextFilter,
    NumberFilter,
    SelectFilter,
    MultiSelectFilter,
    DateFilter,
    CheckboxFilter,
    FilesFilter,
    UrlFilter,
    EmailFilter,
    PhoneFilter,
    ObjectsFilter,
    EmptyFilter
]

class FilterExpression(BaseModel):
    operator: FilterOperator
    conditions: Optional[List[FilterItem]] = None
    filters: Optional[List['FilterExpression']] = None

FilterExpression.model_rebuild()

# Request/Response models
class PaginationMeta(BaseModel):
    offset: int
    limit: int
    total: int
    has_more: bool

class PaginatedResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    data: List[Any]
    pagination: PaginationMeta

class SearchRequest(BaseModel):
    query: Optional[str] = None
    types: Optional[List[str]] = None
    filters: Optional[FilterExpression] = None
    sort: Optional['SortOptions'] = None

class SortOptions(BaseModel):
    property_key: SortProperty = SortProperty.LAST_MODIFIED_DATE
    direction: SortDirection = SortDirection.DESC

class CreateObjectRequest(BaseModel):
    type_key: str
    name: Optional[str] = None
    body: Optional[str] = None
    icon: Optional[Icon] = None
    template_id: Optional[str] = None
    properties: Optional[List[PropertyLink]] = None

class UpdateObjectRequest(BaseModel):
    name: Optional[str] = None
    markdown: Optional[str] = None
    icon: Optional[Icon] = None
    type_key: Optional[str] = None
    properties: Optional[List[PropertyLink]] = None

class CreateSpaceRequest(BaseModel):
    name: str
    description: Optional[str] = None

class UpdateSpaceRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CreatePropertyRequest(BaseModel):
    name: str
    format: PropertyFormat
    key: Optional[str] = None
    tags: Optional[List['CreateTagRequest']] = None

class UpdatePropertyRequest(BaseModel):
    name: str
    key: Optional[str] = None

class CreateTagRequest(BaseModel):
    name: str
    color: Color
    key: Optional[str] = None

class UpdateTagRequest(BaseModel):
    name: Optional[str] = None
    color: Optional[Color] = None
    key: Optional[str] = None

class CreateTypeRequest(BaseModel):
    name: str
    plural_name: str
    layout: TypeLayout
    icon: Optional[Icon] = None
    key: Optional[str] = None
    properties: Optional[List[PropertyLink]] = None

class UpdateTypeRequest(BaseModel):
    name: Optional[str] = None
    plural_name: Optional[str] = None
    layout: Optional[TypeLayout] = None
    icon: Optional[Icon] = None
    key: Optional[str] = None
    properties: Optional[List[PropertyLink]] = None

class AddObjectsToListRequest(BaseModel):
    objects: List[str]

class CreateChallengeRequest(BaseModel):
    app_name: str

class CreateChallengeResponse(BaseModel):
    challenge_id: str

class CreateApiKeyRequest(BaseModel):
    challenge_id: str
    code: str

class CreateApiKeyResponse(BaseModel):
    api_key: str

# Response wrappers
class SpaceResponse(BaseModel):
    space: Space

class ObjectResponse(BaseModel):
    object: ObjectWithBody

class PropertyResponse(BaseModel):
    property: Property

class TypeResponse(BaseModel):
    type: Type

class TagResponse(BaseModel):
    tag: Tag

class MemberResponse(BaseModel):
    member: Member

class TemplateResponse(BaseModel):
    template: ObjectWithBody
