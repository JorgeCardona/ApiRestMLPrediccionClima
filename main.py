############################################################################################
################################ Descripcion################################################
__author__ = "Jorge Cardona"
__copyright__ = "Copyright 2020, The Cogent Project"
__credits__ = "Jorge Cardona"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Jorge cardona "
__email__ = "https://github.com/JorgeCardona"
__status__ = "Production"
###############################################################################################
###############################################################################################

import os
import urllib.request
from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect
import numpy as np
import json
from configuraciones.config import DIRECTORIO_ARCHIVOS
from configuraciones.config import MAX_CONTENT_LENGTH
from configuraciones.config import ARCHIVOS_PERMITIDOS
from configuraciones.config import MAX_CONTENT_LENGTH
from configuraciones.config import ARCHIVOS_PERMITIDOS
from servicios.servicios import  Servicios

nombre_columna_binarizada = 'HumedadBinarizadaPrediccion'
columna_decision = 'relative_humidity_3pm' 
limite_binarizacion = 24.99
split = 0.3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DIRECTORIO_ARCHIVOS
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

ALLOWED_EXTENSIONS = ARCHIVOS_PERMITIDOS

def archivos_permitidos(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ARCHIVOS_PERMITIDOS


@app.route('/consultar_prediccion', methods=['POST'])
def prediccion():
    	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'La Key es Incorrecta, debe llamarse file'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No se Adjunto Ningun Archivo'})
		resp.status_code = 400
		return resp
	if file and archivos_permitidos(file.filename):
		filename = file.filename
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		
		# guarda el archivo cargado en base de datos
		prediccion = Servicios().predecir(DIRECTORIO_ARCHIVOS + '\\' + filename, nombre_columna_binarizada, columna_decision, limite_binarizacion)
		servicio = json.dumps({'prediccion' : prediccion})
		#resp.status_code = 201
		return servicio
	else:
		resp = jsonify({'message' : 'Solo se Aceptan los formatos' + str (ARCHIVOS_PERMITIDOS)})
		resp.status_code = 400
		return resp

	return json.dumps({'resultado_modelos': datos})


@app.route('/consultar_mejor_modelo', methods=['GET'])
def mejor_modelo():
    	
	datos = list(Servicios().entrenar_modelo(columna_decision, nombre_columna_binarizada, split))

	return json.dumps({'resultado_modelos': datos})
    	
# endpoint para carga de archivos
@app.route('/guardar_en_db', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'La Key es Incorrecta, debe llamarse file'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No se Adjunto Ningun Archivo'})
		resp.status_code = 400
		return resp
	if file and archivos_permitidos(file.filename):
		filename = file.filename
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		# guarda el archivo cargado en base de datos
		Servicios().procesar_informacion(DIRECTORIO_ARCHIVOS + '\\' + filename, nombre_columna_binarizada, columna_decision, limite_binarizacion)
		resp = jsonify({'message' : 'Archivo Alojado Satisfactoriamente en: ' + DIRECTORIO_ARCHIVOS + '\\' + filename + 'y grabado en base de datos satistactoriamente'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Solo se Aceptan los formatos' + str (ARCHIVOS_PERMITIDOS)})
		resp.status_code = 400
		return resp

if __name__ == "__main__":
    app.run()
