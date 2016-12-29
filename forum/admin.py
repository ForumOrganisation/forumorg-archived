from wtforms import form, fields
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.model.fields import InlineFormField, InlineFieldList
from flask_login import current_user
from flask import flash

import os
import json

class CompanyForm(form.Form):
    id = fields.StringField('Identifiant')
    name = fields.StringField('Nom')
    password = fields.StringField('Mot de passe')

class CompanyView(ModelView):
    column_list = ('id', 'name', 'password', 'sections')
    column_labels = dict(id='Identifiant', name='Nom', password='Mot de passe')
    column_searchable_list = ('id')
    form = CompanyForm
    create_modal = True
    edit_modal = True
    can_export = True
    can_delete = False
    can_view_details = True
    column_exclude_list = ('sections')

    def __init__(self, model, *args, **kwargs):
        super(CompanyView, self).__init__(model, *args, **kwargs)
        self.static_folder = 'static'
        self.endpoint = 'admin'
        self.name = 'Entreprises'
        self.sections = self.get_sections()

    def is_accessible(self):
        return current_user.get_id() == "admin" and current_user.is_authenticated

    def create_model(self, form):
        try:
            model = form.data
            model["sections"] = self.sections
            self._on_model_change(form, model, True)
            self.coll.insert(model)
        except Exception as ex:
            if str(ex)[:6] == 'E11000':
                flash('Une entreprise avec le meme identifiant existe deja.',
                  'error')
            else:
                flash('Failed to create record. {}'.format(str(ex)),
                  'error')
            return False
        else:
            self.after_model_change(form, model, True)

        return model

    def get_sections(self):
        fn = os.path.join(os.path.dirname(__file__), '..', 'sections.json')
        with open(fn) as file:
            return json.load(file)