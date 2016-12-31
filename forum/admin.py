from werkzeug import secure_filename
from wtforms import form, fields
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.model.fields import InlineFormField, InlineFieldList
from flask_admin.base import expose
from flask_admin.helpers import get_redirect_target
from flask_admin._compat import csv_encode
from flask_login import current_user
from flask import flash, Response, stream_with_context
import csv

import os
import json

def get_sections():
    fn = os.path.join(os.path.dirname(__file__), '..', 'sections.json')
    with open(fn) as file:
        return json.load(file)

class CompanyForm(form.Form):
    id = fields.StringField('Identifiant')
    name = fields.StringField('Nom')
    password = fields.StringField('Mot de passe')

class CompanyView(ModelView):
    column_list = ('id', 'name', 'password', 'sections')
    column_labels = dict(id='Identifiant', name='Nom', password='Mot de passe')
    form = CompanyForm
    create_modal = True
    edit_modal = True
    can_export = True
    can_delete = True
    can_view_details = True
    export_types = ['csv']
    #export_types += ['transport', 'restauration', 'badges', 'equipement']
    column_exclude_list = ('sections')

    def __init__(self, model, *args, **kwargs):
        super(CompanyView, self).__init__(model, *args, **kwargs)
        self.static_folder = 'static'
        self.endpoint = 'admin'
        self.name = 'Entreprises'
        self.sections = get_sections()

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
        new_data = (r['sections'][export_type] for r in data if r['id'] != 'admin')
        gen_vals = generate_vals(writer, export_type, new_data)
        filename = self.get_export_name(export_type='csv')
        disposition = 'attachment;filename=%s' % (secure_filename(filename.replace(self.name, export_type)),)
        return Response(
            stream_with_context(gen_vals),
            headers={'Content-Disposition': disposition},
            mimetype='text/csv'
        )

def generate_vals(writer, export_type, data):
    data = list(data)
    if export_type == 'equipement':
        titles = data[0]['general'].keys() + data[0]['furniture'].keys()
        for row in data:
            vals = [row.get('general', 'furniture')[t] for t in titles]
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'restauration':
        titles = data[0]['general'].keys() + data[0]['furniture'].keys()
        yield writer.writerow(titles)
        for row in data:
            vals = [row.get('general', 'furniture')[t] for t in titles]
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'transport':
        titles = data[0]['general'].keys() + data[0]['furniture'].keys()
        yield writer.writerow(titles)
        for row in data:
            vals = [csv_encode(row.get('general', 'furniture')[t]) for t in titles]
            yield writer.writerow(vals)
    if export_type == 'badges':
        titles = data[0]['general'].keys() + data[0]['furniture'].keys()
        yield writer.writerow(titles)
        for row in data:
            vals = [csv_encode(row.get('general', 'furniture')[t]) for t in titles]
            yield writer.writerow(vals)