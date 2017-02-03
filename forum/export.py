from __future__ import print_function
from flask_admin._compat import csv_encode
import sys


def log(m):
    print(m, file=sys.stderr)


# Export utility
def generate_vals(writer, export_type, data):
    titles = ['id_entreprise']
    if export_type == 'equipement':
        titles += ['duration', 'equiped', 'banner', 'size', 'emplacement']
        titles += [u'chauffeuse', u'mange_debout', u'presentoir', u'ecran_32', u'ecran_42', u'poste_2', u'poste_3', u'poste_6', u'poste_9']
        yield writer.writerow(titles)
        for row in data:
            vals = []
            for t in titles[:1]:
                vals.append(row.get('id', ''))
            for t in titles[1:6]:
                vals.append(row.get(t, 0))
            for t in titles[6:]:
                vals.append(row['sections']['furnitures'].get(t, 0))
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'restauration':
        titles += ['mercredi', 'jeudi']
        yield writer.writerow(titles)
        for row in data:
            vals = []
            vals.append(row.get('id', ''))
            vals.append(row['sections']['catering']['wed'].get('seated', 0))
            vals.append(row['sections']['catering']['thu'].get('seated', 0))
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'transport':
        titles += ['departure_place', 'arrival_place', 'nb_persons', 'comment', 'phone', 'departure_time']
        yield writer.writerow(titles)
        for row in data:
            for t in row['sections']['transports']:
                vals = []
                vals.append(row.get('id', ''))
                for title in titles[1:]:
                    vals.append(t.get(title, ''))
                vals = [csv_encode(v) for v in vals]
                yield writer.writerow(vals)
    if export_type == 'badges':
        titles += ['name', 'function', 'days']
        yield writer.writerow(titles)
        for row in data:
            for t in row['sections']['persons']:
                vals = []
                vals.append(row.get('id', ''))
                for title in titles[1:]:
                    vals.append(t.get(title, ''))
                vals = [csv_encode(v) for v in vals]
                yield writer.writerow(vals)
