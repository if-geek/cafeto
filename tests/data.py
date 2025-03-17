import uuid
import asyncio

from uuid import UUID
from abc import ABC
from datetime import date, time, datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser

from cafeto import FieldError, ModelError, Error
from cafeto.models.base_model import BaseModel, BaseValidator, validate


T = TypeVar('T')


class ChaDataRequestDto(BaseModel):
    message: str
    user: str


class ChaDataResponseDto(BaseModel):
    message: str
    user: str


class GenericResponseDto(BaseModel, Generic[T]):
    data: T


class LoginRequestDto(BaseModel):
    username: str
    password: str


class LoginResponseDto(BaseModel):
    token: str


class TokenAuthBackend(AuthenticationBackend):

    token_admin: str = 'token.admin'
    token_user: str = 'token.user'

    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]

        try:
            if auth == TokenAuthBackend.token_admin or auth == TokenAuthBackend.token_user:
                return AuthCredentials([auth.replace('token.', '')]), SimpleUser('admin')
            else:
                raise AuthenticationError('Invalid basic auth credentials')
        except Exception as e:
            raise AuthenticationError('Invalid basic auth credentials')


class ExampleSingleton:
    ...


class ExampleTransient:
    ...


class ExampleScoped:
    ...


class AGeneratorSingleton(ABC):
    def __init__(
            self,
            example_singleton: ExampleSingleton,
            other: str
            ):
        ...

class GeneratorSingleton(AGeneratorSingleton):
    def __init__(
            self,
            example_singleton: ExampleSingleton,
            other: str
            ):
        self.example_singleton: ExampleSingleton = example_singleton
        self.other: str = other


class GeneratorScoped:
    def __init__(
            self,
            example_singleton: ExampleSingleton,
            example_scoped: ExampleScoped,
            example_transient: ExampleTransient,
            other: str
            ):
        self.example_singleton: ExampleSingleton = example_singleton
        self.example_scoped: ExampleScoped = example_scoped
        self.example_transient: ExampleTransient = example_transient
        self.other: str = other


class GeneratorTransient:
    def __init__(
            self,
            example_singleton: ExampleSingleton,
            example_scoped: ExampleScoped,
            example_transient: ExampleTransient,
            other: str
            ):
        self.example_singleton: ExampleSingleton = example_singleton
        self.example_scoped: ExampleScoped = example_scoped
        self.example_transient: ExampleTransient = example_transient
        self.other: str = other


class AServiceSingleton(ABC):

    example_singleton: ExampleSingleton
    
    def __init__(self, example_singleton: ExampleSingleton, generator_singleton: AGeneratorSingleton):
        ...


class ServiceSingleton(AServiceSingleton):
    
    def __init__(self, example_singleton: ExampleSingleton, generator_singleton: AGeneratorSingleton):
        self.example_singleton = example_singleton
        self.generator_singleton = generator_singleton


class AServiceScoped(ABC):

    example_singleton: ExampleSingleton
    example_scoped: ExampleScoped
    example_transient: ExampleTransient

    def __init__(
            self,
            example_singleton: ExampleSingleton,
            example_scoped: ExampleScoped,
            example_transient: ExampleTransient,
            generator_singleton: AGeneratorSingleton,
            generator_scoped: GeneratorScoped,
            generator_transient: GeneratorTransient
            ):
        ...


class ServiceScoped(AServiceScoped):
    
    def __init__(
            self,
            example_singleton: ExampleSingleton,
            example_scoped: ExampleScoped,
            example_transient: ExampleTransient,
            generator_singleton: AGeneratorSingleton,
            generator_scoped: GeneratorScoped,
            generator_transient: GeneratorTransient
            ):
        self.example_singleton = example_singleton
        self.example_scoped = example_scoped
        self.example_transient = example_transient
        self.generator_singleton = generator_singleton
        self.generator_scoped = generator_scoped
        self.generator_transient = generator_transient



class AServiceTransient(ABC):

    example_singleton: ExampleSingleton
    example_scoped: ExampleScoped
    example_transient: ExampleTransient

    def __init__(
            self,
            example_singleton: ExampleSingleton,
            example_scoped: ExampleScoped,
            example_transient: ExampleTransient,
            generator_singleton: AGeneratorSingleton,
            generator_scoped: GeneratorScoped,
            generator_transient: GeneratorTransient
            ):
        ...


