from Models import Cell, Vesicle, Position, MSD
import numpy as np


# For desired vesicle
def MSDCalc(session, vesicle):
    x = []
    y = []
    z = []
    t = []

# Import positions
    positions = session.query(Position).\
        filter(Position.vesicle == vesicle).all()
    for position in positions:
        x.append(position.x)
        y.append(position.y)
        z.append(position.z)
        t.append(position.t)

    # Segregate before/after
    cell = session.query(Cell).join(Vesicle, Cell.vesicles).\
        filter(Vesicle.id == vesicle.id).one()
    stimulationtime = cell.stimulation_time

    # Before stimulation
    if t[0] < stimulationtime:
        # if after stimulation
        if t[-1] > stimulationtime:
            # Get number of points before stimulation
            sizebefore = stimulationtime - t[0]

            num = min(sizebefore, 20)

            msd = []
            # Calculate MSD for deltat up to nbrofpts or 20
            for deltaT in range(num):

                sqdisp = []
                for elem in range(sizebefore - deltaT):
                    sqdisp.append((x[elem+deltaT] - x[elem])**2 +
                                  (y[elem+deltaT] - y[elem])**2 +
                                  (z[elem+deltaT] - z[elem])**2)

                # Fill values
                meansquare = MSD(vesicle, deltaT, np.mean(sqdisp), 1)
                session.add(meansquare)

            # Get number of points after stimulation
            sizeafter = t[-1] - stimulationtime

            num = min(sizeafter, 20)
            msd = []
            # Calculate MSD for deltat up to nbrofpts or 20
            for deltaT in range(num):

                sqdisp = []
                for elem in range(sizebefore+1,
                                  sizebefore+1+sizeafter-deltaT):

                    sqdisp.append((x[elem+deltaT] - x[elem])**2 +
                                  (y[elem+deltaT] - y[elem])**2 +
                                  (z[elem+deltaT] - z[elem])**2)

                # Fill values
                meansquare = MSD(vesicle, deltaT, np.mean(sqdisp), 2)
                session.add(meansquare)

        # If vesicle is only tracked before stimulation
        else:
            num = min(len(t), 30)
            msd = []
            for deltaT in range(num):
                sqdisp = []
                for elem in range(len(t) - deltaT):
                    sqdisp.append((x[elem + deltaT] - x[elem])**2 +
                                  (y[elem + deltaT] - y[elem])**2 +
                                  (z[elem + deltaT] - z[elem])**2)
                # Fill values
                meansquare = MSD(vesicle, deltaT, np.mean(sqdisp), 1)
                session.add(meansquare)

    # if the vesicle is only tracked after stimulation
    else:
        num = min(len(t), 30)
        msd = []
        for deltaT in range(num - 1):
            sqdisp = []
            for elem in range(len(t) - deltaT):
                sqdisp.append((x[elem + deltaT] - x[elem])**2 +
                              (y[elem + deltaT] - y[elem])**2 +
                              (z[elem + deltaT] - z[elem])**2)

            # Fill values
            meansquare = MSD(vesicle, deltaT, np.mean(sqdisp), 2)
            session.add(meansquare)


def CellMSDs(session, cell):
    vesicles = session.query(Vesicle).filter(Vesicle.cell == cell).all()

    for vesicle in vesicles:
        MSDCalc(session, vesicle)
