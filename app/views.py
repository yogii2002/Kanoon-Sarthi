from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from sparql_queries.queries import get_data
from .case_file_retrieve import *
from .model import *
from django.shortcuts import render
import re
import numpy as np
import xml.etree.ElementTree as ET
from django.utils.safestring import mark_safe
from collections import defaultdict

# from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.contrib import messages


def prediction_view(request):
    if request.method == 'POST':
        if request.POST.get('text'):
            user_input = request.POST.get('text')
        else:
            uploaded_file = request.FILES['uploaded_file']
            # Read the contents of the uploaded file
            user_input = uploaded_file.read().decode('utf-8')

        translation_file_path = "translation.tmx"  # Path to the translation memory file
        file_embeddings = {}

        # Parse the translation file and extract the file embeddings
        
        tree = ET.parse(translation_file_path)
        root = tree.getroot()
        body = root.find("body")

        for tu in body.iter("tu"):
            # Extract the file name (source segment) and embedding (target segment)
            file_name = tu[0][0].text
            embedding = np.fromstring(tu[1][0].text[1:-1], sep=' ')

            # Store the file embedding in the dictionary
            file_embeddings[file_name] = embedding
        model_name = 'sentence-transformers/bert-base-nli-mean-tokens'
        model = SentenceTransformer(model_name)
        user_embeddings = model.encode([user_input])
        user_mean_pooled = np.mean(user_embeddings, axis=0)

        # Compare the user's mean pooled embeddings with the translation memory
        similarity_scores = {}
        for file_path, embedding in file_embeddings.items():
            score = np.dot(user_mean_pooled, embedding) / (np.linalg.norm(user_mean_pooled) * np.linalg.norm(embedding))
            score *= 100
            similarity_scores[file_path] = score

        # Sort the files based on similarity scores
        sorted_files = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Create a list of dictionaries containing file paths and similarity scores
        predictions = [{'file_path': file_path, 'score': score} for file_path, score in sorted_files]

        # Pass the file_scores list to the template
        
       
        sparql=get_data()
        judge = sparql.all_cases()
        facts = sparql.allcase_facts()
        print(facts)
        # grouped_data = defaultdict(list)
        # for case in facts:
        #     case_name = case.get('CaseName')
        #     facts_label = case.get('factsLabel')
            
        #     if case_name and facts_label:
        #         grouped_data[case_name].append(facts_label)

        zipped_data = zip(predictions, judge)
        context = {'zipped_data': zipped_data,
                   'facts': facts,}
        return render(request, 'app/prediction_result.html', context)
    else:
        unique_years = ['Facts' , 'Analysis' , 'Ratio' , 'Pre-Relied', 'Issue' , 'Pre-NotRelied']
        return render(request, 'app/prediction_form.html' , {'unique_years': unique_years})


# Create your views here.

def Home(request):
    return render(request,"app/index.html")














