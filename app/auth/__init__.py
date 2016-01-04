#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   Jianwei Fu
#   E-mail  :   jianwei1031@gmail.com
#   Date    :   15/12/27 14:52:05
#   Desc    :   
#

from flask import Blueprint

auth = Blueprint('auth', __name__)
from . import views