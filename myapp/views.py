from django.shortcuts import render, redirect
from .forms import MchangoForm, ContributionForm
from .models import Mchango, Contribution
import uuid  # For generating unique links
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.contrib import messages
import logging
from django.urls import reverse
from .utils import send_telegram_message
from django.conf import settings

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'index.html', {'navbar':'home'})
def create_mchango(request):
    if request.method == 'POST':
        form = MchangoForm(request.POST)
        if form.is_valid():
            mchango = form.save(commit=False)
            # Generate a unique link for this mchango
            mchango.unique_link = str(uuid.uuid4())[:8]
            mchango.save()
            return redirect('mchango_detail', unique_link=mchango.unique_link)
    else:
        form = MchangoForm()
    return render(request, 'create_mchango.html', {'form': form})

def mchango_detail(request, unique_link):
    mchango = Mchango.objects.get(unique_link=unique_link)
    return render(request, 'mchango_detail.html', {'unique_link': unique_link, 'mchango': mchango})

def search_mchango(request):
    return render(request, 'search_mchango.html')

def search_results(request):
    unique_id = request.GET.get('unique_id', '')
    mchango = Mchango.objects.filter(unique_link=unique_id).first()

    if mchango:
        return redirect(reverse('contribute', kwargs={'unique_link': mchango.unique_link}))

    else:
        return render(request, 'search_mchango.html', {'not_found_message': 'Mchango not found!'})



def token(request):
    consumer_key = '4IVUlE8RkdtmO5FkgK3aAe1MODdzDUIE'
    consumer_secret = '7rZINuwH1D6JsG0U'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})


def contribute(request, unique_link):
    mchango = Mchango.objects.get(unique_link=unique_link)
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.mchango = mchango
            contribution.save()
            phone = request.POST['phone_number']
            amount = request.POST['contribution_amount']
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            payment_request = {
                "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                "Password": LipanaMpesaPpassword.decode_password,
                "Timestamp": LipanaMpesaPpassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone,
                "PartyB": LipanaMpesaPpassword.Business_short_code,
                "PhoneNumber": phone,
                "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
                "AccountReference": "Mchango",
                "TransactionDesc": "Mchango Contribution"
            }
            # Sending thank you message to contributor
            contributor_name = request.POST.get('contributor_name')
            contribution_amount = request.POST.get('contribution_amount')
            thank_you_message = f"Thank you {contributor_name} for your {contribution_amount} contribution!"
            send_telegram_message(settings.CHAT_IDS['telegram'], thank_you_message)

            # Retrieving all contributors and calculating total contributions
            contributors = Contribution.objects.filter(mchango=mchango)
            total_contributions = sum(contrib.contribution_amount for contrib in contributors)

            # Sending a message with all contributors and total contributions for this mchango
            contributors_message = f"Contributors for {mchango.mchango_name}:\n"
            for contrib in contributors:
                contributors_message += f"- {contrib.contributor_name}: {contrib.contribution_amount}\n"
            contributors_message += f"Total Contributions: {total_contributions}"
            send_telegram_message(settings.CHAT_IDS['telegram'], contributors_message)
            response = requests.post(api_url, json=payment_request, headers=headers)
            return redirect('contribution_success')
    else:
        form = ContributionForm()

    return render(request, 'contribute.html', {'form': form, 'mchango': mchango})


def contribution_success(request):
    return render(request, 'success.html')

def stk(request):
    return render(request, 'contribute.html', {'navbar':'stk'})



