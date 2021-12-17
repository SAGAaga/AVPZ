from pyramid.csrf import new_csrf_token
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.security import (
    remember,
    forget,
)
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..models import SuperUser


@view_config(route_name="login", renderer="career:templates/auth/login.mako")
def login(request):
    next_url = request.params.get("next", request.referrer)
    if not next_url:
        next_url = request.route_url("admin_access_vacancies")
    message = ""
    login = ""
    if request.method == "POST":
        login = request.params["login"]
        password = request.params["password"]
        user = (
            request.dbsession.query(SuperUser)
            .filter(SuperUser.username == login)
            .first()
        )
        if user is not None and user.validate_password(password):
            new_csrf_token(request)
            headers = remember(request, user.id)
            return HTTPSeeOther(location=next_url, headers=headers)
        message = "Failed login"
        request.response.status = 400

    return {
        "message": message,
        "url": request.route_url("login"),
        "next_url": next_url,
        "login": login,
    }


@view_config(route_name="logout")
def logout(request):
    next_url = request.route_url("login")
    if request.method == "POST":
        new_csrf_token(request)
        headers = forget(request)
        return HTTPSeeOther(location=next_url, headers=headers)

    return HTTPSeeOther(location=next_url)


@forbidden_view_config(renderer="career:templates/errors/403.mako")
def forbidden_view(exc, request):
    """It is invoked when a pyramid.httpexceptions.HTTPForbidden exception is raised."""
    if not request.is_authenticated:
        next_url = request.route_url("login", _query={"next": request.url})
        return HTTPSeeOther(location=next_url)

    request.response.status = 403
    return {}
