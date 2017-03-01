# -*- coding: utf-8 -*-
# Created by apple on 2017/2/21.

from ..log import log
from sqlalchemy.orm import Session, Query
from ..db import AppModel, AppVersionModel


class DB:
    @staticmethod
    def model_exists(session: Session, model, **query) -> Query:
        query = session.query(model).filter_by(**query)
        if query.count() == 0:
            log.debug('not find {}: {}'.format(model.__name__, query))
        else:
            return query
