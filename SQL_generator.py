"""gunicorn server:app"""
"""import ipdb; ipdb.set_trace()"""
"""#SQL generator"""
import string
import sys
import psycopg2
import psycopg2.extras
import re
import array

#collect variables 
def query_name():
    return query
def case_no():    
    return case
def case_notes():
    return notes 
def count():
    return count
def data():
    return data

replacements = ("  ", " "), (" ", "%"), ("_", " ")

def multiple_replacer(key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)

def multiple_replace(string, key_values):
    return multiple_replacer(key_values)(string)

def split(s):
    if not s:
        return []
    l = s.split('\r\n')
    l = [multiple_replace(x, replacements) for x in l]
    return l
      
def clean_titles(title):
    return split(title)

def clean_comp(comp):
    return split(comp)
        
def clean_state(state):
    if not state:
        return []
    states_list = state.split('\r\n')
    states_list = [x.replace('_', ' ') for x in states_list]
    return states_list
    
def clean_city(city):
    if not city:
        return []
    cities_list = city.split('\r\n')
    cities_list = [x.replace('_', ' ') for x in cities_list]
    return cities_list
        
def clean_extitle(extitle):
    return split(extitle)

def clean_excomp(excomp):
    return split(excomp)
         
def gen_SQL(query, case, notes, title, comp, states_list, cities_list, extitle, excomp, expmin, expmax, count, data):
    txt = []
    txt.append("------------------------------------------------------------\n")
    txt.append("--" + query + ", " + "Case No: " + case)
    txt.append("--" + notes + "\n")
    if count:
        txt.append("--select profile_id, title_freeform, company_freeform, city_stnd, state_stnd")
        txt.append("select count(*)")
    if data:
        txt.append("select profile_id, title_freeform, company_freeform, city_stnd, state_stnd")
        txt.append("--select count(*)")
    txt.append("from coredb.profile where rtrim(ltrim(title_freeform)) is not null")
    if title:
        txt.append(' and (')
        txt.append(' or '.join(["title_freeform ilike '%%%s%%'\n" % c for c in title]))
        txt.append(')\n')
    if comp:
        txt.append(' and (')
        txt.append(' or '.join(["company_freeform ilike '%%%s%%'\n" % c for c in comp]))
        txt.append(')\n')
    if states_list:
        txt.append(' and state_stnd in (')
        txt.append(', \n '.join(["'%s'" % c for c in states_list]))
        txt.append(')\n')
    if cities_list:
        txt.append(' and city_stnd in (')
        txt.append(', \n '.join(["'%s'" % c for c in cities_list]))
        txt.append(')\n')
    if extitle:
        txt.append(' \n '.join(["and title_freeform not ilike '%%%s%%'" % c for c in extitle]))
    if extitle:
        txt.append(' \n '.join(["and company_freeform not ilike '%%%s%%'" % c for c in excomp]))
    if expmin:
        txt.append("and experience > " + expmin)
    if expmax:
        txt.append("and experience < " + expmax)
    if count:
        txt.append("--group by profile_id, title_freeform, company_freeform, city_stnd, state_stnd")
    if data:
        txt.append("group by profile_id, title_freeform, company_freeform, city_stnd, state_stnd")
        txt.append("limit 100 offset 0")
    txt.append("\n--------------------------------------------------------------\n")
    return '\n'.join(txt)
        
