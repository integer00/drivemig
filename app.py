#!/usr/bin/env python3
#####
#find sync folder id
#check for sync folder in drive directory, if none -> create

#should check diff for files

from __future__ import print_function
import argparse
import pickle
import os.path
import sys
import magic

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from googleapiclient.http import MediaFileUpload

def upload():
	print('uploading')
	exit(0)

def download():
	print("downloading")
	exit(0)

def get_creds():
	SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
	          'https://www.googleapis.com/auth/drive.file']

	"""Shows basic usage of the Drive v3 API.
	Prints the names and ids of the first 10 files the user has access to.
	"""

	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'client_id.json', SCOPES)
			creds = flow.run_local_server()
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	return build('drive', 'v3', credentials=creds)


def prepare():
	pass


def main():

	#make parser
	parser = argparse.ArgumentParser()
	sub_parser = parser.add_subparsers(dest='choose')
	uparser = sub_parser.add_parser('upload')
	dparser = sub_parser.add_parser('download')

	uparser.add_argument('data_upload', type=str, nargs='+')
	uparser.add_argument('-v','--verbose', help='show execution and exit', action='store_true')
	dparser.add_argument('data_download', type=str, nargs='+')

	if len(sys.argv) == 1:
		parser.print_usage()
		exit(0)
	args = parser.parse_args()
	service = get_creds()

	service.files().create(
		body={'name': 'sync',
		      'mimeType': 'application/vnd.google-apps.folder'}
		, fields='id').execute()


	if args.choose == 'upload':
		print(args)
		for each in args.data_upload:
			ap = os.path.abspath(each)
			fn = os.path.basename(each)
			m = magic.Magic(mime=True, uncompress=True)
			mime = m.from_file(ap)
			# todo handle empty mime
			# todo handle folder mime

			if args.verbose:
				print("will upload: [" + ap +"]")
				continue

			# todo handle folder
			file_metadata = {'name': fn}
			media = MediaFileUpload(ap, mimetype=mime)
			print("uploading " + ap + " [" + mime + "]")
			service.files().create(body=file_metadata, media_body=media, fields='id').execute()
			# file_metadata = {
			# 	'name': 'Invoices',
			# 	'mimeType': 'application/vnd.google-apps.folder'
			# }
			# service.files().create(body=file_metadata, fields='id').execute()
		print("done")
		exit(0)

	if args.choose == 'download':
		print(args)

	# Call the Drive v3 API
	# results = service.files().list(
	# 	pageSize=10, fields="nextPageToken, files(id, name)").execute()
	# items = results.get('files', [])

	# if not items:
	# 	print('No files found.')
	# else:
	# 	print('Files:')
	# 	for item in items:
	# 		print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
	main()