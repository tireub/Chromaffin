from Models import Cell, StimulationType, MembranePoint, Vesicle, \
    BehaviourType, VesicleBehaviour, MSD, Position
from datetime import date
from Imports.Imports import cell_import, edges_import
from Base import Session, engine, Base
from Calculation.MSDCalc import MSDCalc, CellMSDs
from Calculation.BehaviourSorting import sorting, cellSorting
from Calculation.DistanceFromMembrane import distanceFromMembrane, massDistanceFromMembrane


Base.metadata.create_all(engine)

session = Session()

# cell = session.query(Cell).filter(Cell.id == 1).first()

# massDistanceFromMembrane(session, cell)

# session.commit()

session.close()