import json
import os

from flask import Response, flash, stream_with_context
from flask_admin.babel import gettext
from flask_admin.base import expose
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.helpers import get_redirect_target
from flask_login import current_user
from werkzeug import secure_filename
from wtforms import StringField, fields, form, validators

from export import generate_vals

def sections_formatter(v,c,m,p):
    if m['id'] != 'admin':
        if p == 'nom complet':
            return m['sections']['profile']['name']
        if p in SECTIONS[6:]:
            return m['sections']['equipement']['general'][p]
        return m['sections'][p]['completed']
SECTIONS = ['equipement', 'transport', 'restauration', 'programme', 'badges',\
            'nom complet',\
            'emplacement', 'duration', 'equiped', 'bandeau', 'size']

def get_sections():
    fn = os.path.join(os.path.dirname(__file__), 'sections.json')
    with open(fn) as file:
        return json.load(file)

class CompanyForm(form.Form):
    id = fields.StringField('Identifiant', validators=[validators.Required(), validators.Length(min=3, max=30)], render_kw={"placeholder": "Ex. loreal"})
    password = fields.PasswordField('Mot de passe', validators=[validators.Required(), validators.Length(min=5, max=30)], render_kw={"placeholder": "Ex. 123456"})
    name = fields.StringField('Nom complet', render_kw={"placeholder": "Ex. L'Oreal"}, validators=[validators.Required(), validators.Length(min=3, max=30)])
    emplacement = fields.StringField('Emplacement', render_kw={"placeholder": "Ex. F13"})
    duration = fields.IntegerField('Jours de presence', validators=[validators.optional()], render_kw={"placeholder": "Ex. 2"})
    equiped = fields.BooleanField('Equipe?')
    bandeau = fields.BooleanField('Bandeau?')
    size = fields.IntegerField('Surface', validators=[validators.optional()], render_kw={"placeholder": "Ex. 12"})

class CompanyView(ModelView):
    form = CompanyForm
    column_list = ['id'] + SECTIONS[:5]
    column_labels = dict(id='Identifiant')
    column_formatters = dict((s,sections_formatter) for s in SECTIONS)
    export_types = ['csv', 'transport', 'restauration', 'badges', 'equipement']
    can_export = True
    can_delete = True
    column_details_list = SECTIONS[5:]
    can_view_details = True

    def __init__(self, *args, **kwargs):
        super(CompanyView, self).__init__(*args, **kwargs)
        self.static_folder = 'static'
        self.endpoint = 'admin'
        self.name = 'Entreprises'
        self.sections = get_sections()

    def create_model(self, form):
        try:
            model = form.data
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

    def update_model(self, form, model):
        try:
            model.update(form.data)
            self._on_model_change(form, model, False)
            pk = self.get_pk_value(model)
            self.coll.update({'_id': pk}, model)
        except Exception as ex:
            flash(gettext('Failed to update record. %(error)s', error=str(ex)),
                  'error')
            log.exception('Failed to update record.')
            return False
        else:
            self.after_model_change(form, model, False)

        return True

    def _on_model_change(self, form, model, is_created):
        if is_created:
            model['sections'] = self.sections
        for s in SECTIONS[6:]:
            if s in form.data:
                model['sections']['equipement']['general'][s] = form.data.get(s)
                form.data.pop(s, None)
                model.pop(s, None)
        if 'emplacement' in form.data:
            model['sections']['equipement']['general']['emplacement'] = form.data.get('emplacement')
            form.data.pop('emplacement', None)
            model.pop('emplacement', None)
        if 'name' in form.data:
            model['sections']['profile']['name'] = form.data.get('name')
            form.data.pop('name', None)
            model.pop('name', None)

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
