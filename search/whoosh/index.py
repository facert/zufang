import os
import datetime
from whoosh.index import create_in, open_dir, exists_in
from whoosh.filedb.filestore import FileStorage
from whoosh.writing import AsyncWriter

def get_index(index, schema, refresh=False):
    index_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), index)
    storage = FileStorage(index_dir)
    if exists_in(index_dir) and not refresh:
        ix = storage.open_index()
    else:
        # os.mkdir(index_dir)
        st = FileStorage(index_dir).create()
        ix = st.create_index(schema)
    return ix


def get_writer(ix):
    writer = AsyncWriter(ix)
    # writer = ix.writer()
    return writer


def update_index(document, writer, commit=True):
    # import pdb;pdb.set_trace()
    create_time = datetime.datetime.strptime(document['create_time'], "%Y-%m-%d %H:%M:%S")
    writer.update_document(
        url=document['url'],
        title=document['title'],
        description=document['description'],
        create_time=create_time
    )
    if commit:
        writer.commit()


def update_all_index(collection, schema, index='indexes'):
    ix = get_index(index, schema, refresh=True)
    writer = get_writer(ix)
    for document in collection.find({}):
        update_index(document, writer, False)
    writer.commit()



