from Models import Cell, StimulationType, MembranePoint, Vesicle, \
    BehaviourType, VesicleBehaviour, MSD, Position
from datetime import date
from Imports import cell_import, open_workbook
from Base import Session, engine, Base
from MSDCalc import MSDCalc, CellMSDs
from BehaviourSorting import Sorting, CellSorting


Base.metadata.create_all(engine)

session = Session()


cell = session.query(Cell).filter(Cell.id == 1)[0]

CellSorting(session, cell)

session.commit()

session.close()