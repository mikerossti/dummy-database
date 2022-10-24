from multiprocessing import context
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from passlib.hash import pbkdf2_sha256
from django.core.mail import send_mail
from django.conf import settings
from django.urls import include, path
import uuid
import re
import msal
from django.contrib.auth import login, logout
from microsoft_authentication.auth.auth_utils import (
	get_sign_in_flow,
	get_token_from_code,
	get_user,
	get_django_user,
	get_logout_url,
)
from our_dummy_project import graph
import configparser
from .graph import Graph
from microsoft_authentication.auth.auth_decorators import microsoft_login_required


config = configparser.ConfigParser()
# config.read(['config.cfg', 'config.dev.cfg'])
config['azure'] = {'clientId': '0b89f8ff-7f30-471e-9e64-408604ee8002', 
'clientSecret': 'VL98Q~MZX6QW6~yIu1x3ozto3ehJgEg0srU.JcCP',
'tenantId' : '823cde44-4433-456d-b801-bdf0ab3d41fc',
'authTenant' : '823cde44-4433-456d-b801-bdf0ab3d41fc',
'graphUserScopes' : 'User.Read Mail.Read Mail.Send' }
azure_settings = config['azure']

graph: Graph = Graph(azure_settings)


# Home and Landing Page
def index(response):
	return render(response, "index.html", {})

class IndexView(View):
	def get(self, request):
		user = graph.get_user()
		name = user['displayName']
		
		context = {
			'user': user,
			'name': name,
		}
		return render(request, 'index.html', context)

def microsoft_logout(request):
	logout(request)
	return HttpResponseRedirect(get_logout_url())

@microsoft_login_required()
def home(request):
	return HttpResponse("Logged in")

# If pages need to be restricted to certain groups of users.
@microsoft_login_required(groups=("SpecificGroup1", "SpecificGroup2"))  # Add here the list of Group names
def specific_group_access(request):
	return HttpResponse("You are accessing page which is accessible only to users belonging to SpecificGroup1 or SpecificGroup2")

