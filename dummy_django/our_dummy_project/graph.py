import json
import configparser
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient

class Graph:
	config = configparser.ConfigParser()
	# config.read(['config.cfg', 'config.dev.cfg'])
	config['azure'] = {'clientId': '0b89f8ff-7f30-471e-9e64-408604ee8002', 
	'clientSecret': 'VL98Q~MZX6QW6~yIu1x3ozto3ehJgEg0srU.JcCP',
	'tenantId' : '823cde44-4433-456d-b801-bdf0ab3d41fc',
	'authTenant' : '823cde44-4433-456d-b801-bdf0ab3d41fc',
	'graphUserScopes' : 'User.Read Mail.Read Mail.Send' }
	azure_settings = config['azure']
	graph: Graph = Graph(azure_settings)
	settings: SectionProxy
	device_code_credential: DeviceCodeCredential
	user_client: GraphClient
	client_credential: ClientSecretCredential
	app_client: GraphClient

	def __init__(self, config: SectionProxy):
		self.settings = config
		client_id = self.settings['clientId']
		tenant_id = self.settings['authTenant']
		graph_scopes = self.settings['graphUserScopes'].split(' ')

		self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
		self.user_client = GraphClient(credential=self.device_code_credential, scopes=graph_scopes)

	def get_user_token(self):
		graph_scopes = self.settings['graphUserScopes']
		access_token = self.device_code_credential.get_token(graph_scopes)
		return access_token.token

	def display_access_token(graph: Graph):
		token = graph.get_user_token()
		print('User token:', token, '\n')
		
	def get_user(self):
		endpoint = '/me'
		# Only request specific properties
		select = 'displayName,mail,userPrincipalName'
		request_url = f'{endpoint}?$select={select}'

		user_response = self.user_client.get(request_url)
		return user_response.json()

	def greet_user(graph: Graph):
		user = graph.get_user()
		print('Hello,', user['displayName'])
		# For Work/school accounts, email is in mail property
		# Personal accounts, email is in userPrincipalName
		print('Email:', user['mail'] or user['userPrincipalName'], '\n')



	