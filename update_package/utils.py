from app import db
from models import Modules, Commands


def add_module(module_name, execute_id, cmd_list):
	mod = Modules(name=module_name, execute_id=execute_id)
	db.session.add(mod)
	db.session.commit()
	mod_id = get_module_id(module_name)
	add_commands(cmd_list, mod_id)


def get_module_id(module_name):
	mod_item = Modules.query.filter_by(name=module_name).first()
	return mod_item.id


def add_commands(cmd_list, module_id):
	order = 1
	for cmd in cmd_list:
		command = Commands(cmd=cmd, execute_id=order, module_id=module_id)
		db.session.add(command)
		order += 1
	db.session.commit()


def update_module(module_id, module_name, execute_id, cmd_list):
	module = Modules.query.filter_by(id=module_id).first()
	if module.name != module_name:
		module.name = module_name
		db.session.commit()
		module = Modules.query.filter_by(name=module_id).first()
	if module is None:
		return
	if module.execute_id == execute_id:
		update_without_execute_id(module_name, cmd_list)
	else:
		update_with_execute_id(module_name, execute_id, cmd_list)


def delete_commands(module_id):
	commands = Commands.query.filter_by(module_id=module_id).all()
	for command in commands:
		db.session.delete(command)
	db.session.commit()


def update_without_execute_id( module_name, cmd_list):
	module_id = get_module_id(module_name)
	delete_commands(module_id)
	add_commands(cmd_list, module_id)


def update_module_execute_id(module_id, new_execute_id):
	mod = Modules.query.filter_by(id=module_id).first()
	old_execute_id = mod.execute_id
	module_list_first = Modules.query.filter(Modules.execute_id > old_execute_id, Modules.execute_id <= new_execute_id).all()
	for module in module_list_first:
		module.execute_id -= 1
	mod.execute_id = new_execute_id
	db.session.commit()


def update_with_execute_id(module_name, execute_id, cmd_list):
	module_id = get_module_id(module_name)
	update_module_execute_id(module_id, execute_id)
	delete_commands(module_id)
	add_commands(cmd_list, module_id)


def gen_shell(file_path):
	with open(file_path,'w') as result_file:
		modules = Modules.query.filter(Modules.execute_id).order_by(Modules.execute_id).all()
		for module in modules:
			result_file.write('#'+module.name+'\n')
			commands = Commands.query.filter_by(module_id=module.id).order_by(Commands.execute_id).all()
			for command in commands:
				result_file.write(command.cmd+'\n')
			result_file.write('\n')

def show_gen_form():
	result = []
	modules = Modules.query.filter(Modules.execute_id).order_by(Modules.execute_id).all()
	for module in modules:
		result.append('#'+module.name)
		commands = Commands.query.filter_by(module_id=module.id).order_by(Commands.execute_id).all()
		for command in commands:
			result.append(command.cmd)
		result.append('\n')
	return '\r\n'.join(result)
