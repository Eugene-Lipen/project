from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import HttpResponseRedirect, FileResponse, Http404
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Category, Subcategory, Product, Test, Instruction, User, Work_Name
from testing.models import TestingPeople, TestingCategory


class SearchResultsView(ListView):
    model = Product
    template_name = 'search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['name'] = username

        return context

    def get_queryset(self):  # новый

        query = self.request.GET.get('q').lower()
        object_list = Product.objects.filter(
            Q(title__iregex=query)
        )
        print(object_list)

        return object_list





def show_account(request):
    username = request.user.username
    user = User.objects.filter(username = username).values()
    test = TestingPeople.objects.filter(people_id=user[0]['id']).values()
    position = Work_Name.objects.filter(id=user[0]['position_id']).values()
    position=position[0]['name']


    for i in test:
        if i['switch1'] == True or i['switch2'] == True:
            category_test = TestingCategory.objects.filter(id=i['test_id']).values()[0]['name']
            print(category_test)
            return render(request, 'personal_account.html', {'user': user, 'name': username, 'test':i, 'category_test': category_test, 'position':position})

    return render(request, 'personal_account.html', {'user': user, 'name': username,'position':position})

@login_required
def show_category(request):
    category = Category.objects.all()
    username = request.user.username
    return render(request, 'category.html', {'name': username, 'category': category})

@login_required
def show_subcategory(request, category_slug):
    cat_id = Category.objects.filter(slug=category_slug).values()
    sub = Subcategory.objects.filter(category_id=cat_id[0]['id'])
    username = request.user.username
    return render(request, 'subcategory.html', {'name': username, 'subcategory': sub})

@login_required
def show_product(request, category_slug, subcategory_slug):
    print(subcategory_slug)
    subcat_id = Subcategory.objects.filter(slug=subcategory_slug).values()
    print(subcat_id)
    product = Product.objects.filter(subcategoria_id=subcat_id[0]['id'])

    print(product)
    username = request.user.username
    return render(request, 'product.html', {'name': username, 'product': product})

@login_required
def show_card(request, category_slug, subcategory_slug, product_slug):

    product = Product.objects.filter(slug=product_slug)
    print(product)
    username = request.user.username
    return render(request,'card.html', {'card':product, "name":username})

@login_required
def show_test(request):
    test = Test.objects.all()
    username = request.user.username
    return render(request, "test.html", {'test':test, 'name': username})


def entry(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return HttpResponseRedirect(reverse('top'))
        else:
            return TemplateResponse(request, 'login.html', {'error': True})
    else:
        return TemplateResponse(request, 'login.html', {})

@login_required
def account_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('entry'))

@login_required
def instructions(request):
    document = Instruction.objects.all()
    username = request.user.username
    return render(request,'instructions.html', {'document': document, 'name': username})


#def pdf_view(request, pk):
 #   print(1)
  #  return FileResponse('media/document/2_Инструкция_по_оказанию_первой_помощи_пострадавшим_4.doc')



@login_required
def pdf_view(request, slug_instruction):
    fs = FileSystemStorage()
    filename = Instruction.objects.filter(slug=slug_instruction).values()[0]['document']
    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        return response

