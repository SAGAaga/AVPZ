import argparse
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from ..models.user_models import SuperUser


def setup_models(dbsession):
    """
    Creation new super user

    """
    query = dbsession.query(SuperUser)
    if not query.filter(SuperUser.username == "admin").first():
        model = SuperUser(username="admin", password="admin")
    print(f"\n\n\n\n\nDefault user is:\nadmin:admin\n\n")
    dbsession.add(model)
    ans = input("Add new one [y/n] ")
    if ans.lower() == "y":
        username = input("Username: ")
        password = input("Password: ")
        if not query.filter(SuperUser.username == username).first():
            model = SuperUser(username=username, password=password)
            dbsession.add(model)
            print("\n\n\n")
        else:
            print("User with such username already existes")


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config_uri",
        help="Configuration file, e.g., development.ini",
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env["request"].tm:
            dbsession = env["request"].dbsession
            setup_models(dbsession)
    except OperationalError:
        print(
            """
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            """
        )
