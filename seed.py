#create a seed that has all cuisines already inside of database.
#list of days as well maybe for the meal plan

from models import Cuisine, connect_db, db
from app import app

app.app_context().push()


db.drop_all()
db.create_all()

#Cuisine.query.delete()

c1 = Cuisine(name='African')
c2 = Cuisine(name='Asian')
c3 = Cuisine(name='American')
c4 = Cuisine(name='British')
c5 = Cuisine(name='Cajun')
c6 = Cuisine(name='Caribbean')
c7 = Cuisine(name='Chinese')
c8 = Cuisine(name='Eastern European')
c9 = Cuisine(name='European')
c10 = Cuisine(name='French')
c11 = Cuisine(name='German')
c12 = Cuisine(name='Greek')
c13 = Cuisine(name='Indian')
c14 = Cuisine(name='Irish')
c15 = Cuisine(name='Italian')
c16 = Cuisine(name='Japanese')
c17 = Cuisine(name='Jewish')
c18 = Cuisine(name='Korean')
c19 = Cuisine(name='Latin American')
c20 = Cuisine(name='Mediterranean')
c21 = Cuisine(name='Mexican')
c22 = Cuisine(name='Middle Eastern')
c23 = Cuisine(name='Nordic')
c24 = Cuisine(name='Southern')
c25 = Cuisine(name='Spanish')
c26 = Cuisine(name='Thai')
c27 = Cuisine(name='Vietnamese')

db.session.add_all([c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27])
db.session.commit()
