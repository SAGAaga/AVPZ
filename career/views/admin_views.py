from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPBadRequest,
    HTTPInternalServerError,
)
from pyramid.response import Response

from sqlalchemy.exc import SQLAlchemyError
from formencode.validators import OneOf
from formencode import Invalid as Invalid_form


from ..models import (
    Vacancy,
    VacancyStatusEnum,
    Resume,
    ResumeStatusEnum,
    VacancyContractTypeEnum,
    VacancyJobTypeEnum,
)

from ..logger import get_logger

logger = get_logger()
from ..forms.career_forms import VacancyForm

import paginate
import traceback


ITEM_PER_PAGE = 30
QUERY_LIMIT = 1000

RESUME_SORT_FIELDS = [
    "first_name",
    "last_name",
    "phone",
    "email",
    "status",
    "created_date",
]
RESUME_RENAME_FOR_UNSORTABLE_FIELDS = {"cv_path": "CV", "vac_id": "Vacancy"}

VACANCY_SORT_FIELDS = [
    "title",
    "location",
    "job_type",
    "contract_type",
    "status",
    "created_date",
]
VACANCY_EDIT_FIELDS = {
    "title": "text",
    "desc": "text",
    "location": "text",
    "url_key": "text",
    "job_type": "radio",
    "contract_type": "radio",
    "status": "options",
    "responsibilities": "text",
    "skills": "text",
}
VACANCY_FILTER_FIELDS = [
    "filter_status",
    "filter_location",
    "filter_job_type",
    "filter_contract_type",
]
MY_ENUMS_VALIDATOR = {}

MY_ENUMS = {
    "job_type": VacancyJobTypeEnum,
    "contract_type": VacancyContractTypeEnum,
    "status": VacancyStatusEnum,
}
for field in MY_ENUMS.keys():
    MY_ENUMS_VALIDATOR[field] = OneOf([enm.value for enm in MY_ENUMS[field]])
t = MY_ENUMS_VALIDATOR.get("job_type")


@view_config(
    route_name="admin_access_vacancies",
    renderer="career:templates/admin/admin_panel_vacancies.mako",
)
@view_config(
    route_name="admin_access_vacancies:page",
    renderer="career:templates/admin/admin_panel_vacancies.mako",
)
def view_vacancies_admin_access(request):
    user = request.identity
    if user is None:
        raise HTTPForbidden
    try:
        query = request.dbsession.query(Vacancy)
        try:
            page = request.POST.get("page")
            if not page:
                page = request.matchdict.get("page", 1)
            page = int(page)
        except ValueError as e:
            raise HTTPBadRequest(
                "Page number can not be not intager", content_type="text/plain"
            )
        order_filter = Vacancy.created_date.desc()
        res_dict = {"field_name": "", "direction": "", "filter": {}}
        for field in Vacancy.__table__.columns:
            if field.name in VACANCY_SORT_FIELDS:
                temp = request.POST.get(field.name, "")
                if temp != "":
                    res_dict["field_name"] = field.name
                    res_dict["direction"] = temp
                    if temp == "down":
                        order_filter = field.desc()
                    else:
                        order_filter = field.asc()

            temp_field_name = "filter_" + field.name
            if temp_field_name in VACANCY_FILTER_FIELDS:
                temp = request.POST.get(temp_field_name, "all")
                res_dict["filter"][temp_field_name] = temp
                if temp != "" and temp != "all":
                    if field.name in MY_ENUMS_VALIDATOR.keys():
                        MY_ENUMS_VALIDATOR[field.name].to_python(temp)
                        query = query.filter(field == MY_ENUMS[field.name](temp).name)
                    else:
                        query = query.filter(field == temp)

        vacancies = query.order_by(order_filter).limit(QUERY_LIMIT).all()

        p = paginate.Page(vacancies, page=page, items_per_page=ITEM_PER_PAGE)
        res_dict["data"] = p
        return res_dict

    except SQLAlchemyError as e:
        logger.error(traceback.format_exc())
        raise HTTPInternalServerError(err_msg, content_type="text/plain")


#
# not unique url key check
#
def check_url_key_unique(query, url_key_cur, d):
    url_key_new = d["url_key"]
    if url_key_cur != url_key_new:
        if query.filter(Vacancy.url_key == url_key_new).first():
            raise Invalid_form("Not unique url key", value=d, state=None)


@view_config(
    route_name="admin_access_vacancy",
    renderer="career:templates/admin/admin_panel_vacancy.mako",
)
def vacancy_view_edit(request):
    input_data = None
    error_message = None
    user = request.identity
    if user is None:
        raise HTTPForbidden
    if request.method == "POST":
        if request.POST.get("_method") == "PATCH":
            form = VacancyForm()
            try:
                d = form.to_python(request)
                query = request.dbsession.query(Vacancy)
                id_ = request.matchdict.get("id")

                vacancy = query.get(id_)
                check_url_key_unique(query, vacancy.url_key, d)

                vacancy.update(**d)
                return HTTPFound(
                    request.route_url("admin_access_vacancy", id=vacancy.id)
                )
            except SQLAlchemyError as e:
                logger.error(traceback.format_exc())
                raise HTTPInternalServerError(err_msg, content_type="text/plain")
            except Invalid_form as e:
                error_message = "Invalid input of "
                input_data = e.value
                try:
                    for field in e.error_dict.keys():
                        error_message += f" {field} = {input_data[field]}, "
                except AttributeError:
                    error_message = str(e)
    try:
        query = request.dbsession.query(Vacancy)
        id_ = request.matchdict.get("id")
        if not id_:
            return HTTPFound(request.route_url("admin_access_vacancies"))
        vacancy = query.get(id_)
        if not vacancy:
            logger.error(f"Page [{id_}] does not exist")
            raise HTTPBadRequest("such page does not exist", content_type="text/plain")
    except SQLAlchemyError as e:
        logger.error(traceback.format_exc())
        raise HTTPInternalServerError(err_msg, content_type="text/plain")

    return {
        "vacancy": vacancy,
        "input_data": input_data,
        "error_message": error_message,
    }


