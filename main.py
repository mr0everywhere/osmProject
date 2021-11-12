import os
import sqlite3
from getset import *
import audit
import pandas as pd
from humanize import naturalsize
import fix
import pullphoenixosm
'''WARNING: FULL OSM IS OVER 2 GB AND TAKES A LONG TIME TO PULL AND FILL OUT OTHER FILES WITH 
APPROXIMITLY A 10 MINUTE RUN TIME ON MID TIER PERSONAL PC IS 15 MINUTES LAST OUTPUT IS TOP 10 CUISINES'''

'''look for lines in this style for full run instructions'''

'''remove the next 2 lines comment tags to get full osm'''
# pullphoenixosm.get_full_osm()
# pullphoenixosm.create_sample()
'''remove the comment tags from line 18-20 and comment out line 21 to run the full
osm through to create the database '''
audit.audit_address(get_small_osm())
# audit.audit_address(get_med_osm())
# audit.audit_address(get_osm_filename())
# fix.process_map(get_osm_filename())
fix.process_map(get_small_osm())

# Create database from text files
if os.path.isfile('phoenix.db'):
    os.remove('phoenix.db')
conn = sqlite3.connect('phoenix.db')
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
cur = conn.cursor()
cur.execute("CREATE TABLE nodes ("
            "id INTEGER PRIMARY KEY NOT NULL, "
            "lat REAL, "
            "lon REAL, "
            "user TEXT, "
            "uid INTEGER, "
            "version INTEGER, "
            "changeset INTEGER, "
            "timestamp TEXT )")
conn.commit()
node_df = pd.read_csv('nodes.csv', dtype=object)
node_df.to_sql('nodes', conn, if_exists='append', index=False)


cur.execute("CREATE TABLE nodes_tags (id INTEGER,\
    key TEXT,\
    value TEXT,\
    type TEXT,\
    FOREIGN KEY (id) REFERENCES nodes(id)\
)")
conn.commit()
nodetag_df = pd.read_csv('node_tags.csv')
nodetag_df.to_sql('nodes_tags', conn, if_exists='append', index=False)

cur.execute("CREATE TABLE ways (\
    id INTEGER PRIMARY KEY NOT NULL,\
    user TEXT,\
    uid INTEGER,\
    version TEXT,\
    changeset INTEGER,\
    timestamp TEXT\
)")
conn.commit()
way_df = pd.read_csv('ways.csv')
way_df.to_sql('ways', conn, if_exists='append', index=False)

cur.execute("CREATE TABLE ways_nodes (\
    id INTEGER NOT NULL,\
    node_id INTEGER NOT NULL, \
    position INTEGER NOT NULL, \
    FOREIGN KEY (id) REFERENCES ways(id),\
    FOREIGN KEY (node_id) REFERENCES nodes(id)\
)")
conn.commit()
waynode_df = pd.read_csv('way_nodes.csv')
waynode_df.to_sql('ways_nodes', conn, if_exists='append', index=False)


cur.execute("CREATE TABLE ways_tags (\
    id INTEGER NOT NULL,\
    key TEXT NOT NULL,\
    value TEXT NOT NULL,\
    type TEXT,\
    FOREIGN KEY (id) REFERENCES ways(id)\
)")
conn.commit()
waytag_df = pd.read_csv('way_tags.csv')
waytag_df = waytag_df.dropna(subset=['id', 'key', 'value'], how='any')
waytag_df.to_sql('ways_tags', conn, if_exists='append', index=False)
conn.commit()
# conn.close()
directory = os.getcwd()
for root, dirs, files in os.walk(directory, topdown=False):
    for name in files:
        f = os.path.join(root, name)
        print (name, naturalsize(os.path.getsize(f)))
# conn = sqlite3.connect('phoenix.db')
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
cur = conn.cursor()
query = 'SELECT count(id) FROM nodes; '
total_rows = 0
result = cur.execute(query)
for row in result:
    print 'Nodes in database:', row[0]
    total_rows += row[0]

query = 'SELECT count(id) FROM ways;'

result = cur.execute(query)
for row in result:
    print 'Ways in database:', row[0]
    total_rows += row[0]

query = 'SELECT count(id) FROM nodes_tags;'

result = cur.execute(query)
for row in result:
    print 'Nodes Tags in database:', row[0]
    total_rows += row[0]

query = 'SELECT count(id) FROM ways_nodes;'

result = cur.execute(query)
for row in result:
    print 'Ways Nodes in database:', row[0]
    total_rows += row[0]

query = 'SELECT count(id) FROM ways_tags;'

result = cur.execute(query)
for row in result:
    print 'Ways Tags in database:', row[0]
    total_rows += row[0]

print '\nTotal Rows in database:\033[1m', total_rows, "\033[0m"

query = 'SELECT count(distinct(user)) FROM (' \
        'SELECT user FROM nodes ' \
        'UNION ALL SELECT user FROM ways);'
result = cur.execute(query)
for row in result:
    print '\nTotal users that contributed: ', row[0]

query = 'SELECT user, count(*) ' \
        'FROM nodes GROUP BY user ' \
        'ORDER BY count(*) DESC limit 10;'
print '\nThe top 10 contributors:'
for row in cur.execute(query):
    print (row)

query = 'SELECT DISTINCT key, Count(*) AS [Count] ' \
        'FROM nodes_tags GROUP BY nodes_tags.key ' \
        'ORDER BY Count(*) DESC limit 10;'

result = cur.execute(query)
print '\nTop 10 distinct keys:'
for row in result:
    print (row)

query = "SELECT DISTINCT value, Count(*) AS [Count] " \
        "FROM nodes_tags GROUP BY value, key HAVING (((key)='brand')) " \
        "ORDER BY Count(*) DESC limit 10;"

result = cur.execute(query)
print '\nTop 10 brands keys:'
for row in result:
    print (row)

query = "SELECT nodes_tags.value, COUNT(*) as num " \
        "FROM nodes_tags JOIN (SELECT DISTINCT(id) " \
        "FROM nodes_tags WHERE value='restaurant') i " \
        "ON nodes_tags.id=i.id WHERE nodes_tags.key='cuisine' " \
        "GROUP BY nodes_tags.value ORDER BY num DESC LIMIT 10;"

result = cur.execute(query)
print '\nTop 10 cuisines:'
for row in result:
    print (row)
conn.close()
