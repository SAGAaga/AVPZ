from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from .security import includeme


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    my_session_factory = SignedCookieSessionFactory("itsaseekreet")

    with Configurator(
        settings=settings, session_factory=my_session_factory
    ) as config:
        includeme(config)
        config.include("pyramid_mako")
        config.include(".routes")
        config.include(".models")
        config.add_static_view(
            settings["static"], "static", cache_max_age=3600
        )
        config.add_static_view(settings["cv_storage"], "cv_storage")
        config.scan()
    return config.make_wsgi_app()
