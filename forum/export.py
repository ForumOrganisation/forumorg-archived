from __future__ import print_function
from flask_admin._compat import csv_encode
import sys


def log(m):
    print(m, file=sys.stderr)


# Export utility
def generate_vals(writer, export_type, data):
    titles = ['id_entreprise']
    if export_type == 'equipement':
        titles += ['duration', 'equiped', 'banner', 'size', 'bandeau', 'emplacement']
        titles += data[0]['sections']['equipement']['furnitures'].keys()
        yield writer.writerow(titles)
        for row in data:
            vals = []
            for t in titles[:1]:
                vals.append(row.get('id', ''))
            for t in titles[1:7]:
                vals.append(row['sections']['equipement']['general'].get(t, 0))
            for t in titles[7:]:
                vals.append(row['sections']['equipement']['furnitures'][t].get('quantity'))
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'restauration':
        titles += ['mercredi_assis', 'mercredi_plateau', 'jeudi_assis', 'jeudi_plateau']
        yield writer.writerow(titles)
        for row in data:
            vals = []
            vals.append(row.get('id', ''))
            vals.append(row['sections']['restauration']['dishes']['mercredi'].get('Assis', 0))
            vals.append(row['sections']['restauration']['dishes']['mercredi'].get('Plateau-Repas', 0))
            vals.append(row['sections']['restauration']['dishes']['jeudi'].get('Assis', 0))
            vals.append(row['sections']['restauration']['dishes']['jeudi'].get('Plateau-Repas', 0))
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'transport':
        titles += ['departure_place', 'arrival_place', 'nb_persons', 'comment', 'phone', 'departure_time']
        yield writer.writerow(titles)
        for row in data:
            for t in row['sections']['transport']['transports']:
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
            for t in row['sections']['badges']['persons']:
                vals = []
                vals.append(row.get('id', ''))
                for title in titles[1:]:
                    vals.append(t.get(title, ''))
                vals = [csv_encode(v) for v in vals]
                yield writer.writerow(vals)
