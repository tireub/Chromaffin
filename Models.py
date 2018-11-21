from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from Base import Base


class Cell(Base):
    __tablename__ = 'cell'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    date = Column(Date)
    stimulation_time = Column(Integer)
    stimulation_type_id = Column(Integer, ForeignKey("stimulation_type.id"))
    stimulation_type = relationship("StimulationType")
    vesicles = relationship("Vesicle", back_populates="cell")
    membranes = relationship("MembranePoint", back_populates="cell")

    def __init__(self, name, date):
        self.name = name
        self.date = date


class StimulationType(Base):
    __tablename__ = "stimulation_type"

    id = Column(Integer, primary_key=True)
    chemical = Column(String(100))

    def __init__(self, chemical):
        self.chemical = chemical


class MembranePoint(Base):
    __tablename__ = "membrane_point"

    id = Column(Integer, primary_key=True)
    cell_id = Column(Integer, ForeignKey("cell.id"))
    cell = relationship("Cell", back_populates="membranes")
    x = Column(DECIMAL(6,4))
    y = Column(DECIMAL(6,4))

    def __init__(self, cell_id, x, y):
        self.cell_id = cell_id
        self.x = x
        self.y = y


class Vesicle(Base):
    __tablename__ = "vesicle"

    id = Column(Integer, primary_key=True)
    track_duration = Column(Integer)
    cell_id = Column(Integer, ForeignKey("cell.id"))
    cell = relationship("Cell", back_populates="vesicles")
    behaviour = relationship("VesicleBehaviour", back_populates="vesicle")
    positions = relationship("Position", back_populates="vesicle")

    def __init__(self, duration, cell):
        self.track_duration = duration
        self.cell = cell


class BehaviourType(Base):
    __tablename__ = "behaviour_type"

    id = Column(Integer, primary_key=True)
    type = Column(String(20))

    def __init__(self, type):
        self.type = type


class VesicleBehaviour(Base):
    __tablename__ = "vesicle_behaviour"

    vesicle_id = Column(Integer, ForeignKey("vesicle.id"), primary_key=True)
    vesicle = relationship("Vesicle", back_populates="behaviour")
    time_status = Column(Integer, primary_key=True)
    behaviour_type_id = Column(Integer, ForeignKey("behaviour_type.id"))
    behaviour_type = relationship("BehaviourType")

    def __init__(self, vesicle, time):
        self.vesicle = vesicle
        self.time_status = time


class MSD(Base):
    __tablename__ = "msd"

    vesicle_id = Column(Integer, ForeignKey("vesicle.id"), primary_key=True)
    vesicle = relationship("Vesicle")
    deltat = Column(Integer, primary_key=True)
    before_after_stimu = Column(Integer, primary_key=True)
    value = Column(DECIMAL(8,6))

    def __init__(self, vesicle, deltat, value, beforeafter):
        self.vesicle = vesicle
        self.before_after_stimu = beforeafter
        self.deltat = deltat
        self.value = value


class Position(Base):
    __tablename__ = "position"

    id = Column(Integer, primary_key=True)
    x = Column(DECIMAL(6,4))
    y = Column(DECIMAL(6,4))
    z = Column(DECIMAL(6,4))
    t = Column(Integer)
    vesicle_id = Column(Integer, ForeignKey("vesicle.id"))
    vesicle = relationship("Vesicle", back_populates="positions")
    membrane_point_id = Column(Integer, ForeignKey("membrane_point.id"))
    membrane_point = relationship("MembranePoint")
    distance = Column(DECIMAL(6,4))

    def __init__(self, vesicle, x, y, z, t):
        self.vesicle = vesicle
        self.x = x
        self.y = y
        self.z = z
        self.t = t


