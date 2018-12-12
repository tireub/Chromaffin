from Models import Cell, Vesicle, StimulationType, VesicleBehaviour


def behavchange(session, stimu):
    stim = session.query(StimulationType).filter(
        StimulationType.chemical == stimu).first()
    # Collecting all cells with this kind of stimulation
    cells = session.query(Cell).filter(Cell.stimulation_type == stim).all()
    ves = []

    if cells:
        # Adding all the vesicles
        for c in cells:
            ves = ves + c.vesicles

        freebefves = session.query(Vesicle).join(Vesicle.cell).\
            join(Vesicle.behaviour)\
            .filter(Cell.stimulation_type == stim,
                    VesicleBehaviour.behaviour_type_id == 1,
                    VesicleBehaviour.time_status == 1).all()
        dirbefves = session.query(Vesicle).join(Vesicle.cell). \
            join(Vesicle.behaviour) \
            .filter(Cell.stimulation_type == stim,
                    VesicleBehaviour.behaviour_type_id == 2,
                    VesicleBehaviour.time_status == 1).all()
        cagedbefves = session.query(Vesicle).join(Vesicle.cell). \
            join(Vesicle.behaviour) \
            .filter(Cell.stimulation_type == stim,
                    VesicleBehaviour.behaviour_type_id == 3,
                    VesicleBehaviour.time_status == 1).all()
        freeaftves = session.query(Vesicle).join(Vesicle.cell). \
            join(Vesicle.behaviour) \
            .filter(Cell.stimulation_type == stim,
                    VesicleBehaviour.behaviour_type_id == 1,
                    VesicleBehaviour.time_status == 2).all()
        diraftves = session.query(Vesicle).join(Vesicle.cell). \
            join(Vesicle.behaviour) \
            .filter(Cell.stimulation_type == stim,
                    VesicleBehaviour.behaviour_type_id == 2,
                    VesicleBehaviour.time_status == 2).all()
        cagedaftves = session.query(Vesicle).join(Vesicle.cell). \
            join(Vesicle.behaviour) \
            .filter(Cell.stimulation_type == stim,
                    VesicleBehaviour.behaviour_type_id == 3,
                    VesicleBehaviour.time_status == 2).all()

        sumbef = len(freebefves) + len(dirbefves) + len(cagedbefves)
        freebefvespercent = len(freebefves) / sumbef * 100
        dirbefvespercent = len(dirbefves) / sumbef * 100
        cagedbefvespercent = len(cagedbefves) / sumbef * 100
        sumaft = len(freeaftves) + len(diraftves) + len(cagedaftves)
        freeaftvespercent = len(freeaftves) / sumaft * 100
        diraftvespercent = len(diraftves) / sumaft * 100
        cagedaftvespercent = len(cagedaftves) / sumaft * 100

    else:
        freebefvespercent = 0
        dirbefvespercent = 0
        cagedbefvespercent = 0
        freeaftvespercent = 0
        diraftvespercent = 0
        cagedaftvespercent = 0

    return(freebefvespercent, dirbefvespercent, cagedbefvespercent,
           freeaftvespercent, diraftvespercent, cagedaftvespercent)
