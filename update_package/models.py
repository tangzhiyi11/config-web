from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField,HiddenField
from wtforms.validators import Required,DataRequired
from app import db


class Modules(db.Model):
	__tablename__ = 'modules'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	execute_id = db.Column(db.Integer)

	def __repr__(self):
		return '<Module %r>' % self.name

class Commands(db.Model):
	__tablename__ = 'commands'
	id = db.Column(db.Integer, primary_key=True)
	cmd = db.Column(db.String(128))
	execute_id = db.Column(db.Integer)
	module_id = db.Column(db.Integer, db.ForeignKey('modules.id'))

	def __repr__(self):
		return '<Command %r>' % self.cmd

class AddForm(Form):
	name = StringField('input module name', validators=[DataRequired()])
	execute_id = StringField('input execute order', validators=[DataRequired()])
	commands = TextAreaField("input commands", validators=[DataRequired()])
	submit = SubmitField('add module')


class ShowForm(Form):
	name = StringField('name:',validators=[DataRequired()])
	execute_id = StringField('order:',validators=[DataRequired()])
	commands = TextAreaField('commands:',validators=[DataRequired()])
	submit = SubmitField('update module')
	module_id = HiddenField()


class GenShellForm(Form):
	gen_submit = SubmitField('generate shell file')


class ShowGenShellForm(Form):
	show = TextAreaField('shell file:')
