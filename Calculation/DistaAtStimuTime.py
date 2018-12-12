from Models import Vesicle, Position


def dist_at_stimu(session, vesiclesIDs):
    distances = []

    for id in vesiclesIDs:

        ves = session.query(Vesicle).filter(Vesicle.id == id[0]).first()
        stimutime = ves.cell.stimulation_time

        pos = session.query(Position).filter(Position.vesicle == ves,
                                             Position.t == stimutime).first()
        dist = pos.distance

        distances.append(float(dist))

    return(distances)
