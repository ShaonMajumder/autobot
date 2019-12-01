import shaonutil
primary_seperator = ':'


class language_parser:
	"""docstring for ClassName"""
	def __init__(self, filename, configdic):
		self.filename = filename
		self.configdic = configdic
		
			

	def get_session_title(self,lines):
		# session title
		count = 0
		for line in lines:
			count += 1
			if line.count('\t') == 0:
				param,value = [c.strip() for c in line.split(primary_seperator,1)]
				if 'run' in param:
					return value,lines[count:]

	def get_tasks_and_funcs_lines(self,lines):
		tasks = {}
		functions = {}
		c = 0
		task = []
		function = []
		currentTaskName = ''
		currentFuncName = ''
		currentObj = '' #task/func
		LineNumber = 1
		while c < len(lines):
			line = lines[c]
			if line.count('\t') == 1:
				param,value = [kc.strip() for kc in line.split(primary_seperator,1)]
				if 'task' in param or 'func' in param:
					if c > 0:
						if currentObj == 'task':
							tasks[currentTaskName] = lines[1:c]
							lines = lines[c:]
							c = 0
							currentTaskName = value
						elif currentObj == 'func':
							functions[currentFuncName] = lines[1:c]
							lines = lines[c:]
							c = 0
							currentFuncName = value

					if 'task' in param:
						currentObj = 'task'
						currentTaskName = value
						tasks[currentTaskName] = []
					elif 'func' in param:
						currentObj = 'func'
						currentFuncName = value
						functions[currentFuncName] = []
			else:
				if line.count('\t') > 1:
					lines[c] = line.strip()
				else:
					raise ValueError("Syntax Error at Line ",LineNumber)
			c += 1
			LineNumber += 1
		
		if c == len(lines):
			if c > 0:
				if currentObj == 'task':
					tasks[currentTaskName] = lines[1:c]
					lines = lines[c:]
					c = 0
					currentTaskName = value
				elif currentObj == 'func':
					functions[currentFuncName] = lines[1:c]
					lines = lines[c:]
					c = 0
					currentFuncName = value

		return tasks,functions


	def get_tasks_and_funcs_dic(self,tasks_or_obj):
		tasks = tasks_or_obj
		for key in tasks:
			task = tasks[key]
			taskd = {}
			startSequence = False
			sequenceLines = []
			for line in task:
				if 'sequence:>>>' in line:
					startSequence = True
				elif '<<<' in line:
					startSequence = False
					taskd['sequence'] = sequenceLines
					sequenceLines = []
				elif startSequence:
					sequenceLines.append(line)
				else:
					param,value = [kc.strip() for kc in line.split(primary_seperator,1)]
					taskd[param] = value
			tasks[key] = taskd
		return tasks


	def parse(self):
		language_dic = {}

		lines = shaonutil.file.read_file(self.filename)

		# get session title
		title,lines = self.get_session_title(lines)
		
		
		# get tasks and functions
		tasks,functions = self.get_tasks_and_funcs_lines(lines)
		tasks,functions = self.get_tasks_and_funcs_dic(tasks),self.get_tasks_and_funcs_dic(functions)
		

		language_dic[title] = {
			"tasks":tasks,
			"functions":functions,
		}

		if self.configdic["json"] == True:
			shaonutil.file.write_json(language_dic,"session_dic.json")

		return language_dic

		
	
def main():
	obj = language_parser(
		"github.tasks",
		{
			"json" : True,
		}
	)

	session_dic = obj.parse()


	#shaonutil.strings.nicely_print(session_dic)

if __name__ == '__main__':
	main()