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
import pandas as pd
import numpy as np
from datetime import datetime
from database.mongo import MongoDB
from database.consultas import AccesoDB

from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class ModelosML(object):
    
    def analisis_pca(self, dataframe_original, nombre_columna_binarizada):

        # eilimino la variable objetivo
        dataframe_original = dataframe_original.drop(columns=[nombre_columna_binarizada])

        modelo = PCA(n_components=5).fit(dataframe_original)
        
        pc = modelo.transform(dataframe_original)

        # obtiene el numero de componentes
        numero_componentes = modelo.components_.shape[0]

        # get the index of the most important feature on EACH component i.e. largest absolute value
        # obtiene la lista de los componentes mas importantes
        componentes_mas_importantes = [np.abs(modelo.components_[i]).argmax() for i in range(numero_componentes)]

        # crea una lista con las columnas del dataset
        nombres_columnas = list(dataframe_original.columns)

        # obtiene los nombres mas importantes
        nombres_mas_importantes = [nombres_columnas[componentes_mas_importantes[i]] for i in range(numero_componentes)]

        # crea un diccionario informativo con cada uno de los componentes de mayor a menor importancia
        diccionario = {'PC{}'.format(i+1): nombres_mas_importantes[i] for i in range(numero_componentes)}

        # crea la lista de los nombres de los componentes mas importantes
        lista_nombre_componentes_principales = [nombres_mas_importantes[i] for i in range(numero_componentes)]

        # retorna la lista con el nombre de los componentes principales
        return lista_nombre_componentes_principales


    # obtiene los valores de las metricas de losc lasificadores y realiza las graficas de estos, con sus metricas respectivas
    def obtener_metricas_clasificador (self, clasificador, y_test, cantidad_de_validaciones, resultado_cross_validation, prediccion_obtenida):     

        precision = 2
        # obtiene los valores de la validacion cruzada
        promedio_validacion_cruzada = round(np.mean(resultado_cross_validation) * 100, precision)
        variacion_validacion_cruzada = round(np.std(resultado_cross_validation) * 100, precision)    

        # calcula el area bajo la curva
        false_positive_rate, true_positive_rate, thresholds = metrics.roc_curve(y_test, prediccion_obtenida)
        # obtengo los valores del area bajo la curva
        area_bajo_la_curva           = round(metrics.auc(false_positive_rate, true_positive_rate) * 100, precision)
        valor_roc_area_bajo_la_curva = round(metrics.roc_auc_score(y_test, prediccion_obtenida) * 100, precision)            

        # genera la matriz de confusion y muestra un grafico de esta con el dataset evaluado    
        conf_matrix = metrics.confusion_matrix(y_test, prediccion_obtenida)
        conf_matrix = conf_matrix.tolist()
        conf_matrix_porcentual = []

        for i in range(len(conf_matrix)):

            conf_matrix_porcentual.append(round((conf_matrix[i][i] / sum(conf_matrix[i])) * 100, 2))

        conf_matrix_porcentual = sum(conf_matrix_porcentual) / len(conf_matrix_porcentual)

        # genera el acuracy del modelo
        accuracy = round(metrics.accuracy_score(y_test, prediccion_obtenida) * 100 ,precision)

        # genera la precision del modelo
        precision = round(metrics.precision_score(y_test, prediccion_obtenida) * 100 ,precision)
            
        evaluacion_clasificador = conf_matrix_porcentual - variacion_validacion_cruzada + accuracy + precision + valor_roc_area_bajo_la_curva

        # retorna los valores de medicion con su respectivo clasificador
        return {'clasificador' : clasificador, 'evaluacion_clasificador' : evaluacion_clasificador, 'Exito Matriz Confusion':conf_matrix_porcentual,'promedio_validacion_cruzada':promedio_validacion_cruzada, 'variacion_validacion_cruzada':variacion_validacion_cruzada, 'area_bajo_la_curva': area_bajo_la_curva, 'valor_roc_area_bajo_la_curva':valor_roc_area_bajo_la_curva, 'accuracy':accuracy, 'precision':precision}


    def obtener_mejor_clasificador(self, clasificador, conjunto_de_datos_para_clasificador, cantidad_de_validaciones, data_subida_para_prediccion):

        print('ffffff ', len(data_subida_para_prediccion))

        x_train, x_test, y_train, y_test  = conjunto_de_datos_para_clasificador
        mostrar_metricas = 0
        prediccion_obtenida = []

        if(len(data_subida_para_prediccion) > 0 ):

            x_test = data_subida_para_prediccion
            mostrar_metricas = 1


        # MLPClassifier    
        if(clasificador == 'MLP'):

            #genera un clasificador
            modelo_de_clasificacion =  MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
            
            #Entrena el modelo usando los sets de entrenamiento y dimensiones_de_analisis_test 
            modelo_de_clasificacion.fit(x_train,y_train)

            # guarada los datos de la prediccion
            prediccion_obtenida = modelo_de_clasificacion.predict(x_test)   
            
            #obtiene los resultados de la validacion cruzada para ver el comportamiento 
            valores_cross_validation = cross_val_score(modelo_de_clasificacion, x_train,y_train, cv=cantidad_de_validaciones)

        # GradientBoostingClassifier    
        elif(clasificador == 'GB'):

            #genera un clasificador
            modelo_de_clasificacion = GradientBoostingClassifier(n_estimators=1000, learning_rate = 1, max_features=2, max_depth = 10, random_state = 0)

            #Entrena el modelo usando los sets de entrenamiento y dimensiones_de_analisis_test 
            modelo_de_clasificacion.fit(x_train,y_train)

            # guarada los datos de la prediccion
            prediccion_obtenida = modelo_de_clasificacion.predict(x_test)   
            
            #obtiene los resultados de la validacion cruzada para ver el comportamiento 
            valores_cross_validation = cross_val_score(modelo_de_clasificacion, x_train,y_train, cv=cantidad_de_validaciones)

        # GradientBoostingClassifier    
        elif(clasificador == 'NB'):

            #genera un clasificador
            modelo_de_clasificacion = GaussianNB(priors=None, var_smoothing=1e-09)

            #Entrena el modelo usando los sets de entrenamiento y dimensiones_de_analisis_test 
            modelo_de_clasificacion.fit(x_train,y_train)

            # guarada los datos de la prediccion
            prediccion_obtenida = modelo_de_clasificacion.predict(x_test)   
            
            #obtiene los resultados de la validacion cruzada para ver el comportamiento 
            valores_cross_validation = cross_val_score(modelo_de_clasificacion, x_train,y_train, cv=cantidad_de_validaciones)
                
            
        # LogisticRegression    
        elif(clasificador == 'LR'):

            #genera un clasificador
            modelo_de_clasificacion = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')

            #Entrena el modelo usando los sets de entrenamiento y dimensiones_de_analisis_test 
            modelo_de_clasificacion.fit(x_train,y_train)

            # guarada los datos de la prediccion
            prediccion_obtenida = modelo_de_clasificacion.predict(x_test)   
            
            #obtiene los resultados de la validacion cruzada para ver el comportamiento 
            valores_cross_validation = cross_val_score(modelo_de_clasificacion, x_train,y_train, cv=cantidad_de_validaciones)
            
        # DecisionTreeClassifier    
        elif(clasificador == 'DT'):

            #genera un clasificador
            modelo_de_clasificacion = DecisionTreeClassifier(criterion="entropy", max_depth = 2)

            #Entrena el modelo usando los sets de entrenamiento y dimensiones_de_analisis_test 
            modelo_de_clasificacion.fit(x_train,y_train)

            # guarada los datos de la prediccion
            prediccion_obtenida = modelo_de_clasificacion.predict(x_test)   
            
            #obtiene los resultados de la validacion cruzada para ver el comportamiento 
            valores_cross_validation = cross_val_score(modelo_de_clasificacion, x_train,y_train, cv=cantidad_de_validaciones)    

        # RandomForestClassifier
        elif(clasificador == 'RF'):        

            #genera un clasificador
            modelo_de_clasificacion = RandomForestClassifier(n_estimators=100)

            #Entrena el modelo usando los sets de entrenamiento y dimensiones_de_analisis_test 
            modelo_de_clasificacion.fit(x_train,y_train)

            prediccion_obtenida = modelo_de_clasificacion.predict(x_test)
            
            #obtiene los resultados de la validacion cruzada para ver el comportamiento 
            valores_cross_validation = cross_val_score(modelo_de_clasificacion, x_train,y_train, cv=cantidad_de_validaciones)
            
        # KNeighborsClassifier
        elif(clasificador == 'KNN'):
            
            #genera un clasificador
            modelo_de_clasificacion = KNeighborsClassifier(n_neighbors=100)

            #Entrena el modelo usando los sets de entrenamiento y dimensiones_de_analisis_test 
            modelo_de_clasificacion.fit(x_train,y_train)

            # guarada los datos de la prediccion
            prediccion_obtenida = modelo_de_clasificacion.predict(x_test)
            
            #obtiene los resultados de la validacion cruzada para ver el comportamiento 
            valores_cross_validation = cross_val_score(modelo_de_clasificacion, x_train,y_train, cv=cantidad_de_validaciones)

        if (mostrar_metricas> 0):

            return prediccion_obtenida

        else:                   

            print(2222222222222222, prediccion_obtenida)

            # obtiene todos los valores de las metricas y realiza las graficas de cada clasificador usado en el modelo        
            metricas = self.obtener_metricas_clasificador (clasificador, y_test, cantidad_de_validaciones, valores_cross_validation, prediccion_obtenida)

            # retorna el valor de las metricas obtenidas
            return metricas
