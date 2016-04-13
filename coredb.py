import csv
import sys
import psycopg2


def main(limit):
    conn = psycopg2.connect("dbname='source' user='sourceuser' host='sourcing.ctnmvknyn5pi.us-east-1.redshift.amazonaws.com' password='' port='5439'")
    cur = conn.cursor()
    #cur.execute('select * from coredb.profile limit %s' % limit)
    cur.execute('select * from coredb.profile where profile_id in (select profile_id from coredb.profile order by random() limit %s) ' % limit)
    writer = csv.writer(sys.stdout, dialect='excel-tab')
    row = cur.fetchone()    
    while row:
        writer.writerow(row)
        row = cur.fetchone()    
    
    

if __name__ == '__main__':
    import plac
    plac.call(main)
