from Models import Vesicle, Position, MembranePoint, Cell
import numpy as np
from decimal import Decimal


# Calculate the closest membrane point and the distance
# for each of the positions of concerned vesicle
def distanceFromMembrane(session, vesicle):
    # Retrieve parent cell from vesicle
    associated_cell = session.query(Cell).filter(Cell.id == vesicle.cell_id).first()
    # Retrieve membrane points for that cell
    membranePoints = session.query(MembranePoint).filter(MembranePoint.cell == associated_cell).all()

    for position in vesicle.positions:
        a = (float(position.x), float(position.y))

            #a = np.array(position.x, position.y)
        t = []
        for point in membranePoints:
            b = np.array((float(point.x), float(point.y)))
            dist = np.linalg.norm(a-b)
            t.append([dist, point.id])

        print(min(t))

        position.distance = Decimal(min(t)[0])
        position.membrane_point_id = min(t)[1]


def massDistanceFromMembrane(session, cell):
    # Extract membrane points for related cell
    membranePoints = session.query(MembranePoint).filter(
        MembranePoint.cell == cell).all()
    # Extract all vesicles related to the cell
    vesicles = session.query(Vesicle).filter(Vesicle.cell == cell).all()

    for vesicle in vesicles:
        print(vesicle.id)
        # For every position of the vesicle
        for position in vesicle.positions:
            a = (float(position.x), float(position.y))

            t = []
            for point in membranePoints:
                b = np.array((float(point.x), float(point.y)))
                # Calculate distance from the membrane points
                dist = np.linalg.norm(a - b)
                t.append([dist, point.id])

            # Get only the closest membrane point and save the infos
            position.distance = Decimal(min(t)[0])
            position.membrane_point_id = min(t)[1]


