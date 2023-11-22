import fdb

HOSTNAME = '10.137.2.146'
DATABASE_PATH = r'D:\svxbase\svx.fdb'
USERNAME = 'SYSDBA'
PASSWORD = 'masterkey'

QUERY = """
select first 5 (uvedoc.nomztk ||'/'||substring(uvedoc.drazm from 4 for 1)||'9'|| 
substring (sum(1000000 + uvedoc.numitem) / count(prildoc.docid) from 2 for 7)) as numer,
uvedoc.drazm,
uvedoc.numitem,
uvedoc.transp_num,
LIST (prildoc.numdoc, '; ') as numdoc,
LIST (prildoc.typdid, '; ') as typdid,
LIST(NSITYPDOC.naim,'; ') as naim,
LIST(prildoc.dtdoc, '; ') as dtdoc,
uvedoc.docstate,
uvedoc.date_ss,
uvedoc.regnum_pto,
LIST(custrazr.numtd, ';') as numtd
from uvedoc
left outer join prildoc on uvedoc.docid = prildoc.docid
left outer join NSITYPDOC on prildoc.typdid = NSITYPDOC.typdid
left outer join custrazr on uvedoc.docid = custrazr.docid
where
uvedoc.drazm >= current_date -1
group by uvedoc.nomztk, uvedoc.drazm, uvedoc.numitem, uvedoc.transp_num, uvedoc.docstate, uvedoc.date_ss,
uvedoc.regnum_pto
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
