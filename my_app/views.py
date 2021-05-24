from django.http import response
from django.shortcuts import render
from requests.compat import quote_plus #this is use for url if ther is a space they put %20 like python tutor => python%20tutor
from bs4 import BeautifulSoup
import requests
from . import models

# Create your views here.

BASE_CRAIGSLIST_URL='https://bangalore.craigslist.org/search/?query={}'
BASE_IMAGE_URL='https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request,'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    print(final_url)

    # Getting the webpage, creating a Response object
    response=requests.get(final_url)
    # Extracting the source code of the page
    data=response.text
    # Passing the source code to Beautiful Soup to create a BeautifulSoup object for it
    soup = BeautifulSoup(data,features='html.parser')
    # Extracting all the <a> tags whose class name is 'result-title' into list

    post_listings= soup.find_all('li',{'class':'result-row'})
    # print(post_listings)

    final_postings=[]

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price='N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url=BASE_IMAGE_URL.format(post_image_id)
            # .format use karvathi BASE_IMAGE_URL ma {} ni under post_image_url aavi jase
            print(post_image_url)
        else:
            post_image_url='https://craigslist.org/images/peace.jpg'

        
        final_postings.append((post_title,post_url,post_price,post_image_url))

    

    stuff_for_frontend = {
        'search':search,
        'final_postings':final_postings,
    }
    return render(request,'my_app/new_search.html',stuff_for_frontend)
