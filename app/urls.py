from django.urls import path
from .views import *

urlpatterns = [
    path('',Home,name="home"),
    # path("signup/", Signup, name="signup"),
    # path("login/", Login, name="login"),
    path("contact/", Contact, name="contact"),
    path("Legal Research/", Blog, name="blog"),
    path("about/", About, name="about"),
    path("what-we/", WhatWe, name="what-we"),

    path("simple/", Simple, name="simple"),
    path("advance/", Advance, name="advance"),
    path("semantic/",Semantic, name="semantic"),

    path("legal-judgement", Legaljudgement, name="legal-judgement"),

    #Specific search
    path("search-judge/", Searchjudge, name="search-judge"),
    path("search-court/", Searchcourt, name="search-court"),
    path("search-date/", Searchdate, name="search-date"),
    path("search-party/", Searchparty, name="search-party"),
    path("search-citation/", Searchcitation, name="search-citation"),
    path("search-bench/", Searchbench, name="search-bench"),
    path("search-act/", Searchact, name="search-act"),
    path("search-lawyer/", Searchlawyer, name="search-lawyer"),

    path("inner-page", testing, name="inner-page"),

    #Fetching a case
    path('fetch/', cases_fetch, name='cases_fetch'),
    path('find_cases_for/', find_cases_for, name='find_cases_for'),

    path('search/suggestions/', search_suggestions, name='search_suggestions'),
    path('search/suggestions/court/', search_suggestions_court, name='search_suggestions_court'),
    path('search/suggestions/petitioner/', search_suggestions_petitioner, name='search_suggestions_petitioner'),
    path('search/suggestions/respondent/', search_suggestions_respondent, name='search_suggestions_respondent'),
    path('predict/', prediction_view, name='predict'),

    path('signup/', signup_view, name='signup'),
    path('login/',login_view, name='login'),
    path('logout/', logout_view, name='logout'),

]