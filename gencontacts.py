#!/usr/bin/env python

	# Simple script to generate a csv containing DMR contacts for the MD2017
	# Note that the generated formatting (with extra spaces etc) will
	# look funny, this is done becuase the MD2017 doesn't actually format
	# the data correctly, so as a quick fix I'm using the screenwrap width 
	# of the MD2017 to format it correctly... TYT developers are a joke

    # Copyright (C) 2017  J Cummings (N0PKT)

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <https://www.gnu.org/licenses/>.
	
	# As a side note, it looks like it's actually doing some calculations with
	# numeric values in this third field... could make for some interesting fun 
	# with buffers....

import requests

# The following variable is a list of countries to include in the output because of
# the need to limit the size of the contact list for the MD2017..
# Country lists fund here: https://www.dmr-marc.net/FAQ/GSM-ID.html
prefixes = [31,11,23,22,26,50]

# because there are some nasty encoded chars in this data, let's lose em
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

# becuase some radios are limited to a set number of contact records (like 100,000 on the MD2017) it is 
# necisarry to limit the number of records.. therefore this function exists to filter (inclusively) which
# records from where..
def includeGeo(record):
	try:
		for prefix in prefixes:
			if record.startswith(str(prefix)):
				return 1
		# If we have exhausted our match list then lets return zarro	
		return 0
	except:
		return 1

def main():
	dmrData = requests.get('https://www.radioid.net/static/users.csv') 
	dmrData.encoding = dmrData.apparent_encoding
	contacts = dmrData.iter_lines()
	for record in contacts:
		record = removeNonAscii(record)
		contact = record.split(",")

		if includeGeo(contact[0]) == 0:
			continue

		p = 25 # looks like they are using 25 chars for the first "name" location and 24 thereafter
		
		# handle the extra-long names
		if len(contact[2]) > 25:
			while len(contact[2]) < 49:
				contact[2] += " "
			p = 24

		# process all entries and add whitespace as-needed
		i = 2
		while i < len(contact):
			while len(contact[i]) < p:
				contact[i] += " "
			i += 1
			p = 24

		# all set, output to stdout
		print("{},{},{}{}{}{}").format(contact[0],contact[1],contact[2],contact[3],contact[4],contact[5].strip())

if __name__ == "__main__":
	main()