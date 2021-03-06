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
import pathlib

DIRECTORIO_ARCHIVOS = str(pathlib.Path(__file__).parent.absolute()) 
MAX_CONTENT_LENGTH  = 16 * 1024 * 1024

# son los clasificadores que se van a usar en el analisis
CLASIFICADORES_2    = ['DT','LR']  

CLASIFICADORES    = ['MLP','GB','NB','KNN','RF','DT','LR']  
ARCHIVOS_PERMITIDOS = set(['csv', 'xlsx', 'xls'])

URL_CONEXION     = "mongodb://localhost:27017/"
NOMBRE_BD        = 'db'
NOMBRE_COLECCION = 'clima'    
NOMBRE_COLECCION_CLASIFICADOR = 'mejor_clasificador'