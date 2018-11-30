from xlrd import open_workbook

# from Session import session
from Models import Cell, Vesicle, Position, StimulationType, MembranePoint


# Function to import data from xls file
# Entry parameters : file location, date, stimulation time, stimulation type
def cell_import(session, file, name, date, stimulation_time, stimulation_type):
    wb = open_workbook(file)
    stimu = session.query(StimulationType)\
        .filter(StimulationType.chemical == stimulation_type)

    newcell = Cell(name, date)
    newcell.stimulation_time = stimulation_time
    newcell.stimulation_type = stimu[0]

    # Fill cell values
    session.add(newcell)

# Get number of vesicles
    vesnbr = int(wb.sheet_by_name('Overall').cell(1, 1).value)

    positionsSheet = wb.sheet_by_name('Position')

    k = 1
# For each vesicle
    for i in range(vesnbr):
        # Get track number of points
        nbrOfPts = int(wb.sheet_by_name('Track Number of Points').
                       cell(i+1, 0).value)

        # Fill vesicle values
        ves = Vesicle(nbrOfPts, newcell)
        session.add(ves)

    # For each point
        for point in range(nbrOfPts):
            # Extract x,y,z value
            x = positionsSheet.cell(k, 0).value
            y = positionsSheet.cell(k, 1).value
            z = positionsSheet.cell(k, 2).value
            t = positionsSheet.cell(k, 6).value
            pos = Position(ves, x, y, z, t)

            k += 1

            # Fill position values
            session.add(pos)

    session.commit()


# Function import membrane points from a txt file
def edges_import(session, file, cell):
    # Open requested text file
    with open(file, "r") as edgesFile:
        # Read through the lines
        for line in edgesFile:
            # Remove potential last line error
            if line.split():
                # Extract x and y values
                x = (line.split()[0])
                y = (line.split()[1])

                # Initiate new membrane point
                point = MembranePoint(cell.id, x, y)

                # Fille values in the database
                session.add(point)
