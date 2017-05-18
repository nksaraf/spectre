from setuptools import setup

setup(
	name= "spectre",
	version= "1.0",
	py_modules= ["spectre"],
	install_requires= [
		"click",
	],
	entry_points='''
		[console_scripts]
		spectre=cli:cli
	'''
)