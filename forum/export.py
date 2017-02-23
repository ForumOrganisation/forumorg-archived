from __future__ import print_function
import sys
from flask_admin._compat import csv_encode
from werkzeug import secure_filename
from flask import stream_with_context, Response, redirect, flash
from flask_admin.babel import gettext
from flask_admin.helpers import get_redirect_target
import csv
import os


def log(m):
    print(m, file=sys.stderr)


def find_qty(key, size):
    import json
    import os
    if size != '4.5':
        size = str(int(float(size)))
    path = os.path.join(os.path.dirname(__file__), '../data/furnitures.json')
    data = json.load(open(path))
    res = [row for row in data if row['id'] == key]
    res = res[0].get('quantities').get(size)
    return res


def nb_dishes(size):
    if size <= 12:
        return 2
    elif 12 < size <= 18:
        return 4
    elif size > 18:
        return 6


def generate_vals(writer, export_type, data):
    if export_type == 'general':
        titles = ['email_etudiant']
        titles += ['fra', 'styf', 'master_class', 'joi']
        titles += ['name', 'first_name', 'year', 'specialty', 'school', 'tel']
        yield writer.writerow(titles)
        for row in data:
            vals = []
            vals.append(row.get('id', ''))
            for t in titles[1:5]:
                vals.append(row['events'].get(t, {}).get('registered', False))
            for t in titles[5:]:
                vals.append(row.get('profile', {}).get(t, ''))
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    else:
        titles = ['id_entreprise', 'valide']
    if export_type == 'equipement':
        titles += ['duration', 'equiped', 'banner', 'size', 'emplacement', 'pole']
        titles += ['chaise', 'table', 'banque_hotesse', 'tabouret', 'portemanteau', 'chauffeuse', u'mange_debout', u'presentoir', u'ecran_32', u'ecran_42', u'poste_2', u'poste_3', u'poste_6', u'poste_9']
        yield writer.writerow(titles)
        for row in data:
            vals = []
            vals.append(row.get('id', ''))
            vals.append(row.get('equipement'))
            for t in titles[2:8]:
                if t in ['emplacement', 'banner']:
                    vals.append(row.get(t, ''))
                else:
                    vals.append(row.get(t, 0))
            for t in titles[8:13]:
                val = row['sections']['furnitures'].get(t, 0)
                if row['equiped']:
                    val += int(find_qty(t, str(row.get('size'))))
                vals.append(val)
            for t in titles[13:]:
                val = row['sections']['furnitures'].get(t, 0)
                vals.append(val)
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'restauration':
        titles += ['mercredi', 'jeudi']
        yield writer.writerow(titles)
        for row in data:
            vals = []
            vals.append(row.get('id', ''))
            vals.append(row.get('restauration'))
            val_wed = row['sections']['catering']['wed'].get('seated', 0)
            val_thu = row['sections']['catering']['thu'].get('seated', 0)
            val_wed += nb_dishes(row.get('size'))
            val_thu += nb_dishes(row.get('size'))
            vals.append(val_wed)
            vals.append(val_thu)
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'transport':
        titles += ['departure_place', 'arrival_place', 'nb_persons', 'comment', 'phone', 'departure_time']
        yield writer.writerow(titles)
        for row in data:
            for t in row['sections']['transports']:
                vals = []
                vals.append(row.get('id', ''))
                vals.append(row.get('transport'))
                for tt in titles[2:]:
                    vals.append(t.get(tt, ''))
                vals = [csv_encode(v) for v in vals]
                yield writer.writerow(vals)
    if export_type == 'badges':
        titles += ['entreprise']
        titles += ['name', 'function', 'days']
        yield writer.writerow(titles)
        for row in data:
            for t in row['sections']['persons']:
                vals = []
                vals.append(row.get('id', ''))
                vals.append(row.get('badges'))
                vals.append(row.get('name', ''))
                for title in titles[3:]:
                    vals.append(t.get(title, ''))
                vals = [csv_encode(v) for v in vals]
                yield writer.writerow(vals)
    if export_type == 'programme':
        titles += ['conference', 'networking', 'webtv']
        yield writer.writerow(titles)
        for row in data:
            vals = []
            vals.append(row.get('id', ''))
            vals.append(row.get('programme'))
            for t in titles[2:]:
                vals.append(row['sections']['events'].get(t, False))
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)


def _export_fields(obj, export_type, return_url):
        count, data = obj._export_data()

        class Echo(object):
            def write(self, value):
                return value

        writer = csv.writer(Echo())
        data = [row for row in data if row['id'] != 'admin']
        gen_vals = generate_vals(writer, export_type, data)
        filename = obj.get_export_name(export_type='csv')
        disposition = 'attachment;filename=%s' % (
            secure_filename(filename.replace(obj.name, export_type)),)
        headers = {'Content-Disposition': disposition}
        mimetype = 'text/csv'
        if os.environ.get('DEBUG'):
            headers = None
            mimetype = 'text/plain'
        return Response(
            stream_with_context(gen_vals),
            headers=headers,
            mimetype=mimetype
        )


def _export(obj, export_type):
    return_url = get_redirect_target() or obj.get_url('.index_view')

    if not obj.can_export or (export_type not in obj.export_types):
        flash(gettext('Permission denied.'), 'error')
        return redirect(return_url)

    if export_type == 'csv':
        return obj._export_csv(return_url)
    else:
        return _export_fields(obj, export_type, return_url)