def main(query, case, notes, title, comp, states_list, cities_list, extitle, excomp, expmin, expmax, count, data):
    conn = psycopg2.connect("dbname='source' user='sourceuser' host='sourcing.ctnmvknyn5pi.us-east-1.redshift.amazonaws.com' password='1Page1page' port='5439'")
    cursor = conn.cursor('1-Page_Cursor', cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(gen_SQL(query, case, notes, title, comp, states_list, cities_list, extitle, excomp, expmin, expmax, count, data))
    #for record in cursor:
    #    return record
    while True:
        results = cursor.fetchmany(100)
        if not results:
            break
        for result in results:
            yield result
            
if __name__ == '__main__':
    import plac;
    plac.call(main)  

"""
while restart == 1:
    print gen_SQL(query, case, notes, title, comp, states_list, cities_list, extitle, excomp, exp, minmax)
    enrich_name = raw_input("\nCompany's Enrichment Name:")
    print "\n\n-----------------------------Step 1---------------------------------\n"
    print "insert into output." + enrich_name + "_enrichment_queue_archive select * from output." + enrich_name + "_enrichment_queue;"
    print "truncate table output." + enrich_name + "_enrichment_queue;"
    print "\n--------------------------------------------------------------------\n\n"
    print "-----------------------------Step 2---------------------------------\n"
    print "insert into output." + enrich_name + "_enrichment_queue"
    print "select profile_id from coredb.profile"
    print "where profile_id not in (select profile_id from output." + enrich_name + "_enrichment_queue_archive)"
    print "and profile_id not in (select profile_id from output." + enrich_name + "_enrichment_queue)"
    print "and ltrim(rtrim(title_freeform)) is not null"
    print "and ("
    print "     title_freeform ilike '%" + title[0] + "%'"
    for i in title[1:]:
        print "     or title_freeform ilike '%%%s%%'" % i
    print "     )"
    if not comp:
        print "and state_stnd in ("
        for i in states_list[:-1]:
            print "'%s'," % i
        print "'" + states_list[-1] + "')"
        print "and city_stnd in ("
        for i in cities_list[:-1]:
            if "'" in i or "," in i:
                print "%s" % i
            else:
                print "'%s'," % i
        if "'" in cities_list[-1] or "," in cities_list[-1]:
            print cities_list[-1]+ ")"
        else:
            print "'" + cities_list[-1] + "')"
        for i in extitle:
            print "and title_freeform not ilike '%%%s%%'" % i
        for i in excomp:
            print "and company_freeform not ilike '%%%s%%'" % i
        print "and experience > " + exp
        print "--group by profile_id, title_freeform, company_freeform, city_stnd, state_stnd"
        print "\n--------------------------------------------------------------"
    else:
        print "and ("
        print "     company_freeform ilike '%" + comp[0] + "%'"
        for i in comp[1:]:
            print "     or company_freeform ilike '%%%s%%'" % i
        print "     )\n"
        print "and state_stnd in ("
        for i in states_list[:-1]:
            print "'%s'," % i
        print "'" + states_list[-1] + "')"
        print "and city_stnd in ("
        for i in cities_list[:-1]:
            if "'" in i or "," in i:
                print "%s" % i
            else:
                print "'%s'," % i
        if "'" in cities_list[-1] or "," in cities_list[-1]:
            print cities_list[-1]+ ")"
        else:
            print "'" + cities_list[-1] + "')"
        for i in extitle:
            print "and title_freeform not ilike '%%%s%%'" % i
        for i in excomp:
            print "and company_freeform not ilike '%%%s%%'" % i
        print "and experience > " + exp
        print "--group by profile_id, title_freeform, company_freeform, city_stnd, state_stnd"
        print "\n--------------------------------------------------------------"
    print "\n\n----------------------------Step 3-------------------------------\n"
    print "insert into output." + enrich_name + "_enriched_pools_archive select * from output.XYZ_enriched_pools;"
    print "truncate table output." + enrich_name + "_enriched_pools;"
    print "  "
    print "\n------------------------------------------------------------------\n\n"
    print "-----------------------------Step 4-------------------------------\n"
    print "insert into output." + enrich_name + "_enriched_pools"
    print "select 'Company Name' as company, 'Admin Pool - Position' as pool_name, profile_id from coredb.profile"
    print "where ltrim(rtrim(title_freeform)) is not null"
    print "and ("
    print "     title_freeform ilike '%" + title[0] + "%'"
    for i in title[1:]:
        print "     or title_freeform ilike '%%%s%%'" % i
    print "     )"
    if not comp:
        print "and state_stnd in ("
        for i in states_list[:-1]:
            print "'%s'," % i
        print "'" + states_list[-1] + "')"
        print "and city_stnd in ("
        for i in cities_list[:-1]:
            if "'" in i or "," in i:
                print "%s" % i
            else:
                print "'%s'," % i
        if "'" in cities_list[-1] or "," in cities_list[-1]:
            print cities_list[-1]+ ")"
        else:
            print "'" + cities_list[-1] + "')"
        for i in extitle:
            print "and title_freeform not ilike '%%%s%%'" % i
        for i in excomp:
            print "and company_freeform not ilike '%%%s%%'" % i
        print "and experience > " + exp
        print "--group by profile_id, title_freeform, company_freeform, city_stnd, state_stnd"
        print "\n--------------------------------------------------------------"
    else:
        print "and ("
        print "     company_freeform ilike '%" + comp[0] + "%'"
        for i in comp[1:]:
            print "     or company_freeform ilike '%%%s%%'" % i
        print "     )\n"
        print "and state_stnd in ("
        for i in states_list[:-1]:
            print "'%s'," % i
        print "'" + states_list[-1] + "')"
        print "and city_stnd in ("
        for i in cities_list[:-1]:
            if "'" in i or "," in i:
                print "%s" % i
            else:
                print "'%s'," % i
        if "'" in cities_list[-1] or "," in cities_list[-1]:
            print cities_list[-1]+ ")"
        else:
            print "'" + cities_list[-1] + "')"
        for i in extitle:
            print "and title_freeform not ilike '%%%s%%'" % i
        for i in excomp:
            print "and company_freeform not ilike '%%%s%%'" % i
        print "and experience > " + exp
        print "--group by profile_id, title_freeform, company_freeform, city_stnd, state_stnd"
        print "\n--------------------------------------------------------------"
    restart = 0
"""