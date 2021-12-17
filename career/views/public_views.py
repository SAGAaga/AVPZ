from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound, HTTPInternalServerError
from sqlalchemy.exc import SQLAlchemyError
from formencode import Invalid as Invalid_form
from uuid import uuid4

from ..logger import get_logger

logger = get_logger()
from ..models import Vacancy, Resume
from ..forms.career_forms import Apply

import os
import traceback


QUERY_LIMIT = 1000

#
# View all available vacancies
#
@view_config(route_name="vacancies", renderer="career:templates/public/vacancies.mako")
def vacancies_view(request):
    try:
        query = request.dbsession.query(Vacancy)
        vacancies = query.order_by(Vacancy.created_date.desc()).limit(QUERY_LIMIT).all()
        return {"data": vacancies}
    except SQLAlchemyError:
        logger.error(traceback.format_exc())
        raise HTTPInternalServerError(err_msg, content_type="text/plain")


#
# View current vacancy and apply for it
#
@view_config(route_name="vacancy", renderer="career:templates/public/vacancy.mako")
def vacancy_view_apply(request):
    input_data = None
    error_message = None
    if request.method == "POST":
        form = Apply()
        try:
            d = form.to_python(request)
            if type(d) != dict:
                raise Invalid_form
            if d["cv_file"] is not None:
                binary_data = d["cv_file"].file.read()
            #
            # make proper naming
            #
            extention = d["cv_file"].filename.split(".")[-1]
            rand_name = str(uuid4())
            rand_name += "." + extention

            mydir = f"career/cv_storage/{rand_name[0]}/{rand_name[1]}/"
            CHECK_FOLDER = os.path.isdir(mydir)
            if not CHECK_FOLDER:
                os.makedirs(mydir)

            storage_path = f"{mydir}{rand_name}"
            with open(storage_path, "wb") as f:
                f.write(binary_data)

            query = request.dbsession.query(Vacancy)
            key = request.matchdict.get("vacancy_key_url")
            vacancy = query.filter(Vacancy.url_key == key).first()
            d["vac_id"] = vacancy.id
            d["created_date"] = None
            d["cv_path"] = rand_name
            d.pop("cv_file")
            new_resume = Resume(**d)
            request.dbsession.add(new_resume)
        except SQLAlchemyError as e:
            logger.error(traceback.format_exc())
            raise HTTPInternalServerError(err_msg, content_type="text/plain")
        except Invalid_form as e:
            error_message = "Invalid input of "
            input_data = e.value
            for field in e.error_dict.keys():
                error_message += f" {field} = {input_data[field]}, "
    try:
        query = request.dbsession.query(Vacancy)
        key = request.matchdict.get("vacancy_key_url")
        vacancy = query.filter(Vacancy.url_key == key).first()
        if not vacancy:
            raise HTTPBadRequest("such page does not exist", content_type="text/plain")
    except SQLAlchemyError as e:
        logger.error(traceback.format_exc())
        raise HTTPInternalServerError(err_msg, content_type="text/plain")

    return {
        "vacancy": vacancy,
        "error_message": error_message,
        "input_data": input_data,
    }


err_msg = """\
Something went wrong! 
We're working hard to fix the issue. 
Please try again later.
"""
