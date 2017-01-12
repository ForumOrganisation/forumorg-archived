import json
import os
import csv

from flask import Response, flash, stream_with_context, redirect
from flask_admin.babel import gettext
from flask_admin.base import expose
from flask_admin.contrib.pymongo import ModelView
from flask_admin.helpers import get_redirect_target
from flask_login import current_user
from werkzeug import secure_filename
from wtforms import fields, form, validators
from export import log

from export import generate_vals


def sections_formatter(v, c, m, p):
    if m['id'] != 'admin':
        if p == 'nom complet':
            return m['sections']['profile']['name']
        if p == 'acompte':
            return m['sections']['profile']['acompte']
        try:
            return m['sections']['equipement']['general'][p]
        except:
            return m['sections'][p]['completed']


SECTIONS = ['equipement', 'transport', 'restauration', 'programme', 'badges',
            'nom complet', 'acompte', 'emplacement', 'duration', 'equiped', 'banner', 'bandeau', 'size']


def get_sections():
    fn = os.path.join(os.path.dirname(__file__), 'sections.json')
    with open(fn) as file:
        return json.load(file)


class CompanyForm(form.Form):
    id = fields.StringField('Identifiant', validators=[validators.Required(), validators.Length(min=0, max=30)], render_kw={"placeholder": "Ex. LOREAL"})
    password = fields.StringField('Mot de passe', validators=[validators.Required(), validators.Length(min=0, max=30)], render_kw={"placeholder": "Ex. motdepasse"})
    name = fields.StringField('Nom complet', render_kw={"placeholder": "Ex. L'Oreal"})
    emplacement = fields.StringField('Emplacement', render_kw={"placeholder": "Ex. F13"})
    banner = fields.StringField('Banniere', render_kw={"placeholder": "Ex. Amazon Happy"})
    size = fields.SelectField('Surface', choices=[(9, '9 m2'), (12, '12 m2'), (18, '18 m2'), (36, '36 m2')], coerce=int)
    duration = fields.SelectField('Jours de presence', choices=[(1, '1 jour'), (2, '2 jours')], coerce=int)
    equiped = fields.BooleanField('Equipe?')
    bandeau = fields.BooleanField('Bandeau?')
    acompte = fields.BooleanField('Acompte paye?')


class CompanyView(ModelView):
    form = CompanyForm
    column_list = ['id'] + ['equipement', 'transport', 'restauration', 'programme', 'badges']
    column_labels = dict(id='Identifiant', acompte='Acompte paye?',
                        duration='Duree de presence', equiped='Equipe?',
                        banner='Banniere', bandeau='Bandeau?', size='Taille (m2)',
                        password='Mot de passe')
    column_formatters = dict((s, sections_formatter) for s in SECTIONS)
    export_types = ['csv', 'transport', 'restauration', 'badges', 'equipement']
    can_export = True
    can_delete = True
    create_modal = True
    edit_modal = True
    can_view_details = True
    details_modal = True
    column_details_list = ['id', 'password'] + SECTIONS[-8:]

    def __init__(self, *args, **kwargs):
        super(CompanyView, self).__init__(*args, **kwargs)
        self.static_folder = 'static'
        self.endpoint = 'admin'
        self.name = 'Entreprises'
        self.sections = get_sections()

    def _on_model_change(self, form, model, is_created):
        if is_created:
            model['sections'] = self.sections
        if model.get('name'):
            model['sections']['profile']['name'] = model.pop('name')
        if model.get('acompte'):
            model['sections']['profile']['acompte'] = model.pop('acompte')
        # Adding sections
        for s in SECTIONS[-6:]:
            d = {s: model.pop(s)}
            if d[s]:
                model['sections']['equipement']['general'].update(d)

    def is_accessible(self):
        return current_user.get_id() == 'admin' and current_user.is_authenticated

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
        filename = self.get_export_name(export_type='csv')
        disposition = 'attachment;filename=%s' % (secure_filename(filename.replace(self.name, export_type)),)
        return Response(
            stream_with_context(gen_vals),
            headers={'Content-Disposition': disposition},
            mimetype='text/csv'
        )


class UserForm(form.Form):
    id = fields.StringField('Email', render_kw={"placeholder": "Ex. yokoya@live.com"})
    password = fields.PasswordField('Mot de passe', validators=[validators.Required(), validators.Length(min=5, max=30)], render_kw={"placeholder": "Ex. 123456"})


class UserView(ModelView):
    column_list = ['id', 'events', 'confirmed_on', 'registered_on']
    column_labels = dict(id='Email')
    export_types = ['csv']
    can_export = True
    can_delete = True
    can_view_details = True
    form = UserForm
    column_export_list = ['id', 'registered_on', 'confirmed_on', 'events']

    def __init__(self, *args, **kwargs):
        super(UserView, self).__init__(*args, **kwargs)
        self.name = 'Utilisateurs'


class EventForm(form.Form):
    name = fields.StringField('Nom')
    type = fields.StringField('Type')
    quota = fields.IntegerField('Quota')
    places_left = fields.IntegerField('Places restantes')


class EventView(ModelView):
    column_list = ['name', 'type', 'quota', 'places_left']
    column_labels = dict(id='Email')
    export_types = ['csv']
    can_export = True
    can_delete = True
    form = EventForm

    def __init__(self, *args, **kwargs):
        super(EventView, self).__init__(*args, **kwargs)
        self.name = 'Journee Objectif Ingenieur'