class ServiceTransient(AServiceTransient):
    
    def __init__(
            self,
            example_singleton: ExampleSingleton,
            example_scoped: ExampleScoped,
            example_transient: ExampleTransient,
            generator_singleton: AGeneratorSingleton,
            generator_scoped: GeneratorScoped,
            generator_transient: GeneratorTransient
            ):
        self.example_singleton = example_singleton
        self.example_scoped = example_scoped
        self.example_transient = example_transient
        self.generator_singleton = generator_singleton
        self.generator_scoped = generator_scoped
        self.generator_transient = generator_transient


class UServiceOriginal(ABC):
    data: str = None

    def __init__(self): ...


class ServiceOriginal(UServiceOriginal):
    def __init__(self):
        self.data: str = 'Original'

    
class ServiceOverride(UServiceOriginal):
    def __init__(self):
        self.data: str = 'Override'


class CustomUserDto(BaseModel):
    name: str
    uuid: UUID
    age: int
    balance: float
    extra_dict: Dict[str, str]
    extra_list: List[int]
    is_active: bool
    arrive_date: date
    arrive_time: time
    arrive: datetime

# region ModelDto

class ModelDto(BaseModel):
    optional_field_str: Optional[str] = None
    optional_field_date: Optional[date] = None
    optional_field_list: Optional[List[int]] = None
    optional_field_dict: Optional[Dict[str, str]] = None
    field_str: str
    field_uuid: UUID
    field_int: int
    field_float: float
    field_bool: bool
    field_dict: Dict[str, str]
    field_list: List[int]
    field_date: date
    field_time: time
    field_datetime: datetime
    field_date_list: List[date]
    field_date_dict: Dict[str, date]
    field_time_list: List[time]
    field_time_dict: Dict[str, time]
    field_datetime_list: List[datetime]
    field_datetime_dict: Dict[str, datetime]
    field_uuid_list: List[UUID]
    field_uuid_dict: Dict[str, UUID]

# endregion


# region ModelDependencyInjectionDto

class ModelDependencyInjectionDto(ModelDto):
    @validate()
    def validate_model(data: Dict[str, Any], generator_scoped: GeneratorScoped) -> Dict[str, Any]:
        data['optional_field_str'] = generator_scoped.other
        return data

# endregion


# region ModelRaiseErrorDto

