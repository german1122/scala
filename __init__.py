########################################################################
#################        Importing packages      #######################
########################################################################
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
#from flask_bootstrap import Bootstrap
#from flask_datepicker import datepicker
#from Ruby.models import User
from flask_login import UserMixin
import sqlite3
#from flask_cors import CORS


########################
db = SQLAlchemy()

#Con la siguiente defincición permitimos que SQL nos entregue errores de su operación
#def error():
#    raise Exception('hello')

#db.create_function('error', 0, error)

#sqlite3.enable_callback_tracebacks(True)   # <-- !

#db.execute('select error()')
########################ADDED CODE FROM FLASK ORACLE
SQLALCHEMY_BINDS = {
'legal_arrendamiento': 'sqlite://legal_ap.db',
'legal_arrendamiento_a': 'sqlite://legal_ap_a.db'
# 'my_sql2': 'mysql://root:password@externalserver.domain.com/quickhowto2'
}
#Base.metadata.create_all(engine)
engine = create_engine('sqlite:///arrendamiento.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    #company = db.Column(db.String(1000))
class legal_ap(Base):
    __tablename__ = 'legal_ap'
    id = db.Column(db.Integer, primary_key=True)
    numero_contrato = db.Column(db.String)
    arrendadora = db.Column(db.String)
    RFC_arrendadora = db.Column(db.String)
    domicilio_arrendadora = db.Column(db.String)
    pagina_web = db.Column(db.String)
    apoderado_arrendadora = db.Column(db.String)
    facultades = db.Column(db.String)
    poliza = db.Column(db.String)
    fecha_poliza = db.Column(db.String)
    fedatario = db.Column(db.String)
    numero_notaria = db.Column(db.String)
    entidad = db.Column(db.String)
    folio_mercantil = db.Column(db.String)
    lugar_inscripcion = db.Column(db.String)
    fecha_inscripcion = db.Column(db.String)
    denominacion = db.Column(db.String)
    RFC_arrendataria = db.Column(db.String)
    nacionalidad = db.Column(db.String)
    giro = db.Column(db.String)
    telefonos = db.Column(db.String)
    email = db.Column(db.String)
    domicilio_arrendataria = db.Column(db.String)
    apoderado_arrendataria = db.Column(db.String)
    instrumento_arrendataria = db.Column(db.String)
    fecha_arrendataria = db.Column(db.String)
    fedatario_publico_arrendataria = db.Column(db.String)
    notaria_arrendataria = db.Column(db.String)
    entidad_arrendataria = db.Column(db.String)
    inscripcion_arrendataria = db.Column(db.String)
    lugar_inscripcion_arrendataria = db.Column(db.String)
    #fecha_inscripcion_arrendataria = db.Column(db.String)
    actos_corporativos = db.Column(db.String)
    facultades_apoderado = db.Column(db.String)
    poliza_apoderado = db.Column(db.String)
    fecha_poliza_apoderado = db.Column(db.String)
    poliza_apoderado = db.Column(db.String)
    fecha_poliza_apoderado = db.Column(db.String)
    cargo = db.Column(db.String)
    cargo_arrendataria = db.Column(db.String)
    alcaldia_firma = db.Column(db.String)
    obligado_solidario = db.Column(db.String)
    RFC_obligado = db.Column(db.String)
    regimen_social = db.Column(db.String)
    nacionalidad_obligado = db.Column(db.String)
    ciudad_obligado = db.Column(db.String)
    curp = db.Column(db.String)
    ocupacion = db.Column(db.String)
    telefono_obligado = db.Column(db.String)
    email_obligado = db.Column(db.String)
    domicilio_obligado = db.Column(db.String)
    estado_civil = db.Column(db.String)
    ciudad_firma = db.Column(db.String)

    def __repr__(self):
        return self.legal_ap

class legal_ap_a(Base):
    __tablename__ = 'legal_ap_a'
    #Datos técnicos del cliente
    id = db.Column(db.Integer, primary_key=True)
    dias = db.Column(db.Float)
    tasa_ordinaria = db.Column(db.Float)
    yrs = db.Column(db.Float)
    principal = db.Column(db.Float)
    tasa_comision = db.Column(db.Float)
    residual = db.Column(db.Float)
    Accesorios = db.Column(db.Float)
    Enganche = db.Column(db.Float)

    Rentas_ptg = db.Column(db.Float)
    startdate = db.Column(db.DateTime)
    # Información del Anexo a partir de aquí
    numero_contrato = db.Column(db.String)
    numero_anexo = db.Column(db.String)
    dia_firma = db.Column(db.String)
    mes_firma = db.Column(db.String)
    año_firma = db.Column(db.String)
    arrendadora = db.Column(db.String)
    denominacion = db.Column(db.String)
    bien1factura = db.Column(db.String)
    bien1_descripcion = db.Column(db.String)
    bien1_accesorios = db.Column(db.String)
    bien_observaciones = db.Column(db.String)
    bien1_precio = db.Column(db.String)
    bien1_cantidad = db.Column(db.String)
    bien2_factura = db.Column(db.String)
    bien2_descripcion = db.Column(db.String)
    bien2_accesorios = db.Column(db.String)
    bien2_observacion = db.Column(db.String)
    bien2_precio = db.Column(db.String)
    bien2_cantidad = db.Column(db.String)
    moneda = db.Column(db.String)
    gastos_contratacion = db.Column(db.String)
    comision_remercadeo = db.Column(db.String)
    uso_autorizado = db.Column(db.String)
    ubicacion = db.Column(db.String)
    limite_uso = db.Column(db.String)
    costo_limite = db.Column(db.String)
    proveedor = db.Column(db.String)
    lugar_devolucion = db.Column(db.String)
    banco = db.Column(db.String)
    CLABE = db.Column(db.String)
    cuenta = db.Column(db.String)
    aseguradora = db.Column(db.String)
    correo = db.Column(db.String)
    apariencia = db.Column(db.String)
    condiciones_generales = db.Column(db.String)
    chasis = db.Column(db.String)
    componentes = db.Column(db.String)
    motor = db.Column(db.String)
    llantas = db.Column(db.String)
    frenos = db.Column(db.String)
    signos = db.Column(db.String)
    uso = db.Column(db.String)
    baterias = db.Column(db.String)
    otros = db.Column(db.String)
    testigo = db.Column(db.String)
    renta_global_l = db.Column(db.String)
    domicilio_arrendadora = db.Column(db.String)
    tasa_moratoria_l = db.Column(db.String)
    apoderado = db.Column(db.String)
    apoderado_arrendataria = db.Column(db.String)

    def __repr__(self):
        return self.legal_ap_a

Base.metadata.create_all(engine)

def create_app():
    app = Flask(__name__) # creates the Flask instance, __name__ is the name of the current Python module
    #CORS(app)
    #Bootstrap(app)
    #datepicker(app)
    app.config['SECRET_KEY'] = 'secret-key-goes-here' # it is used by Flask and extensions to keep data safe
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #it is the path where the SQLite database file will be saved


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # deactivate Flask-SQLAlchemy track modifications
    db.init_app(app) # Initialiaze sqlite database


    # The login manager contains the code that lets your application and Flask-Login work together
    login_manager = LoginManager() # Create a Login Manager instance
    login_manager.login_view = 'auth.login' # define the redirection path when login required and we attempt to access without being logged in
    login_manager.init_app(app) # configure it for login

    @login_manager.user_loader
    def load_user(user_id): #reload user object from the user ID stored in the session
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    # blueprint for auth routes in our app
    # blueprint allow you to orgnize your flask app
    from Scala.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # blueprint for non-auth parts of app
    from Scala.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    #blueprint for index creation and reports
    from Scala.cotizador import cotizador_bp
    app.register_blueprint(cotizador_bp)

    from Scala.legal import legal_bp
    app.register_blueprint(legal_bp)

    


    return app
