from sqlalchemy import Table, Column, MetaData, String
from sqlalchemy.dialects import postgresql
from sqlalchemy import create_engine
from sqlalchemy import insert, delete, select
import os

engine = create_engine(
    os.environ["POSTGRES_URL"],
    echo = True,
)

connection = engine.connect()

metadata = MetaData()

authorised = Table(
    "authorised",
    metadata,
    Column('id',String,primary_key=True)
)

table = Table(
    "stickers",
    metadata,
    Column('file_id',String,primary_key=True),
    Column('file_unique_id',String),
    Column('data', postgresql.ARRAY(String)),
    Column('type',String)
)

metadata.create_all(engine)

def add_authorised(id:str) -> None:
    stmt = (
        insert(authorised).
        values(id=id)
    )
    connection.execute(stmt)

def remove_authorised(id:str) -> None:
    stmt = (
        delete(authorised).
        where(authorised.c.id==id)
    )
    connection.execute(stmt)

def is_authorised(id:str) -> bool:
    stmt = (
        select(authorised).
        where(authorised.c.id==id)
    )
    result = connection.execute(stmt)

    try:
        return result.fetchall()[0][0] == id
    except IndexError:
        return False

def add_sticker(file_id:str,file_unique_id:str,tags:list,type:str) -> None:
    stmt = (
        insert(table).
        values(file_id=file_id,file_unique_id=file_unique_id, data=tags, type=type)
    )
    connection.execute(stmt)

def delete_sticker(file_unique_id:str) -> None:
    stmt = (
        delete(table).
        where(table.c.file_unique_id==file_unique_id)
    )
    connection.execute(stmt)

def get_tags(file_unique_id:str)->list:
    stmt = (
        select(table.c.data).
        where(table.c.file_unique_id==file_unique_id)
    )
    return connection.execute(stmt).fetchall()
    
def add_tag(file_id:str,file_unique_id:str,new_tags:list,type:str) -> None:
    # not using postgres array_append because it only
    # supports single argument and not multiple

    old_tags = get_tags(file_unique_id)

    if old_tags != []:
        delete_sticker(file_unique_id)
        union = list(set(old_tags[0][0]).union(set(new_tags)))
    else:
        union = new_tags
    add_sticker(file_id,file_unique_id,union,type)

def remove_tag(file_id:str,file_unique_id,new_tags:list,type:str) -> None:
    # not using postgres array_remove because it only
    # supports single argument and not multiple

    old_tags = get_tags(file_unique_id)

    if old_tags != []:
        delete_sticker(file_unique_id)
        diff_list = list(set(old_tags[0][0]).difference(set(new_tags)))
    else:
        diff_list = new_tags
    add_sticker(file_id,file_unique_id,diff_list,type)


def fetch_sticker(tags:list)->list:
    stmt = (
        select(table.c.file_id,table.c.type).
        where(table.c.data.contains(tags))
    )
    result = connection.execute(stmt)

    temp_list = []
    for i in result.fetchall():
        temp_list.append(i)
    
    return temp_list