class ModelRaiseErrorDto(ModelDto):
    @validate()
    def validate_model(data: Dict[str, Any]) -> Dict[str, Any]:
        error_date_list = Error('type-field_date_list', 'Model error', ['field_date_list', 0])
        error_date_dict = Error('type-field_date_dict', 'Model error', ['field_date_dict', 'key1'])
        raise ModelError([Error('type-model', 'Model error'), error_date_list, error_date_dict])

    @validate('field_str')
    def validate_field_str(value: str, _: Dict[str, Any]) -> str:
        raise FieldError(Error('type-field_str', 'field_str error'))
    
    @validate('field_uuid')
    def validate_field_uuid(value: UUID, _: Dict[str, Any]) -> str:
        raise FieldError(Error('type-field_uuid', 'field_uuid error', 'field_uuid'))
    
    @validate('field_int')
    async def validate_field_int(value: int, _: Dict[str, Any]) -> int:
        await asyncio.sleep(0.1)
        raise FieldError(Error('type-field_int', 'field_int error'))
    
    @validate('field_float')
    def validate_field_float(value: float, _: Dict[str, Any]) -> float:
        raise FieldError(Error('type-field_float', 'field_float error'))
    
    @validate('field_bool')
    def validate_field_bool(value: bool, _: Dict[str, Any]) -> bool:
        raise FieldError(Error('type-field_bool', 'field_bool error'))
    
    @validate('field_dict')
    def validate_field_dict(value: Dict[str, str], _: Dict[str, Any]) -> Dict[str, str]:
        raise FieldError(Error('type-field_dict', 'field_dict error'))
    
    @validate('field_list')
    def validate_field_list(value: List[int], _: Dict[str, Any]) -> List[int]:
        raise FieldError(Error('type-field_list', 'field_list error'))
    
    @validate('field_date')
    def validate_field_date(value: date, _: Dict[str, Any]) -> date:
        raise FieldError(Error('type-field_date', 'field_date error'))
    
    @validate('field_time')
    def validate_field_time(value: time, _: Dict[str, Any]) -> time:
        raise FieldError(Error('type-time', 'field_time error'))
    
    @validate('field_datetime')
    def validate_field_datetime(value: datetime, _: Dict[str, Any]) -> datetime:
        raise FieldError(Error('type-field_datetime', 'field_datetime error'))
    
    @validate('field_date_list')
    def validate_field_date_list(value: List[date], _: Dict[str, Any]) -> List[date]:
        raise FieldError(Error('type-field_date_list', 'field_date_list error'))
    
    @validate('field_date_dict')
    def validate_field_date_dict(value: Dict[str, date], _: Dict[str, Any]) -> Dict[str, date]:
        raise FieldError(Error('type-field_date_dict', 'field_date_dict error'))
    
    @validate('field_time_list')
    def validate_field_time_list(value: List[time], _: Dict[str, Any]) -> List[time]:
        raise FieldError(Error('type-field_time_list', 'field_time_list error'))
    
    @validate('field_time_dict')
    def validate_field_time_dict(value: Dict[str, time], _: Dict[str, Any]) -> Dict[str, time]:
        raise FieldError(Error('type-field_time_dict', 'field_time_dict error'))
    
    @validate('field_datetime_list')
    def validate_field_datetime_list(value: List[datetime], _: Dict[str, Any]) -> List[datetime]:
        raise FieldError(Error('type-field_datetime_list', 'field_datetime_list error'))
    
    @validate('field_datetime_dict')
    def validate_field_datetime_dict(value: Dict[str, datetime], _: Dict[str, Any]) -> Dict[str, datetime]:
        raise FieldError(Error('type-field_datetime-dict', 'field_datetime_dict error'))
    
    @validate('field_uuid_list')
    def validate_field_uuid_list(value: List[UUID], _: Dict[str, Any]) -> List[UUID]:
        raise FieldError(Error('type-field_uuid_list', 'field_uuid_list error'))
    
    @validate('field_uuid_dict')
    def validate_field_uuid_dict(value: Dict[str, UUID], _: Dict[str, Any]) -> Dict[str, UUID]:
        raise FieldError(Error('type-field_uuid_dict', 'field_uuid_dict error'))
    
# endregion


# region ModelRaiseErrorValidator

