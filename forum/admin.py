# coding=utf-8

from flask import url_for
from flask_admin.base import expose, BaseView
from flask_admin.contrib.pymongo import ModelView
from flask_admin.contrib.pymongo.filters import BasePyMongoFilter, FilterEqual
from flask_admin.form import rules
from flask_login import current_user
from wtforms import fields, form, validators
from export import _export, log
from jinja2 import Markup


class StatisticsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('statistics.html')


def formatter(view, context, model, name):
    filters = context.get_all().get('active_filters')
    if any(['pole' in f for f in filters]):
        return Markup("<a href='{}'>{}</a>".format(url_for('dashboard', id='lem'), model['id']))
    return model['id']


class CompanyForm(form.Form):
    # Basic
    id = fields.StringField('Identifiant', validators=[validators.Required(), validators.Length(min=3, max=30)], render_kw={"placeholder": "Ex. loreal, amadeus, canalplus"})
    password = fields.StringField('Mot de passe', validators=[validators.Required(), validators.Length(min=3, max=30)], render_kw={"placeholder": "Ex. password"})
    name = fields.StringField('Nom complet', validators=[validators.Required(), validators.Length(min=3, max=30)], render_kw={"placeholder": "Ex. L'Oreal, Amadeus, Canal+"})
    acompte = fields.BooleanField('Acompte paye?')
    # Equipement
    emplacement = fields.StringField('Emplacement', render_kw={"placeholder": "Ex. F13"})
    size = fields.SelectField('Surface', choices=[(4.5, '4.5 m2'), (9, '9 m2'), (12, '12 m2'), (18, '18 m2'), (24, '24 m2'), (27, '27 m2'), (36, '36 m2')], coerce=float)
    duration = fields.SelectField('Jours de presence', choices=[('wed', 'Mercredi'), ('thu', 'Jeudi'), ('both', 'Mercredi et Jeudi')])
    equiped = fields.BooleanField('Equipe?')
    pole = fields.SelectField('Pole', choices=[('fra', 'Entreprises France'), ('si', 'Section Internationale'), ('cm', 'Carrefour Maghrebin'), ('school', 'Ecoles')])
    # Dashboard
    equipement = fields.BooleanField('Equipement valide?')
    restauration = fields.BooleanField('Restauration valide?')
    badges = fields.BooleanField('Badges valide?')
    transport = fields.BooleanField('Transports valide?')
    programme = fields.BooleanField('Programme valide?')


class FilterPole(FilterEqual, BasePyMongoFilter):

    def apply(self, query, value):
        query.append({'pole': value})
        return query

    def operation(self):
        return "egal a"


class FilterZone(FilterEqual, BasePyMongoFilter):

    def apply(self, query, value):
        query.append({'zone': value})
        return query

    def operation(self):
        return "egal a"


class CompanyView(ModelView):
    form = CompanyForm
    column_list = ['id'] + ['equipement', 'transport',
                            'restauration', 'badges', 'programme']
    export_types = ['equipement', 'transport', 'restauration', 'badges', 'programme']
    form_rules = [
        rules.FieldSet(('id', 'password', 'name', 'pole'), 'Profil'),
        rules.FieldSet(('equipement', 'restauration', 'badges',
                        'programme', 'transport'), 'Suivi'),
        rules.FieldSet(('acompte',), 'Finances'),
        rules.FieldSet(('size', 'duration', 'equiped',
                        'emplacement'), 'Equipement'),
    ]

    can_export = True
    can_delete = True
    create_modal = False
    edit_modal = False

    column_searchable_list = ['id']
    column_sortable_list = ['id']
    column_filters = (FilterPole(column='pole', name='pole', options=(
        ('fra', 'Entreprises France'), ('si', 'Section Internationale'), ('cm', 'Carrefour Maghrebin'), ('school', 'Ecoles'))),
        FilterZone(column='zone', name='zone', options=[["zone{}".format(i)] * 2 for i in range(1, 9)]))
    column_labels = dict(id='Identifiant')
    column_formatters = dict(id=formatter)

    def __init__(self, *args, **kwargs):
        super(CompanyView, self).__init__(*args, **kwargs)
        self.static_folder = 'static'
        self.endpoint = 'admin'
        self.name = 'Entreprises'

    def is_accessible(self):
        return current_user.get_id() == 'admin' and current_user.is_authenticated

    @expose('/export/<export_type>/')
    def export(self, export_type):
        return _export(self, export_type)

    def _on_model_change(self, form, model, is_created):
        if is_created:
            model['sections'] = {
                'furnitures': {}, 'catering': {'wed': {}, 'thu': {}}, 'events': {},
                'persons': [], 'transports': [], 'profile': {'stand': {}, 'facturation': {}}
            }


class UserForm(form.Form):
    pass


class FilterRegister(FilterEqual, BasePyMongoFilter):

    def apply(self, query, value):
        if value == 'ambassador':
            query.append({'events.fra.ambassador': {'$gt': {}}})
        else:
            query.append({'events.{}.registered'.format(value): True})
        return query

    def operation(self):
        return "participe a"


class UserView(ModelView):
    column_list = ['id', 'events', 'confirmed_on', 'registered_on', 'profile']
    column_labels = dict(id='Email', confirmed_on='Confirmation', registered_on='Inscription', profile='Profil', events='Participations')
    export_types = ['general']
    can_export = True
    can_edit = False
    can_delete = False
    can_view_details = True
    form = UserForm
    column_exclude_list = ['confirmed_on', 'events']
    column_searchable_list = ('id',)
    column_filters = (FilterRegister(column='events', name='inscrit', options=(
        ('master_class', 'Master Class'),
        ('fra', 'Forum Rhone-Alpes'),
        ('ambassador', 'Ambassadeur'),
        ('styf', 'Start-Up Your Future'),
        ('joi', 'Journee Objectif Ingenieur'))),)
    column_sortable_list = ['id', 'confirmed_on', 'registered_on']

    def __init__(self, *args, **kwargs):
        super(UserView, self).__init__(*args, **kwargs)
        self.name = 'Utilisateurs'

    @expose('/export/<export_type>/')
    def export(self, export_type):
        return _export(self, export_type)


class JobForm(form.Form):
    pass


class JobView(ModelView):
    column_list = ['company_id', 'title', 'location', 'duration', 'description']
    column_labels = dict(company_id='Entreprise', duration='Duree', location='Lieu')
    can_edit = False
    can_delete = False
    form = JobForm
    can_view_details = True
    column_sortable_list = ['company_id', 'title', 'location', 'duration']
    column_exclude_list = ['description']

    def __init__(self, *args, **kwargs):
        super(JobView, self).__init__(*args, **kwargs)
        self.name = 'Jobs'
