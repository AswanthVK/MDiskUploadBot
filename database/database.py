from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os

import threading
import asyncio

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, UniqueConstraint, func


DB_URL = os.environ.get("DATABASE_URL", "")


def start() -> scoped_session:
    engine = create_engine(DB_URL, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

INSERTION_LOCK = threading.RLock()

class custom_caption(BASE):
    __tablename__ = "caption"
    id = Column(Integer, primary_key=True)
    caption = Column(String)
    
    def __init__(self, id, caption):
        self.id = id
        self.caption = caption

custom_caption.__table__.create(checkfirst=True)

class custom_apikey(BASE):
    __tablename__ = "apikey"
    id = Column(Integer, primary_key=True)
    apikey = Column(String)
    
    def __init__(self, id, apikey):
        self.id = id
        self.caption = apikey

custom_apikey.__table__.create(checkfirst=True)

async def update_apikey(id, apikey):
    with INSERTION_LOCK:
        cap = SESSION.query(custom_apikey).get(id)
        if not cap:
            cap = custom_apikey(id, apikey)
            SESSION.add(cap)
            SESSION.flush()
        else:
            SESSION.delete(cap)
            cap = custom_apikey(id, apikey)
            SESSION.add(cap)
        SESSION.commit()

async def update_caption(id, caption):
    with INSERTION_LOCK:
        cap = SESSION.query(custom_caption).get(id)
        if not cap:
            cap = custom_caption(id, caption)
            SESSION.add(cap)
            SESSION.flush()
        else:
            SESSION.delete(cap)
            cap = custom_caption(id, caption)
            SESSION.add(cap)
        SESSION.commit()

async def del_apikey(id):
    with INSERTION_LOCK:
        msg = SESSION.query(custom_apikey).get(id)
        SESSION.delete(msg)
        SESSION.commit()

async def del_caption(id):
    with INSERTION_LOCK:
        msg = SESSION.query(custom_caption).get(id)
        SESSION.delete(msg)
        SESSION.commit()

async def get_apikey(id):
    try:
        apikey = SESSION.query(custom_apikey).get(id)
        return apikey

async def get_caption(id):
    try:
        caption = SESSION.query(custom_caption).get(id)
        return caption
    finally:
        SESSION.close()
