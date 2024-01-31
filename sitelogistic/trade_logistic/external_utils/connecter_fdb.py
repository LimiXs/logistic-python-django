import fdb

SETTINGS_PATH = r'C:\Program Files\Firebird\settings.txt'

with open(SETTINGS_PATH, 'r') as file:
    lines = file.readlines()

data = {}
for line in lines:
    key, value = line.strip().split('=')
    data[key.strip()] = value.strip().strip("'")

HOSTNAME = data.get('HOSTNAME')
DATABASE_PATH = data.get('DATABASE_PATH')
USERNAME = data.get('USERNAME')
PASSWORD = data.get('PASSWORD')

QUERY = """
SELECT (uvedoc.nomztk ||'/'||substring(uvedoc.drazm FROM 4 FOR 1)||'9'|| 
SUBSTRING(sum(1000000 + uvedoc.numitem) / count(prildoc.docid) FROM 2 FOR 7)) AS numer,
uvedoc.drazm,
uvedoc.numitem,
uvedoc.transp_num,
LIST (prildoc.numdoc, '; ') AS numdoc,
LIST (prildoc.typdid, '; ') AS typdid,
LIST(NSITYPDOC.naim,'; ') AS naim,
LIST(prildoc.dtdoc, '; ') AS dtdoc,
uvedoc.docstate,
uvedoc.date_ss,
uvedoc.regnum_pto,
LIST(custrazr.numtd, ';') AS numtd
FROM uvedoc
LEFT OUTER JOIN prildoc ON uvedoc.docid = prildoc.docid
LEFT OUTER JOIN NSITYPDOC ON prildoc.typdid = NSITYPDOC.typdid
LEFT OUTER JOIN custrazr ON uvedoc.docid = custrazr.docid
WHERE
uvedoc.drazm >= current_date -1
GROUP BY uvedoc.nomztk, uvedoc.drazm, uvedoc.numitem, uvedoc.transp_num,
uvedoc.docstate, uvedoc.date_ss, uvedoc.regnum_pto
"""
CYRILLIC_TO_LATIN = {
        'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O',
        'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X', 'а': 'a', 'е': 'e', 'о': 'o',
        'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x'
    }


def replace_cyrillic_with_latin(text):
    return ''.join(CYRILLIC_TO_LATIN.get(char, char) for char in text)


def get_data_fdb(hostname, database_path, username, password):
    dsn = f'{hostname}:{database_path}'
    con = fdb.connect(dsn=dsn, user=username, password=password)
    cur = con.cursor()
    cur.execute(QUERY)
    data = list(cur.fetchall())
    cur.close()
    con.close()

    records = []
    for i, row in enumerate(data):
        records.append(list(row))
    return records
