import time
import xml.etree.ElementTree as ET

# Read original EZID export tree
t = ET.parse('ezid_export_example.xml')
t_records = t.getroot()

# Create new CrossRef import tree
doi_batch = ET.Element('doi_batch', {
	'xmlns' : 'http://www.crossref.org/schema/4.4.1',
	'xmlns:xsi' : 'http://www.w3.org/2001/XMLSchema-instance',
	'version' : '4.4.1',
	'xsi:schemaLocation' : 'http://www.crossref.org/schema/4.4.1 http://www.crossref.org/schemas/crossref4.4.1.xsd'
	})

# Create head tags
head = ET.SubElement(doi_batch, 'head')

doi_batch_id = ET.SubElement(head, 'doi_batch_id')
doi_batch_id.text = '2006-03-24-21-57-31-10023'

timestamp = ET.SubElement(head, 'timestamp')
timestamp.text = str(int(time.time())) # This is different from Maggie's example

depositor = ET.SubElement(head, 'depositor')
depositor_name = ET.SubElement(depositor, 'depositor_name')
depositor_name.text = 'Duke University Libraries'
depositor_email = ET.SubElement(depositor, 'email_address')
depositor_email.text = 'ddrhelp@duke.edu'

registrant = ET.SubElement(head, 'registrant')
registrant.text = 'Duke University Libraries'

# Create body tags
body = ET.SubElement(doi_batch, 'body')

# MorphoSource database 
ms_database = ET.SubElement(body, 'database')

# MorphoSource Database metadata
ms_database_metadata = ET.SubElement(ms_database, 'database_metadata', {'language' : 'en'})
ms_titles = ET.SubElement(ms_database_metadata, 'titles')
ms_title = ET.SubElement(ms_titles, 'title')
ms_title.text = 'MorphoSource Media'
ms_institution = ET.SubElement(ms_database_metadata, 'institution')
ms_institution_name = ET.SubElement(ms_institution, 'institution_name')
ms_institution_name.text = 'MorphoSource'

# DDR database 
ddr_database = ET.SubElement(body, 'database')

# DDR Database metadata
ddr_database_metadata = ET.SubElement(ddr_database, 'database_metadata', {'language' : 'en'})
ddr_titles = ET.SubElement(ddr_database_metadata, 'titles')
ddr_title = ET.SubElement(ddr_titles, 'title')
ddr_title.text = 'Duke Digital Repository'
ddr_institution = ET.SubElement(ddr_database_metadata, 'institution')
ddr_institution_name = ET.SubElement(ddr_institution, 'institution_name')
ddr_institution_name.text = 'Duke University Libraries'

# Datasets (one per DOI)
# loop through doi records
for record in t_records:
	# Get EZID metadata values
	record_dict = dict()
	record_dict['doi'] = record.attrib['identifier']
	for element in record:
		for k, v in element.attrib.items():
			record_dict[v] = element.text

	# Construct CrossRef metadata tags

	if record_dict['_owner'] == 'duke_morpho':
		dataset = ET.SubElement(ms_database, 'dataset', {'dataset_type' : 'record'})
	else:
		dataset = ET.SubElement(ddr_database, 'dataset', {'dataset_type' : 'record'})

	if 'datacite.creator' in record_dict:
		contributors = ET.SubElement(dataset, 'contributors')
		person_name = ET.SubElement(contributors, 'person_name', {
			'contributor_role' : 'author',
			'sequence' : 'first' 
		})

		full_name = record_dict['datacite.creator']
		if ';' in full_name:
			full_name = full_name.split(';')[0]
		if ',' in full_name:
			lname, fname = full_name.split(',', 1)
		else:
			fname, lname = full_name.rsplit(' ', 1)

		given_name = ET.SubElement(person_name, 'given_name')
		given_name.text = fname
		surname = ET.SubElement(person_name, 'surname')
		surname.text = lname

	if 'datacite.title' in record_dict:
		titles = ET.SubElement(dataset, 'titles')
		title = ET.SubElement(titles, 'title')
		title.text = record_dict['datacite.title']

	if 'datacite.publicationyear' in record_dict:
		database_date = ET.SubElement(dataset, 'database_date')
		publication_date = ET.SubElement(database_date, 'publication_date')
		year = ET.SubElement(publication_date, 'year')
		year.text = record_dict['datacite.publicationyear']

	if 'datacite.resourcetype' in record_dict:
		ds_format = ET.SubElement(dataset, 'format')
		ds_format.text = record_dict['datacite.resourcetype']

	doi_data = ET.SubElement(dataset, 'doi_data')
	doi = ET.SubElement(doi_data, 'doi')
	doi.text = record_dict['doi'].replace('doi:', '')
	resource = ET.SubElement(doi_data, 'resource')
	resource.text = record_dict['_target']

new_tree = ET.ElementTree(doi_batch)
new_tree.write('dul_generated_crossref_dataset.xml')









