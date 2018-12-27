from Base import Session, engine, Base



Base.metadata.create_all(engine)

session = Session()

# cell = session.query(Cell).filter(Cell.id == 1).first()

# massDistanceFromMembrane(session, cell)

# session.commit()

session.close()