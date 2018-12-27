from Models import Vesicle, VesicleBehaviour


def filering(session, filters, current_cell):
    fb = []
    db = []
    cb = []
    fa = []
    da = []
    ca = []

    if filters[0]:
        fb = session.query(Vesicle).filter(
            Vesicle.cell == current_cell).join(Vesicle.behaviour).filter(
            VesicleBehaviour.time_status == 1,
            VesicleBehaviour.behaviour_type_id == 1).all()

    if filters[1]:
        db = session.query(Vesicle).filter(
            Vesicle.cell == current_cell).join(Vesicle.behaviour).filter(
            VesicleBehaviour.time_status == 1,
            VesicleBehaviour.behaviour_type_id == 2).all()

    if filters[2]:
        cb = session.query(Vesicle).filter(
            Vesicle.cell == current_cell).join(Vesicle.behaviour).filter(
            VesicleBehaviour.time_status == 1,
            VesicleBehaviour.behaviour_type_id == 3).all()

    if filters[3]:
        fa = session.query(Vesicle).filter(
            Vesicle.cell == current_cell).join(Vesicle.behaviour).filter(
            VesicleBehaviour.time_status == 2,
            VesicleBehaviour.behaviour_type_id == 1).all()

    if filters[4]:
        da = session.query(Vesicle).filter(
            Vesicle.cell == current_cell).join(Vesicle.behaviour).filter(
            VesicleBehaviour.time_status == 2,
            VesicleBehaviour.behaviour_type_id == 1).all()

    if filters[5]:
        ca = session.query(Vesicle).filter(
            Vesicle.cell == current_cell).join(Vesicle.behaviour).filter(
            VesicleBehaviour.time_status == 2,
            VesicleBehaviour.behaviour_type_id == 1).all()

    vesicles = list(set(fb) | set(db) | set(cb) | set(fa) | set(da) | set(ca))

    return (vesicles)
