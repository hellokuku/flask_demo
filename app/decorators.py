#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   Jianwei Fu
#   E-mail  :   jianwei1031@gmail.com
#   Date    :   15/12/28 12:15:01
#   Desc    :   
#

from functools import wraps
from flask import abort
from flask.ext.login import current_user
from .models import Permission
def permission_require(permission):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not current_user.can(permission):
				abort(403)
			return f(*args, **kwargs)
		return decorated_function
	return decorator

def admin_required(f):
	return permission_require(Permission.ADMINISTER)(f)