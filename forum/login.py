from flask import redirect, url_for
from forum import login_manager
from storage import Company, get_company


@login_manager.user_loader
def load_company(company_id):
    return Company(id=company_id, data=get_company(company_id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


def validate_login(password_input, password_real):
    return password_input == password_real
