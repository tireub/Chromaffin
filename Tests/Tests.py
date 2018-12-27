from unittest import *


"""
Tests of functionalities.

GUI behaviour avoided.

Only calculation functions and display elements are tested.

GUI behaviour to be tested manually.
"""

# Test Imports
    # Create file (or make sure some exists somewhere in a folder (better idea))
    # Check that cell has been added within the db (nbr before = nbrafter-1)
    # Check that vesicles have been added





# Setup a cell
# Setup a few vesicle (cordinates array given to get known value for MSD

# Test membrane import
# Bogus file, then test if membrane has been incremented, and that last element is linked to poper cell


# MSD Calc tests

    # Test that the MSD is properly calculated for a given vesicle (dt=max, dt=1, dt=0)
    # Test the MSD number of entried within the database has been changed



# Distance from membrane tests
    # Generate a memebrane point
    # Test for a vesicle that the distance and membrane point have been added


# Distance at stimu time
    # Test that it returns a value


# Behaviourstorting test
    # Test that behaviour is added
    # Test that it's right for a given cell


# Behaviourchange
    # Create bogus ves with behaviourbef = free, behavaft = directed
    # Test that it returns (100, 0, 0, 0, 100, 0, 1, 1)

    # Changevsoriginal
    # Test that freebefore returns (0, 1, 0, 1, 1)
    # Test cagedbefore returns (0, 0, 0, 0, 1)

