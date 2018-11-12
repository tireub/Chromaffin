from Models import Cell, StimulationType, MembranePoint, Vesicle, \
    BehaviourType, VesicleBehaviour, MSD, Position
from datetime import date
from Imports import cell_import, open_workbook
from Base import Session, engine, Base
from MSDCalc import MSDCalc


Base.metadata.create_all(engine)

session = Session()


vesicle = session.query(Vesicle).filter(Vesicle.id == 1)[0]

MSDCalc(session, vesicle)

session.commit()

session.close()