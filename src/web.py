import json
import os
import time
import re

from flask import Flask, render_template, request

from OPE import OPE
from help_functions import get_longer_path, read_file, read_file_string, matched_brackets, path_strings, \
	find_closest_value, operator_string, property_type, solve_expression

app = Flask(__name__)

last_query = ''


@app.route('/')
def index():
	return render_template('index.jinja2')


@app.route('/search')
def search():
	return render_template('search.jinja2')


@app.route('/search', methods=['POST'])
def search_result():
	global last_query
	start_time = time.time()

	query = request.form.get('query')

	ope = OPE()

	if query:
		query_split = [x.strip() for x in re.split(r'[()]', query) if x.strip()]

		brackets_ok = matched_brackets(query)
		if (brackets_ok):
			if (len(query_split) == 0):
				return {'status': 0, 'message': 'Query cannot be empty.'}

			res = []
			for q in query_split:
				parameters = q.split(' ')

				if (len(parameters) == 1 and (parameters[0] == 'AND' or parameters[0] == 'OR')):
					res.append(parameters[0])
				elif ('AND' not in parameters and 'OR' not in parameters):  # only one condition
					if (len(parameters) < 3):
						return {'status': 0, 'message': 'Query is not correct.'}

					property = parameters[0]
					path_string = path_strings(property)
					operator = parameters[1]
					value = ' '.join(parameters[2:])

					curr_value, position = find_closest_value(path_string, operator, value, property_type(property))

					token = ope.generate_search_token(path_string + curr_value)
					doc_ids = ope.search(token, operator_string(operator), position)
					res.append(doc_ids)
				else:
					and_operators = [i for i, j in enumerate(parameters) if j == 'AND']
					or_operators = [i for i, j in enumerate(parameters) if j == 'OR']
					and_or_operators = and_operators + or_operators
					and_or_operators.sort()

					i = 0
					part_res = []
					while (i < len(parameters)):
						if (i in and_or_operators):
							part_res.append(parameters[i])
						elif (i == 0 or i - 1 in and_or_operators):  # property
							property = parameters[i]
							path_string = path_strings(property)
						elif (i == 1 or i - 2 in and_or_operators):  # operator
							operator = parameters[i]
						elif (i == 2 or i - 3 in and_or_operators):  # start of value
							val = []
							while (i < len(parameters) and i not in and_or_operators):
								val.append(parameters[i])
								i += 1
							i -= 1
							value = ' '.join(val)

							curr_value, position = find_closest_value(path_string, operator, value,
																	  property_type(property))

							token = ope.generate_search_token(path_string + curr_value)
							doc_ids = ope.search(token, operator_string(operator), position)
							part_res.append(doc_ids)
						i += 1

					# solve part_res in save into res
					part_res = solve_expression(part_res)
					res += part_res

			# solve res
			res = solve_expression(res)

			# clear directory, copy encrypted files and decrypt them
			ope.delete_user_directories()
			if (len(res) == 1):
				num_of_files = ope.copy_encrypted_files_to_user(res[0])
				ope.decrypt_documents()
				end_time = time.time()
				last_query = query

				return {'status': 1, 'match': num_of_files, 'time': "{0:.1f}".format(1000 * (end_time - start_time))}
			else:
				return {'status': 0, 'message': 'res does not have one element.'}
		else:
			return {'status': 0, 'message': 'Brackets are not set correctly.'}

	###
	else:
		return {'status': 0, 'message': 'Query cannot be empty.'}


@app.route('/data', methods=['GET'])
def data():
	name = request.args.get('name')

	if (name):
		file = read_file_string(get_longer_path('data') + name)
		print(file)
		parsed = json.loads(file)
		dump = json.dumps(parsed, indent=4)
		return render_template('show_data.jinja2', name=name, file=dump)
	else:

		files = os.listdir(get_longer_path('data'))
		return render_template('all_data.jinja2', files=files)


@app.route('/en_decrypt')
def en_decrypt():
	global last_query
	user_enc = []
	user_dec = []

	user_enc_files = os.listdir(get_longer_path('user_enc'))
	for file in user_enc_files:
		user_enc.append({'name': file, 'content': read_file_string(get_longer_path('user_enc') + file)})

	user_dec_files = os.listdir(get_longer_path('user_dec'))
	for file in user_dec_files:

		parsed = json.loads(read_file_string(get_longer_path('user_dec') + file))
		dump = json.dumps(parsed, indent=4)
		user_dec.append({'name': file, 'content': dump})

	return render_template('en_decrypt.jinja2', query=last_query, user_enc=user_enc, user_dec=user_dec)


if __name__ == '__main__':
	app.debug = True
	app.run()