class ModelRaiseErrorValidator(BaseValidator):
    @validate()
    def validate_model(data: Dict[str, Any]) -> Dict[str, Any]:
        error_date_list = Error('type-field_date_list', 'Model error', ['field_date_list', 0])
        error_date_dict = Error('type-field_date_dict', 'Model error', ['field_date_dict', 'key1'])
        raise ModelError([Error('type-model', 'Model error'), error_date_list, error_date_dict])

    @validate('field_str')
    def validate_field_str(value: str, _: Dict[str, Any]) -> str:
        raise FieldError(Error('type-field_str', 'field_str error'))
    
    @validate('field_uuid')
    def validate_field_uuid(value: UUID, _: Dict[str, Any]) -> str:
        raise FieldError(Error('type-field_uuid', 'field_uuid error', 'field_uuid'))
    
    @validate('field_int')
    async def validate_field_int(value: int, _: Dict[str, Any]) -> int:
        await asyncio.sleep(0.1)
        raise FieldError(Error('type-field_int', 'field_int error'))
    
    @validate('field_float')
    def validate_field_float(value: float, _: Dict[str, Any]) -> float:
        raise FieldError(Error('type-field_float', 'field_float error'))
    
    @validate('field_bool')
    def validate_field_bool(value: bool, _: Dict[str, Any]) -> bool:
        raise FieldError(Error('type-field_bool', 'field_bool error'))
    
    @validate('field_dict')
    def validate_field_dict(value: Dict[str, str], _: Dict[str, Any]) -> Dict[str, str]:
        raise FieldError(Error('type-field_dict', 'field_dict error'))
    
    @validate('field_list')
    def validate_field_list(value: List[int], _: Dict[str, Any]) -> List[int]:
        raise FieldError(Error('type-field_list', 'field_list error'))
    
    @validate('field_date')
    def validate_field_date(value: date, _: Dict[str, Any]) -> date:
        raise FieldError(Error('type-field_date', 'field_date error'))
    
    @validate('field_time')
    def validate_field_time(value: time, _: Dict[str, Any]) -> time:
        raise FieldError(Error('type-time', 'field_time error'))
    
    @validate('field_datetime')
    def validate_field_datetime(value: datetime, _: Dict[str, Any]) -> datetime:
        raise FieldError(Error('type-field_datetime', 'field_datetime error'))
    
    @validate('field_date_list')
    def validate_field_date_list(value: List[date], _: Dict[str, Any]) -> List[date]:
        raise FieldError(Error('type-field_date_list', 'field_date_list error'))
    
    @validate('field_date_dict')
    def validate_field_date_dict(value: Dict[str, date], _: Dict[str, Any]) -> Dict[str, date]:
        raise FieldError(Error('type-field_date_dict', 'field_date_dict error'))
    
    @validate('field_time_list')
    def validate_field_time_list(value: List[time], _: Dict[str, Any]) -> List[time]:
        raise FieldError(Error('type-field_time_list', 'field_time_list error'))
    
    @validate('field_time_dict')
    def validate_field_time_dict(value: Dict[str, time], _: Dict[str, Any]) -> Dict[str, time]:
        raise FieldError(Error('type-field_time_dict', 'field_time_dict error'))
    
    @validate('field_datetime_list')
    def validate_field_datetime_list(value: List[datetime], _: Dict[str, Any]) -> List[datetime]:
        raise FieldError(Error('type-field_datetime_list', 'field_datetime_list error'))
    
    @validate('field_datetime_dict')
    def validate_field_datetime_dict(value: Dict[str, datetime], _: Dict[str, Any]) -> Dict[str, datetime]:
        raise FieldError(Error('type-field_datetime-dict', 'field_datetime_dict error'))
    
    @validate('field_uuid_list')
    def validate_field_uuid_list(value: List[UUID], _: Dict[str, Any]) -> List[UUID]:
        raise FieldError(Error('type-field_uuid_list', 'field_uuid_list error'))
    
    @validate('field_uuid_dict')
    def validate_field_uuid_dict(value: Dict[str, UUID], _: Dict[str, Any]) -> Dict[str, UUID]:
        raise FieldError(Error('type-field_uuid_dict', 'field_uuid_dict error'))

# endregion
    

# region ModelAlterDataDto

class ModelAlterDataDto(ModelDto):

    @validate()
    def validate_model(data: Dict[str, Any]) -> Dict[str, Any]:
        data['optional_field_str'] = 'Model'
        return data
    
    @validate('field_str')
    def validate_field_str(value: str, _: Dict[str, Any]) -> str:
        return value + '!'
    
    @validate('field_int')
    def validate_field_int(value: int, _: Dict[str, Any]) -> int:
        return value + 1
    
    @validate('field_float')
    def validate_field_float(value: float, _: Dict[str, Any]) -> float:
        return value + 10.0
    
    @validate('field_bool')
    def validate_field_bool(value: bool, _: Dict[str, Any]) -> bool:
        return not value
    
    @validate('field_dict')
    def validate_field_dict(value: Dict[str, str], _: Dict[str, Any]) -> Dict[str, str]:
        return {k: v + '!' for k, v in value.items()}
    
    @validate('field_list')
    def validate_field_list(value: List[int], _: Dict[str, Any]) -> List[int]:
        return [v + 1 for v in value]
    
    @validate('field_date')
    def validate_field_date(value: date, _: Dict[str, Any]) -> date:
        return value.replace(year=value.year + 1)
    
    @validate('field_time')
    def validate_field_time(value: time, _: Dict[str, Any]) -> time:
        return value.replace(hour=value.hour + 1)
    
    @validate('field_datetime')
    def validate_field_datetime(value: datetime, _: Dict[str, Any]) -> datetime:
        return value.replace(year=value.year + 1)
    
    @validate('field_date_list')
    def validate_field_date_list(value: List[date], _: Dict[str, Any]) -> List[date]:
        return [v.replace(year=v.year + 1) for v in value]
    
    @validate('field_date_dict')
    def validate_field_date_dict(value: Dict[str, date], _: Dict[str, Any]) -> Dict[str, date]:
        return {k: v.replace(year=v.year + 1) for k, v in value.items()}
    
    @validate('field_time_list')
    def validate_field_time_list(value: List[time], _: Dict[str, Any]) -> List[time]:
        return [v.replace(hour=v.hour + 1) for v in value]
    
    @validate('field_time_dict')
    def validate_field_time_dict(value: Dict[str, time], _: Dict[str, Any]) -> Dict[str, time]:
        return {k: v.replace(hour=v.hour + 1) for k, v in value.items()}
    
    @validate('field_datetime_list')
    def validate_field_datetime_list(value: List[datetime], _: Dict[str, Any]) -> List[datetime]:
        return [v.replace(year=v.year + 1, hour=v.hour + 1) for v in value]
    
    @validate('field_datetime_dict')
    def validate_field_datetime_dict(value: Dict[str, datetime], _: Dict[str, Any]) -> Dict[str, datetime]:
        return {k: v.replace(year=v.year + 1, hour=v.hour + 1) for k, v in value.items()}
    
    @validate('field_uuid_list')
    def validate_field_uuid_list(value: List[UUID], _: Dict[str, Any]) -> List[UUID]:
        return [uuid.uuid4() for _ in value]
    
    @validate('field_uuid_dict')
    def validate_field_uuid_dict(value: Dict[str, UUID], _: Dict[str, Any]) -> Dict[str, UUID]:
        return {k: uuid.uuid4() for k, v in value.items()}
    
