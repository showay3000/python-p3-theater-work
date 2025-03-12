from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Audition(Base):
    __tablename__ = "auditions"

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(String)  # Changed to String to store phone numbers correctly
    hired = Column(Boolean, default=False) 
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="auditions")

    def call_back(self):
        self.hired = True

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    auditions = relationship("Audition", back_populates="role")

    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    def locations(self):
        return [audition.location for audition in self.auditions]
    
    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else "no actor has been hired for this role."
    
    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else "no understudy has been hired for this role."

# Setup a database engine
engine = create_engine("sqlite:///theater.db")
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

# Create a role and auditions
role = Role(character_name="John Doe")

audition1 = Audition(actor="Mark Vog", location="Kenya", phone="123-456-789", role=role)
audition2 = Audition(actor="Will Smith", location="Kenya", phone="987-654-321", role=role)

# Add and commit to the session
session.add(role)
session.add(audition1)
session.add(audition2)
session.commit()

# Print actors and locations
print(role.actors())  # ['Jane Smith', 'Will Smith']
print(role.locations())  # ['Kenya', 'Kenya']

# Call back the first audition (hire the actor)
audition1.call_back()
session.commit()

# Print lead and understudy
print(role.lead())  # 'Jane Smith'
print(role.understudy())  # 'no understudy has been hired for this role.'

# Close the session
session.close()
