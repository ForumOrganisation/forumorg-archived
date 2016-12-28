from wtforms import form, fields
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.model.fields import InlineFormField, InlineFieldList

class CompanyForm(form.Form):
    id = fields.StringField('Identifiant')
    name = fields.StringField('Nom')
    password = fields.StringField('Mot de passe')

class CompanyView(ModelView):
    column_list = ('id', 'name', 'password')
    form = CompanyForm
    create_modal = True
    edit_modal = True