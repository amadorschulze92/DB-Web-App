from __future__ import unicode_literals
from werkzeug import Response
from json import dumps as json_dumps
from render import render
import string
import sys
import SQL_generator

def css(req):
    return Response(render('home.css'),
                    mimetype='text/css')

def home(req):
    rows = 500
    page = req.values.get('page', 0, type=int)
    q = req.values.get('q', '').strip()
    return Response(render('home.jinja2'), mimetype='text/html')

def get_var(req):
    query = req.values.get('query1')
    case = req.values.get('case1')
    notes = req.values.get('notes1')
    title = SQL_generator.clean_titles(req.values.get('title1'))
    comp = SQL_generator.clean_comp(req.values.get('comp1'))
    states_list = SQL_generator.clean_state(req.values.get('state1'))
    cities_list = SQL_generator.clean_city(req.values.get('city1'))
    extitle = SQL_generator.clean_extitle(req.values.get('extitle1'))
    excomp = SQL_generator.clean_comp(req.values.get('excomp1'))
    expmin = req.values.get('expmin1')
    expmax = req.values.get('expmax1')
    count = req.values.get('count1')
    data = req.values.get('data1')
    sql = SQL_generator.gen_SQL(query, case, notes, title, comp, states_list, cities_list, extitle, excomp, expmin, expmax, count, data)
    return Response(sql)
    
def run(req):
    query = req.values.get('query')
    case = req.values.get('case')
    notes = req.values.get('notes')
    title = SQL_generator.clean_titles(req.values.get('title'))
    comp = SQL_generator.clean_comp(req.values.get('comp'))
    states_list = SQL_generator.clean_state(req.values.get('state'))
    cities_list = SQL_generator.clean_city(req.values.get('city'))
    extitle = SQL_generator.clean_extitle(req.values.get('extitle'))
    excomp = SQL_generator.clean_comp(req.values.get('excomp'))
    expmin = req.values.get('expmin')
    expmax = req.values.get('expmax')
    count = req.values.get('count')
    data = req.values.get('data')
    sql = SQL_generator.gen_SQL(query, case, notes, title, comp, states_list, cities_list, extitle, excomp, expmin, expmax, count, data)
    run = SQL_generator.main(query, case, notes, title, comp, states_list, cities_list, extitle, excomp, expmin, expmax, count, data)
    print sql
    return Response(run, mimetype='text/html') 

def blah(req):
    return Response("blah")

def tag_json(req):
    title = req.values.get('title')
    tags = tt.tag(title)
    return Response(json_dumps(tags), mimetype='application/json')
