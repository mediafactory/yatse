# -*- coding: utf-8 -*-
import datetime

def clean_search_values(search):
    result = {}
    for ele in search:
        if type(search[ele]) not in [bool, int, str, unicode, long, None, datetime.date]:
            if search[ele]:
                result[ele] = search[ele].pk
        else:
            result[ele] = search[ele]
    return result

def add_breadcrumbs(request, pk, typ, serverName=None):
    breadcrumbs = request.session.get('breadcrumbs', [])
    # checks if already exists
    if len(breadcrumbs) > 0:
        if breadcrumbs[-1][0] != pk or breadcrumbs[-1][1] != typ:
            if (pk, typ,) in breadcrumbs:
                breadcrumbs.pop(breadcrumbs.index((pk, typ,)))
            if typ == '#':
                server, ticket = pk.split('@')
                breadcrumbs.append((pk, typ, server, ticket, serverName, ))
            else:
                breadcrumbs.append((pk, typ,))

    else:
        if typ == '#':
            server, ticket = pk.split('@')
            breadcrumbs.append((pk, typ, server, ticket, serverName, ))
        else:
            breadcrumbs.append((pk, typ,))
    while len(breadcrumbs) > 10:
        breadcrumbs.pop(0)
    request.session['breadcrumbs'] = breadcrumbs

def fieldNameToTracName(field):
    if field == 'c_date':
        return 'time created'
    if field == 'c_user':
        return 'reporter'
    if field == 'u_date':
        return 'time changed'
    if field == 'assigned':
        return 'owner'
    if field == 'caption':
        return 'summary'
    if field == 'state':
        return 'status'

    return field.replace('_', ' ')

def prettyValues(values):
    result = {}
    for field in values:
        if field == 'caption':
            if values[field]:
                result[fieldNameToTracName(field)] = values[field]
        else:
            result[fieldNameToTracName(field)] = values[field]
    return result
