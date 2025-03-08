from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

# Define naming conventions for foreign keys
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

# Create the base class for declarative models
Base = declarative_base(metadata=metadata)

# Define the Actor model
class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    phone = Column(String())

    # Relationship to Audition (one actor can have many auditions)
    auditions = relationship('Audition', back_populates='actor')

    def __repr__(self):
        return f"Actor(id={self.id}, name='{self.name}', phone='{self.phone}')"

# Define the Role model
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    # Relationship to Audition (one role can have many auditions)
    auditions = relationship("Audition", back_populates="role")

    def __repr__(self):
        return f"Role(id={self.id}, character_name='{self.character_name}')"

# Define the Audition model
class Audition(Base):
    __tablename__ = 'auditions'
    id = Column(Integer(), primary_key=True)
    actor_id = Column(Integer(), ForeignKey('actors.id'))  # Foreign key to Actor
    location = Column(String())
    phone = Column(String())
    hired = Column(Boolean, default=False)

    role_id = Column(Integer(), ForeignKey('roles.id'))  # Foreign key to Role

    # Relationships
    role = relationship("Role", back_populates="auditions")
    actor = relationship("Actor", back_populates="auditions")

    def __repr__(self):
        return f"Audition(id={self.id}, location='{self.location}', hired={self.hired}, actor_id={self.actor_id}, role_id={self.role_id})"

# Database setup
engine = create_engine('sqlite:///theater.db')  # SQLite database file
Base.metadata.create_all(engine)  # Create tables
Session = sessionmaker(bind=engine)
session = Session()