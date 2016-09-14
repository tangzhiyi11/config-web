from flask import render_template, redirect, url_for
from models import Modules, Commands, AddForm, ShowForm, GenShellForm, ShowGenShellForm
from utils import add_module, update_module, gen_shell, show_gen_form
from app import db
from config import config
from . import main


@main.route('/',methods=['GET', 'POST'])
def update_index():
	gen_form = GenShellForm()
	show_form = ShowGenShellForm()
	show_form.show.data = show_gen_form()
	if gen_form.validate_on_submit():
		gen_shell(config['path'])
		return redirect(url_for('main.update_index'))
	return render_template('index.html',gen_form = gen_form, show_form=show_form)


@main.route('/test')
def update_test():
	return '<h1>this is for test!</h1>'


@main.route('/gen_shell')
def update_gen_shell():
	return '<h1>this is gen_shell page!</h1>'


@main.route('/config', methods=['GET','POST'])
def update_config():
	modules = Modules.query.order_by(Modules.execute_id).all()
	add_form = AddForm()
	module_value = []
	module_form = ShowForm()
	if module_form.validate_on_submit():
		form_module_id = int(module_form.module_id.data)
		form_module_name = module_form.name.data
		form_execute_id = int(module_form.execute_id.data)
		form_commands = module_form.commands.data
		cmd_list = form_commands.split('\r\n')
		update_module(form_module_id, form_module_name, form_execute_id, cmd_list)
		return redirect(url_for('main.update_config'))

	if add_form.validate_on_submit():
		module_name = add_form.name.data
		commands = add_form.commands.data
		cmd_list = commands.split('\r\n')
		execute_id = int(add_form.execute_id.data)
		add_module(module_name, execute_id, cmd_list)
		add_form.name.data = ''
		add_form.commands.data = ''
		add_form.execute_id.data = ''
		return redirect(url_for('main.update_config'))
	for m in modules:
		cmd = Commands.query.filter_by(module_id=m.id).order_by(Commands.execute_id).all()
		cmd_list = [c.cmd for c in cmd]
		show = ShowForm()
		show.module_id.data = m.id
		show.name.data = m.name
		show.execute_id.data = str(m.execute_id)
		show.commands.data =  '\r\n'.join(cmd_list)
		item = [m, show]
		module_value.append(item)
	return render_template('config.html',modules=module_value, add_form=add_form)
