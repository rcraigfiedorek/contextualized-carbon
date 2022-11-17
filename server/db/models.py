from db.instance import db


class CompanyModel(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    emissions = db.relationship('EmissionsModel', lazy=False)


class EmissionsModel(db.Model):
    __tablename__ = 'emissions'

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    facility_count = db.Column(db.Integer, nullable=False)
    all_facility_emissions = db.Column(db.Float, nullable=False)
    fully_owned_emissions = db.Column(db.Float, nullable=False)
