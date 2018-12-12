from Models import Cell, Vesicle, StimulationType,\
    VesicleBehaviour, BehaviourType


def changevsoriginal(session, stimu, original):
    stim = session.query(StimulationType).filter(
        StimulationType.chemical == stimu).first()
    # Collecting all cells with this kind of stimulation
    cells = session.query(Cell).filter(Cell.stimulation_type == stim).all()
    behav = session.query(BehaviourType).filter(
        BehaviourType.type == original).first()
    newfree = []
    newdir = []
    newcaged = []
    calc = 0

    if cells:

        oribef = session.query(Vesicle.id).join(Vesicle.cell).\
            join(Vesicle.behaviour) \
            .filter(Cell.stimulation_type == stim,
                    VesicleBehaviour.behaviour_type == behav,
                    VesicleBehaviour.time_status == 1).all()

        freeaft = session.query(Vesicle.id).join(Vesicle.cell).\
            join(Vesicle.behaviour) \
            .filter(Cell.stimulation_type == stim,
                    VesicleBehaviour.behaviour_type_id == 1,
                    VesicleBehaviour.time_status == 2).all()
        diraft = session.query(Vesicle.id).join(Vesicle.cell). \
            join(Vesicle.behaviour) \
            .filter(Cell.stimulation_type == stim,
                    VesicleBehaviour.behaviour_type_id == 2,
                    VesicleBehaviour.time_status == 2).all()
        cagedaft = session.query(Vesicle.id).join(Vesicle.cell). \
            join(Vesicle.behaviour) \
            .filter(Cell.stimulation_type == stim,
                    VesicleBehaviour.behaviour_type_id == 3,
                    VesicleBehaviour.time_status == 2).all()

        for c in oribef:
            if c in freeaft:
                newfree.append(c)
                calc = 1
        for c in oribef:
            if c in diraft:
                newdir.append(c)
                calc = 1
        for c in oribef:
            if c in cagedaft:
                newcaged.append(c)
                calc = 1

    return (newfree, newdir, newcaged, calc)