# endregion


# region ModelAlterDataValidator

class ModelAlterDataValidator(BaseValidator):

    @validate()
    def validate_model(data: Dict[str, Any]) -> Dict[str, Any]:
        data['optional_field_str'] = 'Model'
        return data
    
    @validate('field_str')
    def validate_field_str(value: str, _: Dict[str, Any]) -> str:
        return value + '!'
    
    @validate('field_int')
    def validate_field_int(value: int, _: Dict[str, Any]) -> int:
        return value + 1
    
    @validate('field_float')
    def validate_field_float(value: float, _: Dict[str, Any]) -> float:
        return value + 10.0
    
    @validate('field_bool')
    def validate_field_bool(value: bool, _: Dict[str, Any]) -> bool:
        return not value
    
    @validate('field_dict')
    def validate_field_dict(value: Dict[str, str], _: Dict[str, Any]) -> Dict[str, str]:
        return {k: v + '!' for k, v in value.items()}
    
    @validate('field_list')
    def validate_field_list(value: List[int], _: Dict[str, Any]) -> List[int]:
        return [v + 1 for v in value]
    
    @validate('field_date')
    def validate_field_date(value: date, _: Dict[str, Any]) -> date:
        return value.replace(year=value.year + 1)
    
    @validate('field_time')
    def validate_field_time(value: time, _: Dict[str, Any]) -> time:
        return value.replace(hour=value.hour + 1)
    
    @validate('field_datetime')
    def validate_field_datetime(value: datetime, _: Dict[str, Any]) -> datetime:
        return value.replace(year=value.year + 1)
    
    @validate('field_date_list')
    def validate_field_date_list(value: List[date], _: Dict[str, Any]) -> List[date]:
        return [v.replace(year=v.year + 1) for v in value]
    
    @validate('field_date_dict')
    def validate_field_date_dict(value: Dict[str, date], _: Dict[str, Any]) -> Dict[str, date]:
        return {k: v.replace(year=v.year + 1) for k, v in value.items()}
    
    @validate('field_time_list')
    def validate_field_time_list(value: List[time], _: Dict[str, Any]) -> List[time]:
        return [v.replace(hour=v.hour + 1) for v in value]
    
    @validate('field_time_dict')
    def validate_field_time_dict(value: Dict[str, time], _: Dict[str, Any]) -> Dict[str, time]:
        return {k: v.replace(hour=v.hour + 1) for k, v in value.items()}
    
    @validate('field_datetime_list')
    def validate_field_datetime_list(value: List[datetime], _: Dict[str, Any]) -> List[datetime]:
        return [v.replace(year=v.year + 1, hour=v.hour + 1) for v in value]
    
    @validate('field_datetime_dict')
    def validate_field_datetime_dict(value: Dict[str, datetime], _: Dict[str, Any]) -> Dict[str, datetime]:
        return {k: v.replace(year=v.year + 1, hour=v.hour + 1) for k, v in value.items()}
    
    @validate('field_uuid_list')
    def validate_field_uuid_list(value: List[UUID], _: Dict[str, Any]) -> List[UUID]:
        return [uuid.uuid4() for _ in value]
    
    @validate('field_uuid_dict')
    def validate_field_uuid_dict(value: Dict[str, UUID], _: Dict[str, Any]) -> Dict[str, UUID]:
        return {k: uuid.uuid4() for k, v in value.items()}

