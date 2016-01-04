#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author  :   Jianwei Fu
#   E-mail  :   jianwei1031@gmail.com
#   Date    :   15/12/26 20:48:56
#   Desc    :   
#

import unittest
from flask import current_app
from app import create_app, db
from app.models import User, Role, AnonymousUser, Permission


class BasicsTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_app_exists(self):
		self.assertFalse(current_app is None)

	def test_app_is_testing(self):
		self.assertTrue(current_app.config['TESTING'])


class UserModelTestCase(unittest.TestCase):
	def test_password_setter(self):
		u = User(password='cat')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u = User(password='cat')
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verification(self):
		u = User(password='cat')
		self.assertTrue(u.verify_password('cat'))
		self.assertFalse(u.verify_password('dog'))

	def test_password_salts_are_random(self):
		u = User(password='cat')
		u2 = User(password='dog')
		self.assertTrue(u.password_hash != u2.password_hash)

	def test_roles_and_permissions(self):
		Role.insert_roles()
		u = User(email='jianwei1031@gmail.com', password='wy101030')
		self.assertTrue(u.can(Permission.WRITE_ARTICLES))
		self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

	def test_anony_user(self):
		u = AnonymousUser()
		self.assertFalse(u.can(Permission.FOLLOW))