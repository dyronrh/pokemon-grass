from flask import Flask,request,jsonify
# from prettytable import PrettyTable

import requests
import json
# definiendo los API endpoit
url_pokemon_grass = 'https://pokeapi.co/api/v2/type/12'
url_evolution_change = 'https://pokeapi.co/api/v2/evolution-chain/'
url_version_group  = 'https://pokeapi.co/api/v2/version-group/'


app = Flask(__name__)
# def get_evol_chain(chain_i)



@app.route("/")
def grass():
	# importacion de librerias
	from prettytable import PrettyTable
	# seteando parametros de la tabla como el header
	x = PrettyTable()
	x.field_names = ['Número', 'Nombre','Cadena Evolutiva','Versión del juego']
	# realizando la peticion de la api de los pokemones tipo hierba
	solicitud = requests.get(url_pokemon_grass)
	respuesta = []
	data = []

	# validacion de la peticion si el estado de la respuesta es 200

	if solicitud.status_code == 200:
		r = json.loads(solicitud.text)
		# recorriendo la lista de los pokemones tipo hierba para extraer los datos necesarioa a tabular
		for pokemon in r['pokemon']:
			url_split = pokemon['pokemon']['url'].split('/')
			print("Id number:",url_split[-2])
			print("Evolution Chain URL:",'https://pokeapi.co/api/v2/evolution-chain/'+ url_split[-2])
			# recorriendo la evolucion del item en cuestion para obtener su cadena de evolucion

			stats = requests.get('https://pokeapi.co/api/v2/evolution-chain/'+ url_split[-2])
			print("Response Status: ",stats.status_code)
			evol_1,evol_2,evol_3 = ["","",""]
			versions_group = []
			# extracion de los datos de la evoluciones por cada pokemon tipo hierba
			if stats.status_code == 200:
				evolution = stats.json()
				for k,v in evolution.items():
				    print(len(evolution))
				    if k == 'chain':
				    	chain = json.dumps(v)
				    	print(len(chain))
				    	if len(chain) > 1300:
				    		if evolution['chain']['evolves_to'][0]['evolves_to'] != []:
				    			evol_3 = evolution['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']
				    			print(evolution['chain']['evolves_to'][0]['evolves_to'][0]['species']['name'])

				


				if evolution['chain']['species']['name'] != "":
					evol_1 = evolution['chain']['species']['name']
				if evolution['chain']['evolves_to'] != []:
					evol_2 = evolution['chain']['evolves_to'][0]['species']['name']
				# realizando la peticion para ver las versiones de este pokemon tipo hierba

				versions = requests.get(url_version_group + url_split[-2])

				if versions.status_code == 200:
					print(versions.json()['name'])
					versions_group = versions.json()['name'].split('-')
					vers_g = versions.json()['name'].split('-')

				else:
					versions_group = []

				# adicionando los valores del pokemon tipo hierba en la instancia alctual del loops

				x.add_row([url_split[-2],pokemon['pokemon']['name'],[evol_1, evol_2, evol_3] , versions_group])
				
				# data.append([url_split[-2],pokemon['pokemon']['name'],[ evol_1, evol_2, evol_3],versions_group])
				# adicionando el item pokemon a la lista que sera retornada como respuesta de la api
				respuesta.append({"grass_type":{
					'id':url_split[-2],
					'nombre': pokemon['pokemon']['name'],
					'evolution':{
						'evol_1': evol_1,
						'evol_2': evol_2,
						'evol_3': evol_3
					},
					'versions': versions_group
					}})

		# imprimiento la tabla de los pokemones tipo hieba
		print(x)
		return jsonify(respuesta)
	else:
		return jsonify({"respuesta":"item no disponible!!!"})
 

if __name__ == '__main__':
   app.run(debug = True)

