from models.database import db_session
from models.models import FoodDB
from models.database import init_db
from datetime import datetime
from datetime import timedelta


init_db()

now = datetime.now()

d1 = timedelta(weeks=2*4*12)
d2 = timedelta(weeks=1*4*12)
d3 = timedelta(weeks=13)

f1 = FoodDB("ketchup","red, tomato, good",now + d1)
f2 = FoodDB("maple syrup","delicious, canadian",now + d2)
f3 = FoodDB("ribeye","red, juicy, fat",now + d3)

db_session.add(f1)
db_session.add(f2)
db_session.add(f3)
db_session.commit()
