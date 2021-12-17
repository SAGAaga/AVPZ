import enum
from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
)

from sqlalchemy.orm import relationship


from .meta import Base


class VacancyStatusEnum(enum.Enum):
    published = "published"
    draft = "draft"
    cancelled = "cancelled"


class VacancyJobTypeEnum(enum.Enum):
    full_time = "Full Time"
    part_time = "Part Time"


class VacancyContractTypeEnum(enum.Enum):
    fixed_term = "Fixed Term"
    permanent = "Permanent"


class ResumeStatusEnum(enum.Enum):
    new = "new"
    accepted = "accepted"
    rejected = "rejected"


class Vacancy(Base):
    __tablename__ = "vacancy"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    # description
    desc = Column(String, nullable=False)
    url_key = Column(String, nullable=False, unique=True)
    location = Column(String, index=True)
    responsibilities = Column(String)
    skills = Column(String)
    job_type = Column(
        Enum(VacancyJobTypeEnum),
        index=True,
    )
    contract_type = Column(
        Enum(VacancyContractTypeEnum),
        index=True,
    )
    created_date = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        server_default=func.now(),
        nullable=False,
    )
    status = Column(
        Enum(VacancyStatusEnum),
        default=VacancyStatusEnum.published.name,
        server_default=VacancyStatusEnum.published.name,
        nullable=False,
        index=True,
    )
    resumes = relationship(
        "Resume",
        back_populates="vacancy",
        cascade="all, delete",
        passive_deletes=True,
    )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Resume(Base):
    __tablename__ = "resume"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    email = Column(String)
    cv_path = Column(String)
    status = Column(
        Enum(ResumeStatusEnum),
        default=ResumeStatusEnum.new.name,
        server_default=ResumeStatusEnum.new.name,
        nullable=False,
        index=True,
    )
    created_date = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        server_default=func.now(),
        nullable=False,
    )
    vac_id = Column(
        Integer,
        ForeignKey("vacancy.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    vacancy = relationship("Vacancy", back_populates="resumes")
