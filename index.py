import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'database-1.cproxahba7vr.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Admin1234'
app.config['MYSQL_DB'] = 'test_db'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)

#app.config['UPLOAD_FOLDER'] = './csv'



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/uploader', methods=['POST'])
def uploader():
        #obtener archivo
        f1 = request.files["file1"]
        f2 = request.files["file2"]
                        #se puede montar a S3 con los respectivos permisos y SDK

        #leerlos mediante pandas
        pandas_f1 = pd.read_excel(f1)
        pandas_f2 = pd.read_excel(f2)

        #pasarlo a dataframe para manipularlos
        df1 = pd.DataFrame(pandas_f1)
        df2 = pd.DataFrame(pandas_f2)

        #--------LIMPIEZA DE DATOS-------

        #interseccion entre los dos archivos
        df_clean = df1.merge(df2, how = 'outer')

        #eliminar las columnas requeridas
        df_clean = df_clean.drop(['id','profesion','tipo_sangre','est_civil'], axis=1)

        #--------------IMPORTAR A BASE DE DATOS--------------------------------
        #conexion
        cur = mysql.connection.cursor()
        i = 0    
        for(row,rs) in df_clean.iterrows():
        
            nombre = rs[0]
            apellido = rs[1]
            edad = str(int(rs[2]))
            ciudad = rs[3]
            sexo = rs[4]

            #insercion de registros
            query = 'INSERT INTO table_test (nombre,apellido,edad,ciudad,sexo) VALUES ("'+nombre+'","'+apellido+'","'+edad+'","'+ciudad+'","'+sexo+'");'
            cur.execute(query)
            mysql.connection.commit()

        return render_template('actions.html')


def downLoad_GeneralReport():
    


def downLoad_DailyReport():
    return ''



if __name__ == '__main__':
    app.run() 