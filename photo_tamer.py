import os
from PIL import Image
import zipfile

path = os.path.dirname(os.path.abspath(__file__))

def zip(src, dst):
	zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
	abs_src = os.path.abspath(src)
	for dirname, subdirs, files in os.walk(src):
		for filename in files:
			if filename.endswith('.jpg') or filename == 'idlink.txt':
				absname = os.path.abspath(os.path.join(dirname, filename))
				arcname = absname[len(abs_src) + 1:]
				print 'zipping: %s as %s' % (os.path.join(dirname, filename),
											arcname)
				zf.write(absname, arcname)
	zf.close()

print "======================================"
print "Brian's Photo Tamer"
print """
	("`-''-/").___..--''"`-._
	 `6_ 6  )   `-.  (     ).`-.__.`)
	 (_Y_.)'  ._   )  `._ `. ``-..-'
   _..`--'_..-_/  /--'_.' ,'
  (il),-''  (li),'  ((!.-'
"""
print "--------------------------------------"
print "- Removes Leading Zeros, ie '000123.jpg' becomes '123.jpg'"
print "- Renames .JPG to .jpg"
print "--------------------------------------"

idlink_file = os.path.join(path, 'idlink.txt')
f = open(idlink_file,'wb')

for filename in os.listdir(path):
	filepath = os.path.join(path, filename)

	if filename.startswith('0'):
		# remove leading zeros
		new_filename = filename.lstrip("0")
		print "Removing Leading Zeros: %s to %s" % (filename,new_filename)
		os.rename(filepath, os.path.join(path, new_filename))
		filename = new_filename

	if filename.endswith('.JPG'):
		# rename .JPG to .jpg
		new_filename = filename.replace('.JPG', '.jpg')
		print "Renaming .JPG to .jpg: %s to %s" % (filename,new_filename)
		os.rename(filepath, os.path.join(path, new_filename))
		filename = new_filename

	if filename.endswith('.jpg'):
		# write to idlink.txt file
		f.write('"' + filename.replace('.jpg', '') + '","' + ''.join(filename) + '"\n')

		MAX_SIZE = 800
		image = Image.open(filepath)
		original_size = max(image.size[0], image.size[1])

		if original_size >= MAX_SIZE:
			#resized_file = open(filepath.split('.')[0] + '_resized.jpg', "w")
			if (image.size[0] > image.size[1]):
				resized_width = 600
				resized_height = int(round((MAX_SIZE/float(image.size[0]))*image.size[1])) 
			else:
				resized_height = 800
				resized_width = int(round((MAX_SIZE/float(image.size[1]))*image.size[0]))

			image = image.resize((resized_width, resized_height), Image.ANTIALIAS)
			image.save(filename, 'JPEG')

print "======================================"
f.close()
print "idlink.txt created: " + idlink_file

print "Zipping Files..."
zip(path, os.path.join( os.path.dirname( __file__ ), 'output'))

print "Operation Complete!"