def About(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        pswd = request.POST['password']
        fnd1 = User.objects.filter(email = request.POST['email'].lower())
        # fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) > 0:
            print("Hello")
        
        else:
            messages.error(request, "User does not exist. Please register.")
            return redirect("index")
    else:
        sparql=get_data()
        facts = sparql.facts_for_case('Komal And Others, Meharban And ... vs State Of Uttar Pradesh')
        print(facts)
        return render(request, "app/about.html")
    
def testing(request):
    if request.method == "POST":
        print('hello')
    else:
        sparql=get_data()
        test=sparql.allcase_prerel()
        # facts = sparql.allcase_facts()
        # sections = sparql.section_for_fact('The appellant Trust was registered under the 1 Societies Registration Act, 1860 originally and now regulated under the Tamil Nadu Societies Registration Act, 1975.')
        # facts = sparql.section_for_fact("and a copy of the test report should be forwarded to Electrical Inspector. 9. Sanction from K.S.E.B. under Section 44 of Supply Act 1948 should be obtained and copy forwarded to the Electrical Inspector. 10. Only materials with I.S. certification as required under QCO should be used.")
        test1 = sparql.case_id()
        test = sparql.cites("200701KS10SC")
        print(test1)
        print(test)
        return render(request, "app/inner-page.html",{'facts':test})
    
def Contact(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        pswd = request.POST['password']
        fnd1 = User.objects.filter(email = request.POST['email'].lower())
        # fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) > 0:
            print("Hello")
        
        else:
            messages.error(request, "User does not exist. Please register.")
            return redirect("index")
    else:
        return render(request, "app/contact.html")

def Blog(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        pswd = request.POST['password']
        fnd1 = User.objects.filter(email = request.POST['email'].lower())
        # fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) > 0:
            print("Hello")
        
        else:
            messages.error(request, "User does not exist. Please register.")
            return redirect("index")
    else:
        return render(request, "app/blog.html")
    
def WhatWe(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        pswd = request.POST['password']
        fnd1 = User.objects.filter(email = request.POST['email'].lower())
        # fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) > 0:
            print("Hello")
        
        else:
            messages.error(request, "User does not exist. Please register.")
            return redirect("index")
    else:
        return render(request, "app/what-we.html")
    
def Simple(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        pswd = request.POST['password']
        fnd1 = User.objects.filter(email = request.POST['email'].lower())
        # fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) > 0:
            print("Hello")
        
        else:
            messages.error(request, "User does not exist. Please register.")
            return redirect("index")
    else:
        sparql=get_data()
        judge = sparql.court_case_name('Supreme Court of India')
        print(judge)
        return render(request, "app/simple.html")

def Advance(request):
    if request.method == "POST":
        petitioner = request.POST.get('petitioner')
        respondent = request.POST.get('respondent')
        judge = request.POST.get('respondent')
        court = request.POST.get('court')
        appealno = request.POST.get('appealno')
        date = request.POST.get('date')
        year = request.POST.get('year')
        parameter = request.POST.get('job')
        yearNo = request.POST.get('last_year')
        caseType = request.POST.get('type')
        decision = request.POST.get('decision')
        if parameter == 'and':
            sparql=get_data()
            case = sparql.advance_search_and(petitioner,respondent,judge,court,appealno,date,year,yearNo,caseType,decision)
        else:
            sparql=get_data()
            case = sparql.advance_search_or(petitioner,respondent,judge,court,appealno,date,year,yearNo,caseType,decision)
        
        unique_years = set(cases['date'][-4:] for cases in case)
        unique_courts = set(cases['courtName'] for cases in case)
        return render(request, 'app/advance_result.html', {'case': case,
                                                           'unique_years':unique_years,
                                                           'unique_courts': unique_courts})
    else:
        sparql=get_data()
       # advance = sparql.advance_search("ramesh kumar","","S.B. Sinha","Supreme Court of India","appeal no 398 of 2008","","2008")
        #advance = sparql.advance_search_or("ramesh kumar","","","","","","","5","civil","")
    return render(request, "app/advance.html")
    
def Semantic(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        pswd = request.POST['password']
        fnd1 = User.objects.filter(email = request.POST['email'].lower())
        # fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) > 0:
            print("Hello")
        
        else:
            messages.error(request, "User does not exist. Please register.")
            return redirect("index")
    else:
        return render(request, "app/semantic.html")
    
def Legaljudgement(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        pswd = request.POST['password']
        fnd1 = User.objects.filter(email = request.POST['email'].lower())
        # fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) > 0:
            print("Hello")
        
        else:
            messages.error(request, "User does not exist. Please register.")
            return redirect("index")
    else:
        return render(request, "app/legal-judgement.html")
    
def Searchjudge(request):
    if request.method == "POST":
        judgename = request.POST.get('judgename')
        # judgename = request.GET.get('judgename', '')
        print(judgename)
        sparql=get_data()
        #res = sparql.case_details(result_string)
        case = sparql.judge_case_name(judgename)
        #print(case)
        # temporary = sparql.case_info("State Of Kerala vs Indian Aluminium Co, Ltd And Ors")
        # print(temporary)
        print(case)
        length = len(case)
        unique_years = set(cases['date'][-4:] for cases in case)
        unique_courts = set(cases['court'] for cases in case)
        # result = res[0]
        return render(request, "app/searchjudge.html", 
                      {'case':case,
                       'name': request.POST.get('judgename'),
                        'length':length,
                        # 'result': result
                        'unique_years': unique_years,
                        'unique_courts': unique_courts,
                        })
    else:
        judgename = request.GET.get('judgename', '')
        print(judgename)
        sparql=get_data()
        #res = sparql.case_details(result_string)
        case = sparql.judge_case_name(judgename)
        #print(case)
        # temporary = sparql.case_info("State Of Kerala vs Indian Aluminium Co, Ltd And Ors")
        # print(temporary)
        print(case)
        length = len(case)
        unique_years = set(cases['date'][-4:] for cases in case)
        unique_courts = set(cases['court'] for cases in case)
        # result = res[0]
        return render(request, "app/searchjudge.html", 
                      {'case':case,
                       'name': request.GET.get('judgename', ''),
                        'length':length,
                        # 'result': result
                        'unique_years': unique_years,
                        'unique_courts': unique_courts,
                        })
    
def Searchcourt(request):
    if request.method == "POST":
        courtname = request.POST.get('courtname')
        sparql=get_data()
        case = sparql.court_case_name(courtname)
        length = len(case)
        return render(request, "app/searchcourt.html", 
                      {'case':case,
                        'length':length})
    else:

        return render(request, "app/searchcourt.html")
    
def Searchdate(request):
    if request.method == 'POST':
        # print("hello",request.POST.get) 
        date = request.POST.get("date-input")
        
        # date = request.POST.get("date") this line was written debug by yogeshjat its above line is correct
        print("printing and checking date",date)
        last_year = request.POST.get('last_year')
        print("checking last year",last_year)
        last_year=str(last_year)
        sparql=get_data()
        # case
        if(date):
            case = sparql.date_case_name(date)
        if(last_year):
            case = sparql.last_year(last_year)

        print("printing final case",case)

# Extract the case names from the response
        # length = len(case)
        return render(request, "app/searchdate.html", 
                      {'case':case,
                        # 'length':length
                        })
    else:

        return render(request, "app/searchdate.html")
    
def Searchparty(request):
    if request.method == 'POST':
        if request.POST.get('respondent'):
            sparql=get_data()
            party = request.POST.get('respondent')
            case = sparql.respondent_case_name(party)
        else:
            party = request.POST.get('petitioner')
            sparql=get_data()
            case = sparql.petitioner_case_name(party)
        
        
        length = len(case)
        return render(request, "app/searchparty.html", 
                      {'case':case,
                        'length':length})
    else:
        if request.GET.get('respondent', ''):
            sparql=get_data()
            party = request.GET.get('respondent', '')
            case = sparql.respondent_case_name(party)
        else:
            party = request.GET.get('petitioner', '')
            sparql=get_data()
            case = sparql.petitioner_case_name(party)
        length = len(case)
        return render(request, "app/searchparty.html", 
                      {'case':case,
                        'length':length})

def Searchcitation(request):
    if request.method == 'POST':
        print('hello')
    else:
        return render(request, "app/searchcitation.html")

# code added by yogeshjat on 22march2025
def Searchbench(request):
    # print("my name is yogesh")
    # print("my request is",request.POST)
    if request.method == 'POST':
        sparql=get_data()
        bench=request.POST.get('Benchname')
        case=sparql.casename_searchbybench(bench)
        
        length=len(case)
        return render(request,"app/searchbench.html",{'case':case,'length':length})
    
    else:
        sparql=get_data()
        bench=request.GET.get('Benchname')
        case=sparql.cites(bench)
        
        length=len(case)
        return render(request,"app/searchbench.html",{'case':case,'length':length})
    # return render(request,"app/searchbench.html")
    
def Searchact(request):
    if request.method == 'POST':
        print('hello')
    else:
        return render(request, "app/searchact.html")
    
def Searchlawyer(request):
    if request.method == 'POST':
        print('hello')
    else:
        return render(request, "app/searchlawyer.html")
    
# def cases_fetch(request):
#     result_string = request.GET.get('result_string', '')
#     sparql=get_data()
#     res = sparql.case_details(result_string)
#     id = sparql.case_id(request.GET.get('result_string', ''))
#     text = retrieve_matching_cases(id[0])
#     judges = [obj for obj in res if 'judges' in obj]
#     result = res[0]
#     context = {
#         'result': result,
#         'judges': judges,
#         'text': text,
#         'name': request.GET.get('result_string', '')
#     }
#     return render(request, "app/cases_fetch.html",context)

def cases_fetch(request):
    result_string = request.GET.get('result_string', '')
    sparql=get_data()
    res = sparql.case_details(result_string)
    # res = sparql.case_details('Bokka Subba Rao vs Kukkala Balakrishna & Ors')
    result = res[0]
    # id = sparql.case_id(request.GET.get('result_string', ''))
    # text = retrieve_matching_cases(id[0])
    # judges = [obj for obj in res if 'judges' in obj]
    # result = res[0]
    response_data = sparql.case_info(request.GET.get('result_string', ''))
    print(response_data)
    judges = [item['judgeName'] for item in response_data if 'judgeName' in item]
    provisions = [item['provision'] for item in response_data if 'provision' in item]
    court_name = [item['courtName'] for item in response_data if 'courtName' in item]
    petitioner = [item['petitioner'] for item in response_data if 'petitioner' in item]
    respondent = [item['respondent'] for item in response_data if 'respondent' in item]
    date = [item['date'] for item in response_data if 'date' in item]
    caseNo = [item['caseNo'] for item in response_data if 'caseNo' in item]
    decision = [item['decision'] for item in response_data if 'decision' in item]
    juridiction = [item['juridiction'] for item in response_data if 'juridiction' in item]
    author_name = [item['authorName'] for item in response_data if 'authorName' in item]
    judges = [item['judgeName'] for item in response_data if 'judgeName' in item]
    cites = [item['cites'] for item in response_data if 'cites' in item]
    facts_labels = [item['factsLabel'] for item in response_data if 'factsLabel' in item]
    fact_sections = {}
    for item in response_data:
        if 'factsLabel' in item:
            fact_label = item['factsLabel']
            fact_sections[fact_label] = sparql.section_for_fact(fact_label)
    provisions = [item['provision'] for item in response_data if 'provision' in item]
    stat = [item['statute'] for item in response_data if 'statute' in item]

    highlighted_fact_sections = {}

    for text, sections in fact_sections.items():
        highlighted_text = text
        for section in sections:
            statute = section.get('statute', '')
            if statute:
                if '(' in statute and ')' in statute:
                    statutes = statute[:-7] 
                else:
                    statutes = statute
                highlighted_text = re.sub(re.escape(statutes), f'<span class="highlight">{statute}</span>', highlighted_text)

            provision = section.get('provision', '')
            if provision:
                highlighted_text = re.sub(re.escape(provision), f'<span class="highlightpro">{provision}</span>', highlighted_text)
            
        
        highlighted_fact_sections[text] = mark_safe(highlighted_text)
    context = {
        'result': result,
        'judges': judges,
        'fact_sections': fact_sections,
        'petitioner': petitioner,
        'respondent': respondent,
        'date': date,
        'caseNo': caseNo,
        'decision': decision,
        'juridiction': juridiction,
        'author_name': author_name,
        'cites':cites,
        'facts_labels': facts_labels,
        'stat': stat,
        'provisions': provisions,
        'court_name':court_name,
        'highlighted_fact_sections': highlighted_fact_sections,
        'name': request.GET.get('result_string', '')
    }
    return render(request, "app/cases_fetch.html",context)

def find_cases_for(request):
    if request.GET.get('respondent', ''):
        sparql=get_data()
        party = request.GET.get('respondent', '')
        case = sparql.respondent_case_name(party)
    elif request.GET.get('petitioner', ''):
        party = request.GET.get('petitioner', '')
        sparql=get_data()
        case = sparql.petitioner_case_name(party)
    elif request.GET.get('judgename', ''):
        party = request.GET.get('judgename', '')
        sparql=get_data()
        #res = sparql.case_details(result_string)
        case = sparql.judge_case_name(party)
        #print(case)
        # temporary = sparql.case_info("State Of Kerala vs Indian Aluminium Co, Ltd And Ors")
        # print(temporary)
        unique_years = set(cases['date'][-4:] for cases in case)
        unique_courts = set(cases['court'] for cases in case)
        # result = res[0]    
    
    length = len(case)
    return render(request, "app/find_cases_for.html", 
                    {'case':case,
                     'name': party,
                    'length':length})

def search_suggestions(request):
    # query = request.GET.get('query')
    sparql=get_data()
    res = sparql.all_judges()
    # Perform a search query or any other logic to retrieve suggestions
    suggestions = res
    
    return JsonResponse({'suggestions': suggestions})

def search_suggestions_court(request):
    # query = request.GET.get('query')
    sparql=get_data()
    res = sparql.all_courts()
    # Perform a search query or any other logic to retrieve suggestions
    suggestions = res
    
    return JsonResponse({'suggestions': suggestions})

def search_suggestions_petitioner(request):
    # query = request.GET.get('query')
    sparql=get_data()
    res = sparql.all_petitioners()
    # Perform a search query or any other logic to retrieve suggestions
    suggestions = res
    
    return JsonResponse({'suggestions': suggestions})

def search_suggestions_respondent(request):
    # query = request.GET.get('query')
    sparql=get_data()
    res = sparql.all_respondents()
    # Perform a search query or any other logic to retrieve suggestions
    suggestions = res
    
    return JsonResponse({'suggestions': suggestions})
















def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if len(password) < 6:
            messages.error(request, "Password should be at least 6 characters long.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'app/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')  # Replace with your post-login redirect
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'app/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')