# endregion


# region ExtraModelDto

class ExtraModelDto(ModelDto):
    field_model: ModelDto
    field_model_list: List[ModelDto] = None
    field_model_dict: Dict[str, ModelDto] = None


# endregion


# region ExtraModelPydanticValidationsDto

class ExtraModelPydanticValidationsDto(BaseModel):
    field_model: ModelDto
    field_model_list: List[ModelDto]
    field_model_dict: Dict[str, ModelDto]

# endregion


# region ExtraModelAlterDataDto

class ExtraModelAlterDataDto(ModelAlterDataDto):

    field_model: ModelAlterDataDto
    field_model_list: Optional[List[ModelAlterDataDto]] = None
    field_model_dict: Optional[Dict[str, ModelAlterDataDto]] = None

    @validate()
    async def validate_model(data: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        data['optional_field_str'] = 'Model'
        return data

    @validate('field_model')
    def validate_field_model(value: ModelAlterDataDto, _: Dict[str, Any]) -> ModelAlterDataDto:
        return value

# endregion


# region ExtraModelAlterDataValidator

class ExtraModelAlterDataValidator(ModelAlterDataValidator):

    field_model: ModelAlterDataValidator
    field_model_list: ModelAlterDataValidator
    field_model_dict: ModelAlterDataValidator

    @validate('field_str')
    def validate_field_str(value: str, _: Dict[str, Any]) -> str:
        return value + '!'

# endregion


# region ExtraModelRaiseErrorDto

class ExtraModelRaiseErrorDto(ModelRaiseErrorDto):

    field_model: ModelRaiseErrorDto
    field_model_list: List[ModelRaiseErrorDto] = None
    field_model_dict: Dict[str, ModelRaiseErrorDto] = None

# endregion


# region ExtraModelRaiseErrorDto

class ExtraModelRaiseErrorValidator(ModelRaiseErrorValidator):

    field_model: ModelRaiseErrorValidator
    field_model_list: ModelRaiseErrorValidator
    field_model_dict: ModelRaiseErrorValidator

# endregion




def is_uuid(uuid_str: str) -> bool:
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return str(uuid_obj) == uuid_str.lower()
    except ValueError:
        return False


def datetime_seed(seed: int) -> str:
    return f'0{seed}' if seed < 10 else str(seed)


def generate_model_data(seed: int, len_list_dict: int = 2) -> Dict[str, Any]:
    return {
        'field_str': f'Hello {seed}',
        'field_uuid': str(uuid.uuid4()),
        'field_int': seed,
        'field_float': seed / 5.0,
        'field_dict': {f'key {i}': f'value {i}' for i in range(1, len_list_dict + 1)},
        'field_list': [i for i in range(1, len_list_dict + 1)],
        'field_bool': seed % 2 == 0,
        'field_date': f'20{datetime_seed(seed)}-01-01',
        'field_time': f'{datetime_seed(seed)}:00:00',
        'field_datetime': f'20{datetime_seed(seed)}-01-01T{datetime_seed(seed)}:00:00',
        'field_date_list': [f'20{datetime_seed(i)}-01-01' for i in range(1, len_list_dict + 1)],
        'field_date_dict': {f'key{i}': f'20{datetime_seed(i)}-01-01' for i in range(1, len_list_dict + 1)},
        'field_time_list': [f'{datetime_seed(i)}:00:00' for i in range(1, len_list_dict + 1)],
        'field_time_dict': {f'key{i}': f'{datetime_seed(i)}:00:00' for i in range(1, len_list_dict + 1)},
        'field_datetime_list': [f'20{datetime_seed(i)}-01-01T{datetime_seed(i)}:00:00' for i in range(1, len_list_dict + 1)],
        'field_datetime_dict': {f'key{i}': f'20{datetime_seed(i)}-01-01T{datetime_seed(i)}:00:00' for i in range(1, len_list_dict + 1)},
        'field_uuid_list': [str(uuid.uuid4()) for _ in range(1, len_list_dict + 1)],
        'field_uuid_dict': {f'key {i}': str(uuid.uuid4()) for i in range(1, len_list_dict + 1)}
    }


def generate_extra_model_data(seed: int, len_list_dict: int = 2) -> Dict[str, Any]:
    data = generate_model_data(seed, len_list_dict)
    data.update({
        'field_model': generate_model_data(seed, len_list_dict),
        'field_model_list': [generate_model_data(i, len_list_dict) for i in range(1, len_list_dict + 1)],
        'field_model_dict': {f'key {i}': generate_model_data(i, len_list_dict) for i in range(1, len_list_dict + 1)},
    })

    return data


def assert_model(data: Dict[str, Any], seed: int, len_list_dict: int = 2):
    assert data['field_str'] == f'Hello {seed}'
    assert is_uuid(data['field_uuid'])
    assert data['field_int'] == seed
    assert data['field_float'] == seed / 5.0
    assert data['field_bool'] == (seed % 2 == 0)
    assert data['field_dict'] == {f'key {i}': f'value {i}' for i in range(1, len_list_dict + 1)}
    assert data['field_list'] == [i for i in range(1, len_list_dict + 1)]
    assert data['field_date'] == f'20{datetime_seed(seed)}-01-01'
    assert data['field_time'] == f'{datetime_seed(seed)}:00:00'
    assert data['field_datetime'] == f'20{datetime_seed(seed)}-01-01T{datetime_seed(seed)}:00:00'
    for i in range(1, len_list_dict + 1):
        assert data['field_date_list'][i - 1] == f'20{datetime_seed(i)}-01-01'
        assert data['field_date_dict'][f'key{i}'] == f'20{datetime_seed(i)}-01-01'
        assert data['field_time_list'][i - 1] == f'{datetime_seed(i)}:00:00'
        assert data['field_time_dict'][f'key{i}'] == f'{datetime_seed(i)}:00:00'
        assert data['field_datetime_list'][i - 1] == f'20{datetime_seed(i)}-01-01T{datetime_seed(i)}:00:00'
        assert data['field_datetime_dict'][f'key{i}'] == f'20{datetime_seed(i)}-01-01T{datetime_seed(i)}:00:00'
        assert is_uuid(data['field_uuid_list'][i - 1])
        assert is_uuid(data['field_uuid_dict'][f'key {i}'])


def assert_extra_model(data: Dict[str, Any], seed: int, len_list_dict: int = 2):
    assert_model(data, seed, len_list_dict)
    assert_model(data['field_model'], seed, len_list_dict)
    for i in range(1, len_list_dict + 1):
        assert_model(data['field_model_list'][i - 1], i, len_list_dict)
        assert_model(data['field_model_dict'][f'key {i}'], i, len_list_dict)


def assert_model_alter_data(data: Dict[str, Any], seed: int, len_list_dict: int = 2):
    assert data['optional_field_str'] == 'Model'
    assert data['field_str'] == f'Hello {seed}!'
    assert data['field_int'] == seed + 1
    assert data['field_float'] == (seed / 5.0) + 10.0
    assert data['field_bool'] == (not (seed % 2 == 0))
    assert data['field_dict'] == {f'key {i}': f'value {i}!' for i in range(1, len_list_dict + 1)}
    assert data['field_list'] == [i + 1 for i in range(1, len_list_dict + 1)]

    date_value = date.fromisoformat(data['field_date'])
    date_value.replace(year=date_value.year + 1)
    assert data['field_date'] == date_value.isoformat()

    time_value = time.fromisoformat(data['field_time'])
    time_value.replace(hour=time_value.hour + 1)
    assert data['field_time'] == time_value.isoformat()

    datetime_value = datetime.fromisoformat(data['field_datetime'])
    datetime_value.replace(year=datetime_value.year + 1)
    assert data['field_datetime'] == datetime_value.isoformat()

    for i in range(1, len_list_dict + 1):
        assert data['field_date_list'][i - 1] == f'20{datetime_seed(i + 1)}-01-01'
        assert data['field_date_dict'][f'key{i}'] == f'20{datetime_seed(i + 1)}-01-01'
        assert data['field_time_list'][i - 1] == f'{datetime_seed(i + 1)}:00:00'
        assert data['field_time_dict'][f'key{i}'] == f'{datetime_seed(i + 1)}:00:00'
        assert data['field_datetime_list'][i - 1] == f'20{datetime_seed(i + 1)}-01-01T{datetime_seed(i + 1)}:00:00'
        assert data['field_datetime_dict'][f'key{i}'] == f'20{datetime_seed(i + 1)}-01-01T{datetime_seed(i + 1)}:00:00'


def assert_extra_model_alter_data(data: Dict[str, Any], seed: int, len_list_dict: int = 2):
    assert_model_alter_data(data, seed, len_list_dict)
    assert_model_alter_data(data['field_model'], seed, len_list_dict)
    for i in range(1, len_list_dict + 1):
        assert_model_alter_data(data['field_model_list'][i - 1], i, len_list_dict)
        assert_model_alter_data(data['field_model_dict'][f'key {i}'], i, len_list_dict)


def assert_model_raise_error(data: List[Dict[str, Any]], loc: List[str] = []):
    fields: List[str] = [
        'field_str', 'field_uuid', 'field_int', 'field_float', 'field_bool', 'field_dict', 'field_list',
        'field_date', 'field_time', 'field_datetime', 'field_date_list', 'field_date_dict', 'field_time_list',
        'field_time_dict', 'field_datetime_list', 'field_datetime_dict', 'field_uuid_list', 'field_uuid_dict'
    ]

    for field in fields:
        any(loc + [field] == error['loc'] and f'type-{field}' == error['type'] for error in data)

    field_model = {
        'loc': loc + ['__model__'],
        'type': 'type-model',
        'msg': 'Model error'
    }
    assert field_model in data

    field_model_list_0 = {
        'type': 'type-field_date_list',
        'msg': 'Model error',
        'loc': loc + ['field_date_list', 0]
    }
    assert field_model_list_0 in data

    field_model_dict_key1 = {
        'type': 'type-field_date_dict',
        'msg': 'Model error',
        'loc': loc + ['field_date_dict', 'key1']
    }
    assert field_model_dict_key1 in data


def assert_pydantic_model_raise_error(data: List[Dict[str, Any]], loc: List[str] = []):
    fields: List[str] = [
        'field_str', 'field_uuid', 'field_int', 'field_float', 'field_bool', 'field_dict', 'field_list',
        'field_date', 'field_time', 'field_datetime', 'field_date_list', 'field_date_dict', 'field_time_list',
        'field_time_dict', 'field_datetime_list', 'field_datetime_dict', 'field_uuid_list', 'field_uuid_dict'
    ]

    for field in fields:
        any(loc + [field] == error['loc'] and 'missing' == error['type'] for error in data)

def assert_extra_model_raise_error(data: List[Dict[str, Any]], len_list_dict: int = 2):
    assert_model_raise_error(data)
    assert_model_raise_error(data, ['field_model'])
    for i in range(1, len_list_dict + 1):
        assert_model_raise_error(data, ['field_model_list', i - 1])
        assert_model_raise_error(data, ['field_model_dict', f'key {i}'])


def error_object_style():
    error = {}

    fields: List[str] = [
        'field_str', 'field_uuid', 'field_int', 'field_float', 'field_bool', 'field_dict', 'field_list',
        'field_date', 'field_time', 'field_datetime', 'field_date_list', 'field_date_dict', 'field_time_list',
        'field_time_dict', 'field_datetime_list', 'field_datetime_dict', 'field_uuid_list', 'field_uuid_dict'
    ]

    for field in fields:
        error[field] = {
            'msg': f'{field} error',
            'type': f'type-{field}'
        }

    error.update({
        '__model__': {
            'type': 'type-model',
            'msg': 'Model error'
        },
        'field_date_list': {
            0: {
                'type': 'type-field_date_list',
                'msg': 'Model error'
            }
        },
        'field_date_dict': {
            'key1': {
                'type': 'type-field_date_dict',
                'msg': 'Model error'
            }
        }
    })
    
    return error

def assert_model_raise_error_object_style(data: List[Dict[str, Any]]):
    error = error_object_style()
    assert error == data


def assert_extra_model_raise_error_object_style(data: List[Dict[str, Any]], len_list_dict: int = 2):
    error = error_object_style()
    error['field_model'] = error_object_style()

    for i in range(1, len_list_dict + 1):
        error['field_model_list'][i - 1] = error_object_style()
        error['field_model_dict'][f'key {i}'] = error_object_style()

    assert error == data
