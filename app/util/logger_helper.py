# -*- coding: utf-8 -*-

from flask.ext.login import current_user

from .. import db
from ..models import OperationRecord

def add_log(operation_note, user_id=None):
    if user_id is None:
        user_id = current_user.id

    db.session.add(OperationRecord.new(user_id=user_id, operation_note=operation_note))
    db.session.commit()