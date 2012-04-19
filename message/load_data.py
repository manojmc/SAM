csv_filepathname="/home/manoj/test"
# Full path to your django project directory
your_djangoproject_home="/home/manoj/1/sam/"

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from message.models import ZipCode
import csv
class data:
	dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
	for row in dataReader:
		 # Ignore the header row, import everything else
		zipcode = ZipCode()
		zipcode.zipcode = row[0]
		zipcode.city = row[1]
		zipcode.statecode = row[2]
		zipcode.save()
