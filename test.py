from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import enum
app = Flask(__name__) #creo l'app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #collego il database all'app Flask


@app.route('/')
def home():
  return "Benvenuto nell'applicazione!"

#devo creare il database
class TipoRichiesta(enum.Enum):
  installazione = 'installazione'
  configurazione = 'configurazione'
  aggiornamento = 'aggiornamento' 
class Ticket(db.Model):
  id = db.Column(db.Integer, primary_key=True) #campo chiave primaria
  tipo = db.Column(db.String(50), nullable=False) #tipo di ticket
  email = db.Column(db.String(120), nullable=False) #per tutti e tre dico che non è mai vuoto
  descrizione = db.Column(db.String(500), nullable=False)
  stato = db.Column(db.String(50), default='In attesa') #stato del ticket
  data_creazione = db.Column(db.DateTime, default=db.func.now())
  operatore_id = db.Column(db.Integer, db.ForeignKey('operatore.id'))#chiave ext


#la stessa cosa per l'operatore
class Operatore(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), nullable=False)
  richieste_gestite = db.Column(db.String(200), nullable=False) 
  fascia_oraria = db.Column(db.String(20), nullable=False)
  tickets = db.relationship('Ticket', backref='operatore', lazy = True)
#assegnazione ticket


def assegna_operatore(ticket):
  ora_att = datetime.now().strftime("%H:%M")
  #trovo operatore disponibile nella fascia oraria
  operatori = Operatore.query.all()
  for operatore in operatori:
    fasce = operatore.fascia_oraria.split('-')
    if len(fasce) == 2 and fasce [0] <= ora_att <= fasce [1]:
      ticket.operatore_id = operatore.id
      db.session.commit()
      return"Ticket assegnato a {operatore.nome}"
  else:
      return "Nessun operatore disponibile oggi"