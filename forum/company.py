from werkzeug.security import check_password_hash
import flask_login
from forum import login_manager
from storage import get_company

class Company(flask_login.UserMixin):

    def __init__(self, company_id=None, password=None, data=None):
        self.company_id = company_id
        self.password = password
        self.data = data

    def get_id(self):
        return self.company_id

@login_manager.user_loader
def load_company(company_id):
    comp = get_company(company_id)
    return Company(company_id=company_id, data=comp) if comp else None

def validate_login(password_hash, password):
    return check_password_hash(password_hash, password)