@view_config(
    route_name="admin_access_vacancy",
    renderer="career:templates/admin/admin_panel_vacancy.mako",
    request_method="POST",
    request_param="form.delete",
)
def vacancy_delet(request):
    user = request.identity
    if user is None:
        raise HTTPForbidden
    query = request.dbsession.query(Vacancy)
    id_ = request.matchdict.get("id")
    vacancy = query.get(id_)
    request.dbsession.delete(vacancy)
    return HTTPFound(request.route_url("admin_access_vacancies"))


@view_config(
    route_name="admin_access_vacancy",
    renderer="career:templates/admin/admin_panel_vacancy_creation.mako",
    request_param="form.add",
)
def vacancy_creation(request):
    input_data = None
    error_message = None
    user = request.identity
    if user is None:
        raise HTTPForbidden
    if request.method == "POST":
        try:
            form = VacancyForm()
            d = form.to_python(request)
            query = request.dbsession.query(Vacancy)

            check_url_key_unique(query, "", d)

            new_vacancy = Vacancy(**d)

            request.dbsession.add(new_vacancy)
            return HTTPFound(
                request.route_url("admin_access_vacancy", id=new_vacancy.id)
            )
        except SQLAlchemyError as e:
            logger.error(traceback.format_exc())
            raise HTTPInternalServerError(err_msg, content_type="text/plain")
        except Invalid_form as e:
            error_message = "Invalid input of "
            input_data = e.value
            try:
                for field in e.error_dict.keys():
                    error_message += f" {field} = {input_data[field]}, "
            except AttributeError:
                error_message = str(e)
    return {
        "input_data": input_data,
        "error_message": error_message,
    }


@view_config(
    route_name="admin_panel_resumes",
    renderer="career:templates/admin/admin_panel_resumes.mako",
)
@view_config(
    route_name="admin_panel_resumes:page",
    renderer="career:templates/admin/admin_panel_resumes.mako",
)
@view_config(
    route_name="edit_resume",
    renderer="career:templates/admin/admin_panel_resumes.mako",
)
def resumes_view_edit(request):
    error_message = None
    user = request.identity
    if user is None:
        raise HTTPForbidden
    if request.method == "POST":
        if request.POST.get("_method") == "PATCH":
            try:
                query = request.dbsession.query(Resume)
                id_ = request.matchdict.get("id")
                resume = query.get(id_)
                if not resume:
                    #
                    # if not exist
                    #
                    raise HTTPBadRequest(
                        "Incorrect request \nSuch id does not exist",
                        content_type="text/plain",
                    )
                status_validation = OneOf([enm.value for enm in ResumeStatusEnum])
                try:
                    status = status_validation.to_python(request.POST.get("status"))
                    resume.status = ResumeStatusEnum(status).name
                except Invalid_form as e:
                    error_message = "Invalid input of "
                    input_data = e.value
                    try:
                        for field in e.error_dict.keys():
                            error_message += f" {field} = {input_data[field]}, "
                    except AttributeError:
                        error_message = str(e)

            except SQLAlchemyError as e:
                logger.error(traceback.format_exc())
                raise HTTPInternalServerError(err_msg, content_type="text/plain")
    try:
        query = request.dbsession.query(Resume)
        status = request.POST.get("status_filter", "all")
        try:
            page = request.POST.get("page")
            if not page:
                page = request.matchdict.get("page", 1)
            page = int(page)
        except ValueError as e:
            raise HTTPBadRequest(
                "Page number can not be not intager", content_type="text/plain"
            )
        name = ""
        val = ""
        order_filter = Resume.created_date.desc()
        for field in Resume.__table__.columns:
            if field.name in RESUME_SORT_FIELDS:
                temp = request.POST.get(field.name, "")
                if temp != "":
                    name = field.name
                    val = temp
                    if temp == "down":
                        order_filter = field.desc()
                    else:
                        order_filter = field.asc()
                    break
        if status is not None and status != "all":
            status_validator = OneOf([enm.value for enm in ResumeStatusEnum])
            status_validator.to_python(status)
            query = query.filter(Resume.status == ResumeStatusEnum(status).name)

        resumes = query.order_by(order_filter).limit(QUERY_LIMIT).all()
        p = paginate.Page(resumes, page=page, items_per_page=ITEM_PER_PAGE)
        return {
            "data": p,
            "filter_by_status": status,
            "field_name": name,
            "direction": val,
            "error_message": error_message,
        }
    except SQLAlchemyError as e:
        logger.error(traceback.format_exc())
        raise HTTPInternalServerError(err_msg, content_type="text/plain")


@view_config(
    route_name="edit_resume",
    renderer="career:templates/admin/admin_panel_resumes.mako",
    request_method="POST",
    request_param="form.delete",
)
def delete_resumes(request):
    user = request.identity
    if user is None:
        raise HTTPForbidden
    query = request.dbsession.query(Resume)
    id_ = request.matchdict.get("id")
    resume = query.get(id_)
    request.dbsession.delete(resume)
    return HTTPFound(request.route_url("admin_panel_resumes"))


err_msg = """\
Something went wrong! 
We're working hard to fix the issue. 
Please try again later.
"""
