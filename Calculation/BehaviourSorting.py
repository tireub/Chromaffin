from Models import MSD, BehaviourType, Vesicle, VesicleBehaviour
import numpy as np
import matplotlib.pyplot as plt


# For the desired vesicle
def sorting(session, vesicle):

    # For MSD before stimulation
    # Import vesicle MSD values before stimulation
    msdvalues = session.query(MSD).filter(MSD.vesicle == vesicle,
                                          MSD.before_after_stimu == 1).\
        order_by(MSD.deltat).all()

    if len(msdvalues) >= 5:
        behav = VesicleBehaviour(vesicle, 1)

        # Realise fit with a 2degrees polynomial curve
        x = [float(item.deltat) for item in msdvalues]
        y = [float(item.value) for item in msdvalues]
        fit = np.polyfit(x, y, 2)

        # print(fit)

        # f = np.poly1d(fit)
        # x_new = np.linspace(x[0], x[-1], 50)
        # y_new = f(x_new)
        # plt.plot(x, y, 'o', x_new, y_new)
        # plt.show()

        # Extract plynomial coefficients
        c2 = fit[0]  # x² coeff
        c1 = fit[1]  # x coeff

        # Determine kind of movement
        if c2/c1 <= -0.025 or max(y) <= 0.1:    # caged movement
            behav.behaviour_type_id = 3
        else:
            if c2/c1 >= 0.02 or max(y) >= 1.3:  # directed movement
                behav.behaviour_type_id = 2
            else:                               # free movement
                behav.behaviour_type_id = 1

        session.add(behav)  # Save info

    msdvalues = session.query(MSD).filter(MSD.vesicle == vesicle,
                                          MSD.before_after_stimu == 2).\
        order_by(MSD.deltat).all()

    if len(msdvalues) >= 5:
        behav = VesicleBehaviour(vesicle, 2)

        # Realise fit with a 2degrees polynomial curve
        x = [float(item.deltat) for item in msdvalues]
        y = [float(item.value) for item in msdvalues]
        fit = np.polyfit(x, y, 2)

        # Extract plynomial coefficients
        c2 = fit[0]  # x² coeff
        c1 = fit[1]  # x coeff

        # Determine kind of movement
        if c2 / c1 <= -0.025 or max(y) <= 0.1:    # caged movement
            behav.behaviour_type_id = 3
        else:
            if c2 / c1 >= 0.02 or max(y) >= 1.3:  # directed movement
                behav.behaviour_type_id = 2
            else:                                 # free movement
                behav.behaviour_type_id = 1

            session.add(behav)  # Save info




def cellSorting(session, cell):
    vesicles = session.query(Vesicle).filter(Vesicle.cell == cell).all()

    for vesicle in vesicles:
        sorting(session, vesicle)

    session.commit()