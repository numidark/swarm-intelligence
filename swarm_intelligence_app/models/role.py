"""
Define the classes for the role API.

"""

from enum import Enum
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.role_member import role_members


class RoleType(Enum):
    """
    Define values for an Role status.

    """
    LEAD_LINK = 'lead_link'
    REP_LINK = 'rep_link'
    FACILITATOR = 'facilitator'
    SECRETARY = 'secretary'
    CIRCLE = 'circle'
    CUSTOM = 'custom'


class Role(db.Model):
    """
    Define a mapping to the database for a role.

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(RoleType), nullable=False)
    parent_circle_id = db.Column(db.Integer, db.ForeignKey('circle.id',
                                                           use_alter=True),
                                 nullable=True)
    circle_id = db.Column(db.Integer, db.ForeignKey('circle.id',
                                                    use_alter=True),
                          nullable=True)

    partners = db.relationship('Partner', secondary=role_members,
                               back_populates='roles')
    roles = db.relationship('Role', secondary=role_members,
                            back_populates='partners')

    def __init__(self, name, purpose, parent_circle_id, circle_id, type):
        """
        Initialize a role.

        """
        self.name = name
        self.type = type
        self.parent_circle_id = parent_circle_id
        self.circle_id = circle_id
        self.purpose = purpose

    def __repr__(self):
        """
        Return a readable representation of a role.

        """
        return '<Role %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of a role.

        """
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'circle_id': self.circle_id,
            'parent_circle_id': self.parent_circle_id,
            'purpose': self.purpose
        }