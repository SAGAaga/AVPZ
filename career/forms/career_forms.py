import formencode
from formencode import validators
from ..models import (
    VacancyStatusEnum,
    VacancyJobTypeEnum,
    VacancyContractTypeEnum,
    ResumeStatusEnum,
)
from slugify import slugify
from formencode import Invalid as Invalid_form


class Apply(formencode.Schema):
    first_name = validators.ByteString()
    last_name = validators.ByteString()
    email = validators.Email(resolve_domain=True)
    phone = validators.PhoneNumber()
    cv_file = validators.FieldStorageUploadConverter(not_empty=True)
    status = validators.OneOf([enm.value for enm in ResumeStatusEnum])

    def to_python(self, value_dict):
        validate_dict = {}
        for field in Apply.fields:
            validate_dict[field] = value_dict.POST.get(field)
            if validate_dict[field] == "":
                validate_dict[field] = None
        validate_dict = super().to_python(validate_dict)
        if type(validate_dict) == dict:
            #
            # If status is None we will get ValueError
            # but None value is ok for us as status will be set by default
            #
            try:
                validate_dict["status"] = ResumeStatusEnum(validate_dict["status"]).name
            except ValueError:
                pass
        return validate_dict


class VacancyForm(formencode.Schema):
    title = validators.ByteString(not_empty=True)
    desc = validators.ByteString(not_empty=True)
    url_key = validators.ByteString(not_empty=True)
    location = validators.ByteString()
    responsibilities = validators.ByteString()
    skills = validators.ByteString()
    job_type = validators.OneOf([enm.value for enm in VacancyJobTypeEnum])
    contract_type = validators.OneOf([enm.value for enm in VacancyContractTypeEnum])
    status = validators.OneOf([enm.value for enm in VacancyStatusEnum], not_empty=True)

    def _validate_python(self, value, state):
        if value["url_key"] != slugify(value["url_key"]):
            raise Invalid_form("Not correct url key", value=value, state=state)

        return super()._validate_python(value, state)

    def to_python(self, value_dict):
        validate_dict = {}
        for field in VacancyForm.fields:
            validate_dict[field] = value_dict.POST.get(field)
            if validate_dict[field] == "":
                validate_dict[field] = None
        if not validate_dict["url_key"]:
            validate_dict["url_key"] = slugify(validate_dict["title"])
        validate_dict = super().to_python(validate_dict)
        if type(validate_dict) == dict:
            #
            # If job_type is None we will get ValueError
            # but None value is ok for us as job_type has no null constrain
            #
            try:
                validate_dict["job_type"] = VacancyJobTypeEnum(
                    validate_dict["job_type"]
                ).name
            except ValueError:
                pass
            #
            # If contract_type is None we will get ValueError
            # but None value is ok for us as contract_type has no null constrain
            #
            try:
                validate_dict["contract_type"] = VacancyContractTypeEnum(
                    validate_dict["contract_type"]
                ).name
            except ValueError:
                pass
            #
            # If status is None we will get ValueError
            # but None value is ok for us as status will be set by default
            #
            try:
                validate_dict["status"] = VacancyStatusEnum(
                    validate_dict["status"]
                ).name
            except ValueError:
                pass
        return validate_dict
