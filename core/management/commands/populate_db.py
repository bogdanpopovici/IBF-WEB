from django.core.management.base import BaseCommand
from core.models import CustomUser, Item, Media
import sys, urllib2
from urlparse import urlparse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management import call_command
from StringIO import StringIO 
 


SQL_STATEMENT = 'BEGIN;DROP TABLE `core_media`;DROP TABLE `core_item`;DROP TABLE `core_userprofile`;ALTER TABLE `core_customuser_user_permissions` DROP FOREIGN KEY `customuser_id_refs_id_b678a283`;ALTER TABLE `core_customuser_groups` DROP FOREIGN KEY `customuser_id_refs_id_4cc940bd`;DROP TABLE `core_customuser`;DROP TABLE `core_customuser_user_permissions`;DROP TABLE `core_customuser_groups`;COMMIT;'

class Command(BaseCommand):
	args = '<foo bar ...>'
	help = 'command to be used for populating the database with mock data'

	def _create_items(self):

		#try to drop all the tables before migrating
		'''content = StringIO()
		call_command('sqlclear', 'core', stdout=content)
		content.seek(0)
		SQL_STATEMENT = content.read()

		inputS = StringIO()
		inputS.write(SQL_STATEMENT)

		call_command('dbshell', NAME='ibf-web', USER='user', PASSWORD='password',stdin=inputS)'''

		call_command('migrate', 'auth')
		sys.stdout.write("\n==========Auth App Migrated===========\n")

		call_command('migrate')
		sys.stdout.write("\n==========Other Apps Migrated===========\n")

		call_command('syncdb', interactive=True)

		Item.objects.all().delete()
		
		user = CustomUser.objects.all()[:1].get()
		tphone = Item()
		tphone.unique_id = '123456789'
		tphone.tags = "Black Samsung Galaxy S6 34GB"
		tphone.description = 'Black Samsung Galaxy S6 found in Stile'
		tphone.location = "southampton"
		tphone.category = "Electronics"
		tphone.date_field = "2015-09-15"
		tphone.time_field = "14:33::22"
		tphone.found_by_user = user
		tphone.save()

		tbag = Item()
		tbag.unique_id = '-'
		tbag.description = 'Green bag found on the poll edge at "Summer Time"'
		tbag.tags = "Beg Green"
		tbag.location = "london"
		tbag.category = "Bags"
		tbag.date_field = "2015-08-20"
		tbag.time_field = "10:33::22"
		tbag.found_by_user = user
		tbag.save()

		photo = Media()
		photo.of_item = tbag
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'http://www.suggestcamera.com/wp-content/uploads/2015/08/81K-jtyW82L._SL1500_.jpg')
		photo.save()

		tbag = Item()
		tbag.description = 'Green bag found on the poll edge at "Summer Time"'
		tbag.tags = "Beg"
		tbag.location = "london"
		tbag.category = "Bags"
		tbag.date_field = "2015-09-12"
		tbag.time_field = "10:33::22"
		tbag.found_by_user = user
		tbag.save()

		photo = Media()
		photo.of_item = tphone
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'http://i.dailymail.co.uk/i/pix/2013/11/13/article-2505060-0B22502B000005DC-342_634x422.jpg')
		photo.save()

		tLeptop = Item()
		tLeptop.unique_id = '098765432'
		tLeptop.description = '15 inch Dell found in Winchester"'
		tLeptop.tags = "Leptop Dell Black"
		tLeptop.location = "london"
		tLeptop.category = "Electronics"
		tLeptop.date_field = "2015-09-18"
		tLeptop.time_field = "10:33::22"
		tLeptop.found_by_user = user
		tLeptop.save()

		sys.stdout.write("\n==========Database Re-populated===========\n")

		call_command('rebuild_index')

	def handle(self, *args, **options):
		while True:
		    sys.stdout.write("This command will erase all the data from the db and re-populate it\n"+
		    				 "Do you want to continue (y/n):")
		    choice = raw_input().lower()
		    if choice == 'y':
		        self._create_items()
		        return
		    elif choice == 'n':
		    	return
		    else:
		        sys.stdout.write("Please respond with 'y' or 'n'.\n")

def save_url_to_image(media_obj, url):

	name = urlparse(url).path.split('/')[-1]
	img_temp = NamedTemporaryFile()
	img_temp.write(urllib2.urlopen(url).read())
	img_temp.flush()
	media_obj.data.save(name, File(img_temp))