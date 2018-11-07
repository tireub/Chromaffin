from Models import Cell, StimulationType, MembranePoint, Vesicle, \
    BehaviourType, VesicleBehaviour, MSD, Position
from datetime import date
from Imports import cell_import, open_workbook
from Base import Session, engine, Base


Base.metadata.create_all(engine)

session = Session()

wb = open_workbook(r'F:\UQ\Data\Confocal experiments\20091008 Chroma '
                   r'Nicotine\Data experiment 1\experiment 1 stimu 62.xls')

cell_import(session, "test1", date(2009,10,8), 62, "Nicotine")

positions = session.query(Position).all()


session.commit()

session.close()