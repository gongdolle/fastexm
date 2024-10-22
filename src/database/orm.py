from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Boolean,Column,Integer,String,ForeignKey
from src.schema.request import CreateToDoRequest



Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False, unique=True)  # 예: 'Admin', 'User', 'Manager'
    
    # 역할을 정의하는 생성 메서드
    @classmethod
    def create(cls, role_name: str) -> "Role":
        return cls(
            role_name=role_name
        )

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone_num = Column(String(100), nullable=True)  # 전화번호는 선택 사항
    name = Column(String(100), nullable=False)  # 이름은 필수
    roles_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)  # 역할 ID
    company_code = Column(String(100), ForeignKey('company_ids.company_code'), nullable=False)  # 회사 코드 필수

    # 관계 설정
    role = relationship("ROLE")  # Role 테이블과의 관계
    company = relationship("CompanyIDs", back_populates="users")  # CompanyIDs와의 관계

    # 생성 메서드
    @classmethod
    def create(cls, username: str, email: str, hashed_password: str, name: str, roles_id: int, company_code: str, phone_num: str = None) -> "User":
        return cls(
            username=username,
            email=email,
            password=hashed_password,
            name=name,
            phone_num=phone_num,
            roles_id=roles_id,
            company_code=company_code  # 회사 코드는 필수로 받음
        )


class CompanyIDs(Base):
    __tablename__ = "company_ids"

    company_code = Column(String(100), primary_key=True)  # 회사 코드
    company_id = Column(Integer, ForeignKey('companies.company_id'), nullable=False)  # 외래 키

    # 관계 설정
    companies = relationship("Companies", back_populates="company_ids")  # Companies와의 관계
    users = relationship("User", back_populates="company")  # Users와의 관계

class Companies(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, autoincrement=True)  # 회사 ID
    company_name = Column(String(100), nullable=False)  # 회사 이름

    # 관계 설정
    company_ids = relationship("CompanyIDs", back_populates="companies")  # CompanyIDs와의 관계


class InverterType(Base):
    __tablename__ = "inverter_type"

    inverter_type_id = Column(Integer, primary_key=True)  # 인버터 유형 ID
    type_name = Column(String(100), nullable=False)  # 인버터 유형 이름

    # 관계 설정
    attributes = relationship("InverterAttributes", back_populates="inverter_type")  # Attributes와의 관계


class InverterAttributes(Base):
    __tablename__ = "INVERTER_Attributes"

    attribute_id = Column(Integer, primary_key=True, autoincrement=True)  # 특성 ID
    attribute_name = Column(String(255), nullable=False)  # 특성 이름
    attribute_type = Column(String(100), nullable=False)  # 특성 타입

    # 관계 설정
    inverter_type_id = Column(Integer, ForeignKey('inverter_type.inverter_type_id'))  # 외래 키
    inverter_type = relationship("InverterType", back_populates="attributes")  # InverterType과의 관계


class InvInfo(Base):
    __tablename__ = "INV_INFO"

    inv_id = Column(Integer, primary_key=True, autoincrement=True)  # 인버터 ID
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # 사용자 ID
    inv_name = Column(String(100), nullable=False)  # 인버터 이름
    inverter_type_id = Column(Integer, ForeignKey('inverter_type.inverter_type_id'))  # 인버터 유형 ID

    # 관계 설정
    user = relationship("User")  # User와의 관계
    inverter_type = relationship("InverterType")  # InverterType과의 관계


class InvDataInt(Base):
    __tablename__ = "INV_DATA_INT"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID
    inv_id = Column(Integer, ForeignKey('INV_INFO.inv_id'), nullable=False)  # 인버터 ID
    inverter_type_id = Column(Integer, ForeignKey('inverter_type.inverter_type_id'))  # 인버터 유형 ID
    attribute_id = Column(Integer, ForeignKey('INVERTER_Attributes.attribute_id'), nullable=False)  # 특성 ID
    timestamp = Column(DateTime, nullable=False)  # 타임스탬프
    value = Column(Integer, nullable=False)  # 값

    # 관계 설정
    inv_info = relationship("InvInfo")  # InvInfo와의 관계


class InvDataBool(Base):
    __tablename__ = "INV_DATA_BOOL"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID
    inv_id = Column(Integer, ForeignKey('INV_INFO.inv_id'), nullable=False)  # 인버터 ID
    inverter_type_id = Column(Integer, ForeignKey('inverter_type.inverter_type_id'))  # 인버터 유형 ID
    attribute_id = Column(Integer, ForeignKey('INVERTER_Attributes.attribute_id'), nullable=False)  # 특성 ID
    timestamp = Column(DateTime, nullable=False)  # 타임스탬프
    value = Column(Boolean, nullable=False)  # 값 (불리언)

    # 관계 설정
    inv_info = relationship("InvInfo")  # InvInfo와의 관계


class InvDataChar(Base):
    __tablename__ = "INV_DATA_CHAR"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID
    inv_id = Column(Integer, ForeignKey('INV_INFO.inv_id'), nullable=False)  # 인버터 ID
    inverter_type_id = Column(Integer, ForeignKey('inverter_type.inverter_type_id'))  # 인버터 유형 ID
    attribute_id = Column(Integer, ForeignKey('INVERTER_Attributes.attribute_id'), nullable=False)  # 특성 ID
    timestamp = Column(DateTime, nullable=False)  # 타임스탬프
    value = Column(String(255), nullable=False)  # 값 (문자열)

    # 관계 설정
    inv_info = relationship("InvInfo")  # InvInfo와의 관계



class InvDataFloat(Base):
    __tablename__ = "INV_DATA_FLOAT"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID
    inv_id = Column(Integer, ForeignKey('INV_INFO.inv_id'), nullable=False)  # 인버터 ID
    inverter_type_id = Column(Integer, ForeignKey('inverter_type.inverter_type_id'))  # 인버터 유형 ID
    attribute_id = Column(Integer, ForeignKey('INVERTER_Attributes.attribute_id'), nullable=False)  # 특성 ID
    timestamp = Column(DateTime, nullable=False)  # 타임스탬프
    value = Column(Float, nullable=False)  # 값 (부동 소수점)

    # 관계 설정
    inv_info = relationship("InvInfo")  # InvInfo와의 관계
