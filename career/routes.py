def admin_panel_vacancies(config):
    config.add_route("admin_access_vacancies", "")
    config.add_route("admin_access_vacancies:page", "/page={page}")
    config.add_route("admin_access_vacancy", "/vacancy/{id}")


def admin_panel_resumes(config):
    config.add_route("admin_panel_resumes", "")
    config.add_route("admin_panel_resumes:page", "/page={page}")
    config.add_route("edit_resume", "/resume/{id}")


def admin_panel(config):
    config.include(admin_panel_vacancies, route_prefix="/vacancies")
    config.include(admin_panel_resumes, route_prefix="/resumes")


def includeme(config):
    config.add_route("login", "/login")
    config.add_route("logout", "/logout")
    config.add_route("vacancies", "/careers")
    config.add_route("vacancy", "/careers/{vacancy_key_url}")
    config.include(admin_panel, route_prefix="/adm1n44")
