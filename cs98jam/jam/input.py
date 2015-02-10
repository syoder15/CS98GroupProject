from jam.models import Company

## Contains functions to read from a file and upload that information into the database
## File format for companies should be:
## Company, yyyy-mm-dd


def read_from_file(user, input_file):
	print "in read_from_file"
	for line in input_file:
		company_info = line.split(',')
		company_name = company_info[0]
		company_deadline = company_info[1].strip()

		company = Company(name=company_name,
						  application_deadline=company_deadline,
						  user=user)
		company.save()