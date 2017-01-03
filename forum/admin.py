import json
import os

from flask import Response, flash, stream_with_context
from flask_admin.base import expose
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.helpers import get_redirect_target
from flask_login import current_user
from mongoengine.errors import NotUniqueError
from werkzeug import secure_filename
from wtforms import fields, form

from export import generate_vals

def get_sections():
    fn = os.path.join(os.path.dirname(__file__), 'sections.json')
    with open(fn) as file:
        return json.load(file)

class CompanyForm(form.Form):
    id = fields.StringField('Identifiant')
    password = fields.PasswordField('Mot de passe')

class CompanyView(ModelView):
    can_export = True
    can_delete = True
    column_list = ['id', 'password']
    column_labels = dict(id='identifiant', password='mot de passe')
    export_types = ['csv', 'transport', 'restauration', 'badges', 'equipement']
    form = CompanyForm

    def __init__(self, *args, **kwargs):
        super(CompanyView, self).__init__(*args, **kwargs)
        self.static_folder = 'static'
        self.endpoint = 'admin'
        self.name = 'Entreprises'
        self.sections = get_sections()

    def create_model(self, form):
        try:
            model = form.data
            model['sections'] = self.sections
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

    def is_accessible(self):
        return current_user.get_id() == "admin" and current_user.is_authenticated

    @expose('/export/<export_type>/')
    def export(self, export_type):
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_export or (export_type not in self.export_types):
            flash(gettext('Permission denied.'), 'error')
            return redirect(return_url)

        if export_type == 'csv':
            return self._export_csv(return_url)
        else:
            return self._export_fields(export_type, return_url)

    def _export_fields(self, export_type, return_url):
        count, data = self._export_data()

        # Dummy object for csv creation
        class Echo(object):
            def write(self, value):
                return value

        writer = csv.writer(Echo())
        data = [r for r in data if r['id'] != 'admin']
        gen_vals = generate_vals(writer, export_type, data)
        # filename = self.get_export_name(export_type='csv')
        filename = 'export.csv'
        disposition = 'attachment;filename=%s' % (secure_filename(filename.replace(self.name, export_type)),)
        return Response(
            stream_with_context(gen_vals),
            headers={'Content-Disposition': disposition},
            mimetype='text/csv'
        )
