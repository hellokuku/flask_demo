#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Author  :   Jianwei Fu
#   E-mail  :   jianwei1031@gmail.com
#   Date    :   15/12/26 20:30:22
#   Desc    :   
#

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	MAIL_SERVER = 'smtp.126.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'yourEmail'  #os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = 'yourPassword'  #os.environ.get('MAIL_PASSWORD')
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'YourEmail'  #'Flasky Admin <flasky@example.com>'
	FLASKY_ADMIN = 'Admin_Email_here'  #os.environ.get('FLASKY_ADMIN')
	FLASKY_POSTS_PER_PAGE = 20


	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
        # DevelopMood
	'default': DevelopmentConfig
}
