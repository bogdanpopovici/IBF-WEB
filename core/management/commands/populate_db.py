#  --- University of Southampton ---
#  --- Group Design Project in collaboration with 'The Big Consulting' ---
#  --- Copyright 2015 ---

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
		tbag.tags = "Bag Green"
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
		tbag.tags = "Bag"
		tbag.location = "london"
		tbag.category = "Bags"
		tbag.date_field = "2015-09-12"
		tbag.time_field = "10:33::22"
		tbag.found_by_user = user
		tbag.save()

		photo = Media()
		photo.of_item = tbag
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

		tLaptop = Item()
		tLaptop.unique_id = '123456788'
		tLaptop.description = 'Apple MacBook 15" found at Hartley Library'
		tLaptop.tags = "Apple MacBook"
		tLaptop.location = "Southampton"
		tLaptop.category = "Electronics"
		tLaptop.date_field = "2015-11-16"
		tLaptop.time_field = "22:35::22"
		tLaptop.found_by_user = user
		tLaptop.save()

		photo = Media()
		photo.of_item = tLaptop
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'http://static.trustedreviews.com/94/9736c1/5242/15168-crw398s.jpg')
		photo.save()

		tIDCard = Item()
		tIDCard.unique_id = '123459876'
		tIDCard.description = 'Passport found outside Sprinkles'
		tIDCard.tags = "Passport UK EU e-passport"
		tIDCard.location = "Southampton"
		tIDCard.category = "ID/Cards"
		tIDCard.date_field = "2015-07-23"
		tIDCard.time_field = "12:07::22"
		tIDCard.found_by_user = user
		tIDCard.save()

		photo = Media()
		photo.of_item = tIDCard
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'http://i.telegraph.co.uk/multimedia/archive/01595/mp-passport-pa_1595880b.jpg')
		photo.save()

		tBook = Item()
		tBook.unique_id = '121212123'
		tBook.description = 'Dan Brown The Lost Symbol paperback edition'
		tBook.tags = "Dan Brown The Lost Symbol Paperback "
		tBook.location = "Bournemouth"
		tBook.category = "Books"
		tBook.date_field = "2015-09-30"
		tBook.time_field = "17:53:28"
		tBook.found_by_user = user
		tBook.save()

		photo = Media()
		photo.of_item = tBook
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'http://thumbs1.ebaystatic.com/d/l225/m/mIuB9Oannj3xR0YhYCIiEZg.jpg')
		photo.save()

		tScarf = Item()
		tScarf.unique_id = '666777888'
		tScarf.description = 'Grey Scarf with Dark Grey Stripes'
		tScarf.tags = "Scarf Grey Dark Grey Stripes "
		tScarf.location = "Surrey"
		tScarf.category = "Clothes"
		tScarf.date_field = "2015-10-28"
		tScarf.time_field = "13:53:28"
		tScarf.found_by_user = user
		tScarf.save()

		photo = Media()
		photo.of_item = tScarf
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'http://assets3.howtospendit.ft-static.com/images/52/46/d7/5246d742-1619-46b4-83c8-9e9d726203da_three_eighty.png')
		photo.save()

		tNecklace = Item()
		tNecklace.unique_id = '898998989'
		tNecklace.tags = 'Black Leather necklace'
		tNecklace.description = "leather necklace black men unisex"
		tNecklace.location = "Glasgow"
		tNecklace.category = "Accessories"
		tNecklace.date_field = "2015-11-28"
		tNecklace.time_field = "13:27:28"
		tNecklace.found_by_user = user
		tNecklace.save()

		photo = Media()
		photo.of_item = tNecklace
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'http://cdn.notonthehighstreet.com/system/product_images/images/001/615/301/original_mens-leather-necklace.jpg')
		photo.save()

		tHobbit = Item()
		tHobbit.unique_id = '454647489'
		tHobbit.tags = 'J R R Tolkien - The Hobbit Hard Cover'
		tHobbit.description = "tolkien hobbit the hobbit hardcover"
		tHobbit.location = "Eastleigh"
		tHobbit.category = "Books"
		tHobbit.date_field = "2015-10-30"
		tHobbit.time_field = "10:41:28"
		tHobbit.found_by_user = user
		tHobbit.save()

		photo = Media()
		photo.of_item = tHobbit
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'https://i.ytimg.com/vi/X75pnPtqhvE/maxresdefault.jpg')
		photo.save()

		tPlayer = Item()
		tPlayer.unique_id = '145897123'
		tPlayer.tags = 'Sony Walkman MP4 Player Black'
		tPlayer.description = "sony walkman mp4 player mp3 black "
		tPlayer.location = "London"
		tPlayer.category = "Electronics"
		tPlayer.date_field = "2015-10-30"
		tPlayer.time_field = "10:41:28"
		tPlayer.found_by_user = user
		tPlayer.save()

		photo = Media()
		photo.of_item = tPlayer
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'https://i.ytimg.com/vi/PI_nQ3MSSHI/maxresdefault.jpg')
		photo.save()

		tDog = Item()
		tDog.unique_id = '321654987'
		tDog.tags = 'Lost Chihuahua found on Portswood Road'
		tDog.description = "chihuahua dog portswood southampton lost "
		tDog.location = "Southampton"
		tDog.category = "Animal"
		tDog.date_field = "2015-11-17"
		tDog.time_field = "22:41:28"
		tDog.found_by_user = user
		tDog.save()

		photo = Media()
		photo.of_item = tDog
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'http://thepoodleanddogblog.typepad.com/.a/6a00d83451580669e20115723c6d29970b-pi')
		photo.save()

		tHobbit = Item()
		tHobbit.unique_id = '125678991'
		tHobbit.tags = 'Adele - Rolling in the Deep CD Album'
		tHobbit.description = "adele rolling in the deep cd album"
		tHobbit.location = "Manchester"
		tHobbit.category = "Other"
		tHobbit.date_field = "2015-09-27"
		tHobbit.time_field = "13:44:28"
		tHobbit.found_by_user = user
		tHobbit.save()

		photo = Media()
		photo.of_item = tHobbit
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'http://thumbs2.ebaystatic.com/d/l225/m/mQTzqU9kSL8uIcBHIkfwOqA.jpg')
		photo.save()

		tMug = Item()
		tMug.unique_id = '123654897'
		tMug.description = 'Found this mug at the Solent Library, 2nd Level'
		tMug.tags = "mug white solent southampton"
		tMug.location = "Southampton"
		tMug.category = "Other"
		tMug.date_field = "2015-10-06"
		tMug.time_field = "09:13:28"
		tMug.found_by_user = user
		tMug.save()

		photo = Media()
		photo.of_item = tMug
		photo.media_type = "PHOTO" 
		save_url_to_image(photo, 'https://s-media-cache-ak0.pinimg.com/736x/7c/01/a9/7c01a9440c8e8afde4b11ab4acbfcd3d.jpg')
		photo.save()

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