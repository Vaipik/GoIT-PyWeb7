from app.models import User, db


def create_user(form) -> None:
    """
    Adding new user to DB
    :param form: user registration form
    :return: None
    """
    user = User(username=form.name.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()


def read_user(username: str) -> User:
    return User.query.filter_by(username=username).first()

