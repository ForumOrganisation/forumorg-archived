from flask_admin._compat import csv_encode

# Export utility
# UNDER WORKS #

def generate_vals(writer, export_type, o_data):
    new_data = (r['sections'][export_type] for r in o_data)
    data = []
    for nr, od in zip(new_data, o_data):
        nr['company_id'] = od['id']
        data.append(nr)
    if export_type == 'equipement':
        titles = data[0]['general'].keys() + data[0]['furniture'].keys()
        titles = ['company_id'] + titles
        yield writer.writerow(titles)
        for row in data:
            vals = []
            for t in titles:
                if t in row['general']:
                    temp = row['general'].get(t)
                    if 'quantity' in temp:
                        vals += temp.get('quantity') if temp else ''
                    else:
                        vals += temp
                elif t in row['furniture']:
                    temp = row['general'].get(t, None)
                    if temp:
                        vals += temp.get('quantity')
                    else:
                        vals += ''
                else:
                    vals += [row['company_id']]
            # vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'restauration':
        titles = ['company_id'] + ['mercredi', 'jeudi']
        print(titles)
        yield writer.writerow(titles)
        for row in data:
            vals = [row.get('dishes').get(t, '0') for t in titles]
            vals = vals + row.get('name')
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'transport':
        titles = ['company_id'] + data[0]['transports'][0][0].keys()
        yield writer.writerow(titles)
        for row in data:
            vals = [row.get(t, '') for t in titles]
            vals = vals + row.get('name')
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
    if export_type == 'badges':
        titles = ['company_id'] + data[0]['persons'].keys()
        yield writer.writerow(titles)
        for row in data:
            vals = [row.get(t, '') for t in titles]
            vals = vals + row.get('name')
            vals = [csv_encode(v) for v in vals]
            yield writer.writerow(vals)
