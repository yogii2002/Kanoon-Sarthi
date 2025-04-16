from SPARQLWrapper import SPARQLWrapper, JSON , CSV
import pandas as pd
import numpy as np
import datetime
import re
class get_data:
   
   def __init__(self):
      
      self.sparql = SPARQLWrapper('https://fusekiserver-production.up.railway.app/test_kg/sparql')
      print("hello")

   def case_id(self):       
      query="""      
      prefix nyon: <https://w3id.org/def/NyOn#>
      select distinct ?case where
      {
         ?case nyon:hasCaseName  ?casename.
      }
      """  
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      caseid = []
      for result in results["results"]["bindings"]:
           caseid.append( result["case"]["value"])

      cid=[]
      for case in caseid:
         parts = case.split('/')
         last_part = parts[-1]

         if 'case' in last_part:
            last_part = last_part.split('case')[-1]
         cid.append(last_part)
      return cid
      
   def cites(self,case):   
      caseid = f"<https://w3id.org/def/NyOn#Case{case}>"   
      query="""      
      prefix nyon: <https://w3id.org/def/NyOn#>
      select ?caseName ?cite ?citeby ?eqcite where
      {
         {
            """+caseid+""" nyon:hasCaseName  ?caseName.   
         }
        union
         {
            """+caseid+""" nyon:Cites ?cite.
         }
        union
         {
            """+caseid+""" nyon:Citedby ?citeby.
         }
        union
         {
            """+caseid+""" nyon:equalcite ?eqcite.
         }
       }
      """  
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      case_cite = []

      for result in results["results"]["bindings"]:
         cites = {}
         if "caseName" in result:
          cites["caseName"] = result["caseName"]["value"]
         if "cite" in result:
          cites["cite"] = result["cite"]["value"]
         if "citeby" in result:
          cites["citeby"] = result["citeby"]["value"]
         if "eqcite" in result:
          cites["eqcite"] = result["eqcite"]["value"]
         case_cite.append(cites)
      
      return case_cite
   
   def judge_case_name(self,name):       
        query="""
        PREFIX nyon: <https://w3id.org/def/NyOn#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?CaseName ?date ?court ?type ?decision where
        {
           ?judges rdfs:label '""" + name+"""'@en.
           ?case nyon:hasCourtOfficial ?judges;                                                
                 nyon:hasCaseName ?CaseName;
                 nyon:hasDate ?date;
                 nyon:hasCourt ?courts;
                 nyon:hasCaseType ?type;
                 nyon:hasCourtDecision ?deci.
           ?courts rdfs:label ?court.
           ?deci rdfs:label ?decision.
        }
        """ 
        #   print(query)
        self.sparql.setQuery(query)        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        case = []
        for result in results["results"]["bindings"]:
         case.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "court": result["court"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
        return case
    
   def all_judges(self):       
        query="""
        prefix nyon: <https://w3id.org/def/NyOn#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select distinct ?JudgeName where
        {
           ?case nyon:hasCourtOfficial ?judges.
           ?judges rdfs:label ?JudgeName.
        }
        """ 
        self.sparql.setQuery(query)
        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
           
        all_judgename = []
        print(results)
        for result in results["results"]["bindings"]:
              all_judgename.append( result["JudgeName"]["value"])
             
        return all_judgename
    

   def court_case_name(self,name):       
        query="""
        PREFIX nyon: <https://w3id.org/def/NyOn#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?CaseName ?date ?court ?type ?decision where
        {
           ?courts rdfs:label '""" + name+"""'@en.
           ?case nyon:hasCourt ?courts;                                                
                 nyon:hasCaseName ?CaseName;
                 nyon:hasDate ?date;
                 nyon:hasCaseType ?type;
                 nyon:hasCourtDecision ?deci.
           ?courts rdfs:label ?court.
           ?deci rdfs:label ?decision.
        }
        """ 
        #   print(query)
        self.sparql.setQuery(query)        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        case = []
        for result in results["results"]["bindings"]:
         case.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "court": result["court"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
        return case
    
    
   def all_courts(self):       
        query="""
        prefix nyon: <https://w3id.org/def/NyOn#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select distinct ?CourtName where
        {
           ?case nyon:hasCourt ?court.
           ?court rdfs:label ?CourtName.
        }
        """ 
        self.sparql.setQuery(query)
        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
           
        all_courtname = []
        print(results)
        for result in results["results"]["bindings"]:
              all_courtname.append( result["CourtName"]["value"])
             
        return all_courtname
    

   def date_case_name(self,date):      
        date_s = datetime.datetime.strptime(date, "%Y-%m-%d") 
        date_string = date_s.strftime("%d/%m/%Y") 
        query= f"""
    PREFIX case: <https://w3id.org/def/NyOn#Case>
    PREFIX nyon: <https://w3id.org/def/NyOn#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?caseName ?date ?court ?type ?decision
    WHERE {{
        ?case a nyon:Case;
              nyon:hasDate ?date;
              nyon:hasCaseName ?caseName;
              nyon:hasCourt ?courts;
              nyon:hasCaseType ?type;
              nyon:hasCourtDecision ?deci.

        ?courts rdfs:label ?court.
        ?deci rdfs:label ?decision.

        FILTER(?date = "{date_string}")
    }}
    """ 
        #   print(query)
        self.sparql.setQuery(query)        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        case = []
        for result in results["results"]["bindings"]:
         case.append({
            "CaseName": result["caseName"]["value"],
            "date": result["date"]["value"],
            "court": result["court"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
        return case
    
   def petitioner_case_name(self,name):       
        query="""
        PREFIX nyon: <https://w3id.org/def/NyOn#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?CaseName ?date ?court ?type ?decision where
        {
           ?party rdfs:type nyon:Petitioner;
                  rdfs:label '""" + name+"""'@en.
           ?case nyon:hasParty ?party;                                                 
                 nyon:hasCaseName ?CaseName;
                 nyon:hasCourt ?courts;
                 nyon:hasDate ?date;
                 nyon:hasCaseType ?type;
                 nyon:hasCourtDecision ?deci.
           ?courts rdfs:label ?court.
           ?deci rdfs:label ?decision.
        }
        """ 
        #   print(query)
        self.sparql.setQuery(query)        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        case = []
        for result in results["results"]["bindings"]:
         case.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "court": result["court"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
        return case
    
   def all_petitioners(self):       
        query="""
        PREFIX nyon: <https://w3id.org/def/NyOn#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select distinct ?petitioner where
        {
         ?case nyon:hasParty ?party.
         ?party rdfs:type nyon:Petitioner;
         rdfs:label ?petitioner.
        }
        """
        self.sparql.setQuery(query)
        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
           
        all_petitioner = []
      #   print(results)
        for result in results["results"]["bindings"]:
              all_petitioner.append( result["petitioner"]["value"])
             
        return all_petitioner
    
   def respondent_case_name(self,name):       
        query="""
        PREFIX nyon: <https://w3id.org/def/NyOn#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select ?CaseName ?date ?court ?type ?decision where
        {
           ?party rdfs:type nyon:Respondent;
                  rdfs:label '""" + name+"""'@en.
           ?case nyon:hasParty ?party;                                                 
                 nyon:hasCaseName ?CaseName;
                 nyon:hasCourt ?courts;
                 nyon:hasDate ?date;
                 nyon:hasCaseType ?type;
                 nyon:hasCourtDecision ?deci.
           ?courts rdfs:label ?court.
           ?deci rdfs:label ?decision.
        }
        """ 
        #   print(query)
        self.sparql.setQuery(query)        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        case = []
        for result in results["results"]["bindings"]:
         case.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "court": result["court"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
        return case
    
   def all_respondents(self):       
        query="""
          PREFIX nyon: <https://w3id.org/def/NyOn#>
          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
          select distinct ?respondent where
          {
            ?case nyon:hasParty ?party.
            ?party rdfs:type nyon:Respondent;
                   rdfs:label ?respondent.
          }
        """ 
        self.sparql.setQuery(query)
        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
           
        all_respondent = []
      #   print(results)
        for result in results["results"]["bindings"]:
              all_respondent.append( result["respondent"]["value"])
             
        return all_respondent 

   def advance_search_and(self,petitionerName,respondentName,judgeName,courtName,appealno,date,year,yearNo,caseType,decision):   
        query="""
        PREFIX nyon: <https://w3id.org/def/NyOn#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
        select distinct ?CaseName ?date ?courtName ?type ?decision where
        {
            ?case nyon:hasParty ?party1;
                  nyon:hasParty ?party2;
                  nyon:hasCourt ?court;
                  nyon:hasCourtOfficial ?judge;
                  nyon:hasDate ?date;
                  nyon:hasYear ?year;
                  nyon:hasCaseType ?type;
                  nyon:hasCourtDecision ?deci;
                  nyon:hasCaseName ?CaseName.
            ?party1 rdfs:type nyon:Petitioner;
                    rdfs:label ?petitioner.
            ?party2 rdfs:type nyon:Respondent;
                    rdfs:label ?respondent.
            ?judge rdfs:label ?judgeName.
            ?court rdfs:label ?courtName.
            ?deci rdfs:label ?decision.
        """ 

        if appealno != "":
          query +="""
                  ?case nyon:hasAppealNo ?appeal;
                        nyon:hasCaseName ?CaseName.
                  Filter(?appeal = '""" + appealno +"""')
                  """ 
        if petitionerName != "":
           query += f"\nFILTER(?petitioner = '{petitionerName}'@en)"
        if respondentName != "":
           query += f"\nFILTER(?respondent = '{respondentName}'@en)"
        if judgeName != "":
           query += f"\nFILTER(?judgeName = '{judgeName}'@en)"
        if courtName != "":
           query += f"\nFILTER(?courtName = '{courtName}'@en)"
        if date != "":
           date_s = datetime.datetime.strptime(date, "%Y-%m-%d") 
           date_string = date_s.strftime("%d/%m/%Y")
           query += f"\nFILTER(?date = '{date_string}')"
        if year != "":
          query += f"\nFILTER(?year = '{year}')"
        if yearNo != "":
           query+=f"\nFILTER(xsd:integer(?year) > (YEAR(NOW())-{yearNo}))"
        if caseType != "":
          if caseType == "civil":  
           query += f"\nFILTER(?type = nyon:Civil)"
          if caseType == "criminal":  
           query += f"\nFILTER(?type = nyon:Criminal)"
        if decision != "":
           query += f"\nFILTER(?decision = '{decision}'@en)"
           
        query += "\n}"

        print(query)
        self.sparql.setQuery(query)        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        
        casenames = []
        for result in results["results"]["bindings"]:
              casenames.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "courtName": result["courtName"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
                
        return casenames
      
   def advance_search_or(self,petitionerName,respondentName,judgeName,courtName,appealno,date,year,yearNo,caseType,decision):   
        query="""
        PREFIX nyon: <https://w3id.org/def/NyOn#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        select distinct ?CaseName ?date ?courtName ?type ?decision where
{
        { 
        }
        """

        if petitionerName != "":
          query += """
union
{
   ?case nyon:hasParty ?party1;
         nyon:hasCaseName ?CaseName;
         nyon:hasDate ?date;
         nyon:hasCourt ?court;
         nyon:hasCaseType ?type;
         nyon:hasCourtDecision ?deci.
   ?court rdfs:label ?courtName.
   ?deci rdfs:label ?decision.
   ?party1 rdfs:type nyon:Petitioner;
           rdfs:label ?petitioner.
   Filter(?petitioner = '""" + petitionerName +"""'@en)
}
"""
        if respondentName != "":
          query += """
union
{
      ?case nyon:hasParty ?party2;
         nyon:hasCaseName ?CaseName;
         nyon:hasDate ?date;
         nyon:hasCourt ?court;
         nyon:hasCaseType ?type;
         nyon:hasCourtDecision ?deci.
      ?court rdfs:label ?courtName.
      ?deci rdfs:label ?decision.
      ?party2 rdfs:type nyon:Respondent;
              rdfs:label ?respondent.
      Filter(?respondent = '""" + respondentName +"""'@en)
}
"""
        if judgeName != "":
          query += """
union
{ 
      ?case nyon:hasCourtOfficial ?judge;
         nyon:hasCaseName ?CaseName;
         nyon:hasDate ?date;
         nyon:hasCourt ?court;
         nyon:hasCaseType ?type;
         nyon:hasCourtDecision ?deci.
      ?court rdfs:label ?courtName.
      ?deci rdfs:label ?decision.
      ?judge rdfs:label ?judgeName.    
      Filter(?judgeName = '""" + judgeName +"""'@en)
}
"""
        if courtName != "":
          query += """
union
{    
      ?case nyon:hasCourt ?court;
         nyon:hasCaseName ?CaseName;
         nyon:hasDate ?date;         
         nyon:hasCaseType ?type;
         nyon:hasCourtDecision ?deci.
      ?court rdfs:label ?courtName.
      ?deci rdfs:label ?decision.
      Filter(?courtName = '""" + courtName +"""'@en)   
}
"""
        if appealno != "":
          query += """
union
{     
      ?case nyon:hasAppealNo ?appeal;
         nyon:hasCaseName ?CaseName;
         nyon:hasCourt ?court;         
         nyon:hasDate ?date;         
         nyon:hasCaseType ?type;
         nyon:hasCourtDecision ?deci.
      ?court rdfs:label ?courtName.
      ?deci rdfs:label ?decision.
      Filter(?appeal = '""" + appealno +"""')
}
""" 
        if date != "":
          date_s = datetime.datetime.strptime(date, "%Y-%m-%d") 
          date_string = date_s.strftime("%d/%m/%Y")
          query += """
      union
      {
         ?case nyon:hasDate ?date;  
            nyon:hasCaseName ?CaseName;  
            nyon:hasCourt ?court;                         
            nyon:hasCaseType ?type;
            nyon:hasCourtDecision ?deci.
         ?court rdfs:label ?courtName.
         ?deci rdfs:label ?decision.
         Filter(?date ='""" + date_string +"""')          
      } 
                  """ 
        if year != "":
          query += """
      union
      {
         ?case nyon:hasYear ?year;
            nyon:hasCaseName ?CaseName; 
            nyon:hasCourt ?court;    
            nyon:hasDate ?date;                         
            nyon:hasCaseType ?type;
            nyon:hasCourtDecision ?deci.
         ?court rdfs:label ?courtName.
         ?deci rdfs:label ?decision.
         Filter(?year='""" + year +"""')          
      }  
                  """ 
        if yearNo != "":
           query+="""
         union
         {
         ?case nyon:hasYear ?year;           
            nyon:hasCaseName ?CaseName; 
            nyon:hasCourt ?court;
            nyon:hasDate ?date;                 
            nyon:hasCaseType ?type;
            nyon:hasCourtDecision ?deci.
         ?court rdfs:label ?courtName.
         ?deci rdfs:label ?decision.
         FILTER(xsd:integer(?year) > (YEAR(NOW())-"""+yearNo+"""))        
         }  
                  """ 
        if caseType != "":
          if caseType == "civil":  
           query += """
         union
         {
         ?case nyon:hasCaseType nyon:Civil;          
            nyon:hasCaseName ?CaseName; 
            nyon:hasCourt ?court;   
            nyon:hasDate ?date;              
            nyon:hasCaseType ?type;
            nyon:hasCourtDecision ?deci.
         ?court rdfs:label ?courtName.
         ?deci rdfs:label ?decision.
         }  
                  """ 
          if caseType == "criminal":  
           query +="""
         union
         {
         ?case nyon:hasCaseType nyon:Criminal;          
            nyon:hasCaseName ?CaseName; 
            nyon:hasCourt ?court;   
            nyon:hasDate ?date;              
            nyon:hasCaseType ?type;
            nyon:hasCourtDecision ?deci.
         ?court rdfs:label ?courtName.
         ?deci rdfs:label ?decision.         
         }  
                  """  
        if decision != "":
           query += """
         union
         {
         ?case nyon:hasCourtDecision ?deci;         
            nyon:hasCaseName ?CaseName; 
            nyon:hasCourt ?court;   
            nyon:hasDate ?date;              
            nyon:hasCaseType ?type.
         ?court rdfs:label ?courtName.
         ?deci rdfs:label ?decision.
         FILTER(?decision = '"""+decision+"""'@en)
         }  
                  """  
        query += "\n}"

        print(query)
        self.sparql.setQuery(query)        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        print("check by yogesh")
        print(results)
        
        casenames = []
        for result in results["results"]["bindings"]:
            if "CaseName" in result:
              casenames.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "courtName": result["courtName"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
      
        return casenames  

   def case_details(self,case_name):       
         query="""
         # list all the information of a particular case
            PREFIX nyon: <https://w3id.org/def/NyOn#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            select ?date ?court ?petitioner ?respondent ?decision ?author ?caseno ?appeal ?judges where
            {
             {
               ?case nyon:hasCaseName  '""" + case_name+"""'@en;
                     nyon:hasDate ?date;
                     nyon:hasCourt ?Cot;
                     nyon:hasCourtDecision ?Deci;
                     nyon:hasParty ?Party1;
                     nyon:hasParty ?Party2.
               ?Cot rdfs:label ?court.
               ?Deci rdfs:label ?decision.
               ?Party1 rdfs:type nyon:Petitioner;
                       rdfs:label ?petitioner.
               ?Party2 rdfs:type nyon:Respondent;
                       rdfs:label ?respondent.
               optional{
                      ?case nyon:hasCaseName  '""" + case_name+"""'@en;
                            nyon:hasAuthor ?case_author.
                      ?case_author rdfs:label ?author.
                       }
               optional{
                     ?case nyon:hasCaseName  '""" + case_name+"""'@en;             
                           nyon:hasCaseNo ?caseno.                    
                       }
               optional{
                      ?case nyon:hasCaseName  '""" + case_name+"""'@en;
                            nyon:hasAppealNo ?appeal.
                       }
             }
             union{
                ?case nyon:hasCaseName  '""" + case_name+"""'@en;
                      nyon:hasCourtOfficial ?judge.
                ?judge rdfs:label ?judges.
             }
            }
        """
 
         #   print(query)
         self.sparql.setQuery(query)        
         self.sparql.setReturnFormat(JSON)
         results = self.sparql.query().convert()

         case = []
         for result in results["results"]["bindings"]:
            case_dict = {}
            if "date" in result:
               case_dict["date"] = result["date"]["value"]
            if "court" in result:
               case_dict["court"] = result["court"]["value"]
            if "petitioner" in result:
               case_dict["petitioner"] = result["petitioner"]["value"]
            if "respondent" in result:
               case_dict["respondent"] = result["respondent"]["value"]
            if "decision" in result:
               case_dict["decision"] = result["decision"]["value"]
            if "author" in result:
               case_dict["author"] = result["author"]["value"]
            if "caseno" in result:
               case_dict["caseno"] = result["caseno"]["value"]
            if "appeal" in result:
               case_dict["appeal"] = result["appeal"]["value"]
            if "judges" in result:
               case_dict["judges"] = result["judges"]["value"]
            case.append(case_dict)

         return case

   # def case_id(self,name):       
   #      query="""
   #      PREFIX nyon: <https://w3id.org/def/NyOn#>
   #      select ?case where
   #      {
   #         ?case nyon:hasCaseName '""" + name+"""'@en.
   #      }
   #      """ 
   #      #   print(query)
   #      self.sparql.setQuery(query)        
   #      self.sparql.setReturnFormat(JSON)
   #      results = self.sparql.query().convert()

   #      caseid = []
   #      for result in results["results"]["bindings"]:
   #            caseid.append( result["case"]["value"])
                
   #      return caseid
    
   def case_info(self,name):       
        query="""
PREFIX nyon: <https://w3id.org/def/NyOn#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

select ?petitioner ?respondent ?date ?courtName ?type ?caseNo ?decision ?juridiction ?authorName ?judgeName ?cites ?factsLabel ?provision ?statute where 
{
  {
    ?case nyon:hasCaseName  '""" + name+"""'@en;
          nyon:hasParty ?party1;
          nyon:hasParty ?party2;
          nyon:hasDate ?date;
          nyon:hasCaseType ?casetype;
          nyon:hasCourtDecision ?deci.    
    ?party1 rdfs:type nyon:Petitioner;
	       rdfs:label ?petitioner .
    ?party2 rdfs:type nyon:Respondent;
	       rdfs:label ?respondent.
    ?casetype rdfs:label ?type.
    ?deci rdfs:label ?decision.

   optional
   {
      ?case nyon:hasCaseName  '""" + name+"""'@en;
            nyon:hasJurisdiction ?juri.
      ?juri rdfs:label ?juridiction.
   }
   optional
   {
      ?case nyon:hasCaseName  '""" + name+"""'@en;
            nyon:hasAuthor ?author.
      ?author rdfs:type nyon:Author;
	          rdfs:label ?authorName.
   }
   optional
   {
      ?case nyon:hasCaseName  '""" + name+"""'@en;
            nyon:hasCaseNo ?caseNo.
   }
   optional
   {
      ?case nyon:hasCaseName  '""" + name+"""'@en;
            nyon:hasCourt ?court.
       ?court rdfs:label ?courtName.
   }
  }
union
  {
      ?case nyon:hasCaseName  '""" + name+"""'@en;
            nyon:hasCourtOfficial ?judges.
      ?judges rdfs:label ?judgeName.
  }
union
  {
      ?case nyon:hasCaseName  '""" + name+"""'@en;
            nyon:equalcite ?cites.
  }
union
  {
     ?case nyon:hasCaseName  '""" + name+"""'@en;
           nyon:hasFact ?facts.
     ?facts nyon:hasProvision ?section.
     ?section nyon:hasProvision ?provision;
            nyon:hasStatute ?statute.
      
  }
union
{
      ?case nyon:hasCaseName  '""" + name+"""'@en;
            nyon:hasFact ?facts.
      ?facts rdfs:label ?factsLabel;
             nyon:hasStartIndex ?start.
}
}
order by ?start
        """ 
        print(query)
        self.sparql.setQuery(query)        
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        caseinfo = []
        for result in results["results"]["bindings"]:
         info = {}
         if "petitioner" in result:
          info["petitioner"] = result["petitioner"]["value"]
         if "respondent" in result:
          info["respondent"] = result["respondent"]["value"]
         if "date" in result:
          info["date"] = result["date"]["value"]
         if "courtName" in result:
          info["courtName"] = result["courtName"]["value"]
         if "type" in result:
          info["type"] = result["type"]["value"]
         if "caseNo" in result:
          info["caseNo"] = result["caseNo"]["value"]
         if "decision" in result:
          info["decision"] = result["decision"]["value"]
         if "juridiction" in result:
          info["juridiction"] = result["juridiction"]["value"]
         if "authorName" in result:
          info["authorName"] = result["authorName"]["value"]
         if "judgeName" in result:
          info["judgeName"] = result["judgeName"]["value"]
         if "cites" in result:
          info["cites"] = result["cites"]["value"]
         if "factsLabel" in result:
          info["factsLabel"] = result["factsLabel"]["value"]
         if "provision" in result:
          info["provision"] = result["provision"]["value"]
         if "statute" in result:
          info["statute"] = result["statute"]["value"]
         caseinfo.append(info)
         
        return caseinfo


   def facts_for_case(self,name):       
      query="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT distinct ?factsLabel  WHERE 
      {
         ?case nyon:hasCaseName  '""" + name+"""'@en;
               nyon:hasFact ?facts.
         ?facts rdfs:label ?factsLabel;
                nyon:hasStartIndex ?start.               
      }         
      order by ?start      
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      fact = []
      for result in results["results"]["bindings"]:
           fact.append( result["factsLabel"]["value"])
      return fact
    

   def allcase_facts(self):       
      query="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT distinct ?CaseName ?factsLabel  WHERE 
      {
         ?case nyon:hasCaseName  ?CaseName;
               nyon:hasFact ?facts.
         ?facts rdfs:label ?factsLabel;
                nyon:hasStartIndex ?start.               
      }         
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      fact = []
      for result in results["results"]["bindings"]:
           fact.append({
            "CaseName": result["CaseName"]["value"],
            "factsLabel": result["factsLabel"]["value"]
            })
      res={}
      for i in fact:
        if i['CaseName'] in res:
          res[i['CaseName']].append(i['factsLabel'])
        else:
          res[i['CaseName']]= [i['factsLabel']]
      return res
    

   def section_for_fact(self,name):       
      query_t="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

      SELECT distinct ?provision ?statute WHERE 
      {  
          ?facts rdfs:label ?factLabel;
                 nyon:hasProvision ?section.   
          ?section nyon:hasProvision ?provision;
                   nyon:hasStatute ?statute. 
           FILTER(?factLabel = ?name)    
      }
      """  

      query = query_t.replace("?name", "'" + name.replace("'", "\\'") + "'@en")
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      section = []
      for result in results["results"]["bindings"]:
           section.append({
            "provision": result["provision"]["value"],
            "statute": result["statute"]["value"]
            })
      return section


   def last_year(self,year):       
      query="""  
      # List all cases of the last some years
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>      
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      select ?CaseName ?date ?court ?type ?decision where
      {
         ?case nyon:hasYear ?year;
               nyon:hasCaseName ?CaseName;
               nyon:hasDate ?date;
               nyon:hasCourt ?courts;
               nyon:hasCaseType ?type;
               nyon:hasCourtDecision ?deci.
         ?courts rdfs:label ?court.
         ?deci rdfs:label ?decision.
         FILTER(xsd:integer(?year) > (YEAR(NOW())-""" + year+"""))
      } 
      """ 
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      case = []
      for result in results["results"]["bindings"]:
         case.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "court": result["court"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
      return case

   def last_year_peti(self,year,petitionerName,respondentName,judgeName,courtName,caseType,decision):       
      query="""  
      # List all cases of the last some years where person x is a petitioner?
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>    
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      select distinct ?CaseName ?date ?court ?type ?decision where
      {
         ?Case nyon:hasParty ?party1;
               nyon:hasParty ?party2;
               nyon:hasCourtOfficial ?judge;
               nyon:hasYear ?year; 
               nyon:hasCaseName ?CaseName;
               nyon:hasDate ?date;
               nyon:hasCourt ?courts;
               nyon:hasCaseType ?type;
               nyon:hasCourtDecision ?deci.
         ?party1 rdfs:type nyon:Petitioner;
                 rdfs:label ?petitioner.
         ?party2 rdfs:type nyon:Respondent;
                rdfs:label ?respondent.
         ?judge rdfs:label ?judgeName.
         ?courts rdfs:label ?court.
         ?deci rdfs:label ?decision.

         FILTER(xsd:integer(?year) > (YEAR(NOW())-""" + year+"""))
      """

      if petitionerName != "":
           query += f"\nFILTER(?petitioner = '{petitionerName}'@en)"
      if respondentName != "":
           query += f"\nFILTER(?respondent = '{respondentName}'@en)"
      if judgeName != "":
           query += f"\nFILTER(?judgeName = '{judgeName}'@en)"
      if courtName != "":
           query += f"\nFILTER(?courtName = '{courtName}'@en)"
      if caseType != "":
         if caseType == "civil":  
           query += f"\nFILTER(?type = nyon:Civil)"
         if caseType == "criminal":  
           query += f"\nFILTER(?type = nyon:Criminal)"
      if decision != "":
           query += f"\nFILTER(?decision = '{decision}'@en)"

      query += "\n}" 
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      case = []
      for result in results["results"]["bindings"]:
         case.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "court": result["court"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
      return case


   def last_year(self,year):       
      query="""  
      # List all cases of the last some years
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>      
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      select ?CaseName ?date ?court ?type ?decision where
      {
         ?case nyon:hasYear ?year;
               nyon:hasCaseName ?CaseName;
               nyon:hasDate ?date;
               nyon:hasCourt ?courts;
               nyon:hasCaseType ?type;
               nyon:hasCourtDecision ?deci.
         ?courts rdfs:label ?court.
         ?deci rdfs:label ?decision.
         FILTER(xsd:integer(?year) > (YEAR(NOW())-""" + year+"""))
      } 
      """ 
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      case = []
      for result in results["results"]["bindings"]:
         case.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "court": result["court"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
      return case

   def all_cases(self):       
      query="""  
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>    
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      select distinct ?CaseName ?date ?court ?type ?decision where
      {
         ?Case nyon:hasCaseName ?CaseName;
               nyon:hasDate ?date;
               nyon:hasCourt ?courts;
               nyon:hasCaseType ?type;
               nyon:hasCourtDecision ?deci.
         ?courts rdfs:label ?court.
         ?deci rdfs:label ?decision.
       }
      """
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      case = []
      for result in results["results"]["bindings"]:
         case.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "court": result["court"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
            })
      return case





   def rlc_for_case(self,name):       
      query="""      
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?rlcLabel  WHERE 
      {
         ?case nyon:hasCaseName '""" + name+"""'@en;
               nyon:hasRLC ?rlc.
         ?rlc rdfs:label ?rlcLabel;
                nyon:hasStartIndex ?start.               
      }         
      order by ?start 
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      rlc = []
      for result in results["results"]["bindings"]:
           rlc.append( result["rlcLabel"]["value"])
      return rlc
    

   def allcase_rlc(self):       
      query="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT distinct ?CaseName ?rlcLabel  WHERE 
      {
         ?case nyon:hasCaseName  ?CaseName;
               nyon:hasRLC ?rlc.
         ?rlc rdfs:label ?rlcLabel;
                nyon:hasStartIndex ?start.               
      }
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      rlc = []
      for result in results["results"]["bindings"]:
           rlc.append({
            "CaseName": result["CaseName"]["value"],
            "rlcLabel": result["rlcLabel"]["value"]
            })
      res={}
      for i in rlc:
        if i['CaseName'] in res:
          res[i['CaseName']].append(i['rlcLabel'])
        else:
          res[i['CaseName']]= [i['rlcLabel']]
      return res
    

   def section_for_rlc(self,name):       
      query_t="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

      SELECT distinct ?provision ?statute WHERE 
      {  
          ?rlc rdfs:label ?name;
                 nyon:hasProvision ?section.   
          ?section nyon:hasProvision ?provision;
                   nyon:hasStatute ?statute.     
          FILTER(?factLabel = ?name)    
      }
      """  

      query = query_t.replace("?name", "'" + name.replace("'", "\\'") + "'@en") 
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      section = []
      for result in results["results"]["bindings"]:
           section.append({
            "provision": result["provision"]["value"],
            "statute": result["statute"]["value"]
            })
      return section
   

   def ana_for_case(self,name):       
      query="""      
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?anaLabel  WHERE 
      {
         ?case nyon:hasCaseName '""" + name+"""'@en;
               nyon:hasAnalysis ?ana.
         ?ana rdfs:label ?anaLabel;
                nyon:hasStartIndex ?start.               
      }         
      order by ?start 
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      ana = []
      for result in results["results"]["bindings"]:
           ana.append( result["anaLabel"]["value"])
      return ana
    

   def allcase_ana(self):       
      query="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT distinct ?CaseName ?anaLabel  WHERE 
      {
         ?case nyon:hasCaseName  ?CaseName;
               nyon:hasAnalysis ?ana.
         ?ana rdfs:label ?anaLabel;
                nyon:hasStartIndex ?start.               
      }
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      ana = []
      for result in results["results"]["bindings"]:
           ana.append({
            "CaseName": result["CaseName"]["value"],
            "anaLabel": result["anaLabel"]["value"]
            })
      res={}
      for i in ana:
        if i['CaseName'] in res:
          res[i['CaseName']].append(i['anaLabel'])
        else:
          res[i['CaseName']]= [i['anaLabel']]
      return res
    

   def section_for_ana(self,name):       
      query_t="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

      SELECT distinct ?provision ?statute WHERE 
      {  
          ?ana rdfs:label ?name;
                 nyon:hasProvision ?section.   
          ?section nyon:hasProvision ?provision;
                   nyon:hasStatute ?statute.     
          FILTER(?factLabel = ?name)    
      }
      """  

      query = query_t.replace("?name", "'" + name.replace("'", "\\'") + "'@en")
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      section = []
      for result in results["results"]["bindings"]:
           section.append({
            "provision": result["provision"]["value"],
            "statute": result["statute"]["value"]
            })
      return section
   

   def rpc_for_case(self,name):       
      query="""      
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?rpcLabel  WHERE 
      {
         ?case nyon:hasCaseName '""" + name+"""'@en;
               nyon:hasRPC ?rpc.
         ?rpc rdfs:label ?rpcLabel;
                nyon:hasStartIndex ?start.               
      }         
      order by ?start 
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      rpc = []
      for result in results["results"]["bindings"]:
           rpc.append( result["rpcLabel"]["value"])
      return rpc
    

   def allcase_rpc(self):       
      query="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT distinct ?CaseName ?rpcLabel  WHERE 
      {
         ?case nyon:hasCaseName  ?CaseName;
               nyon:hasRPC ?rpc.
         ?rpc rdfs:label ?rpcLabel;
                nyon:hasStartIndex ?start.               
      }
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      rpc = []
      for result in results["results"]["bindings"]:
           rpc.append({
            "CaseName": result["CaseName"]["value"],
            "rpcLabel": result["rpcLabel"]["value"]
            })
      res={}
      for i in rpc:
        if i['CaseName'] in res:
          res[i['CaseName']].append(i['rpcLabel'])
        else:
          res[i['CaseName']]= [i['rpcLabel']]
      return res
    

   def section_for_rpc(self,name):       
      query_t="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

      SELECT distinct ?provision ?statute WHERE 
      {  
          ?rpc rdfs:label ?name;
                 nyon:hasProvision ?section.   
          ?section nyon:hasProvision ?provision;
                   nyon:hasStatute ?statute.     
      FILTER(?factLabel = ?name)    
      }
      """  

      query = query_t.replace("?name", "'" + name.replace("'", "\\'") + "'@en") 
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      section = []
      for result in results["results"]["bindings"]:
           section.append({
            "provision": result["provision"]["value"],
            "statute": result["statute"]["value"]
            })
      return section
   

   def ratio_for_case(self,name):       
      query="""      
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?ratioLabel  WHERE 
      {
         ?case nyon:hasCaseName '""" + name+"""'@en;
               nyon:hasRatio ?ratio.
         ?ratio rdfs:label ?ratioLabel;
                nyon:hasStartIndex ?start.               
      }         
      order by ?start 
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      ratio = []
      for result in results["results"]["bindings"]:
           ratio.append( result["ratioLabel"]["value"])
      return ratio
    

   def allcase_ratio(self):       
      query="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT distinct ?CaseName ?ratioLabel  WHERE 
      {
         ?case nyon:hasCaseName  ?CaseName;
               nyon:hasRatio ?ratio.
         ?ratio rdfs:label ?ratioLabel;
                nyon:hasStartIndex ?start.               
      }
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      ratio = []
      for result in results["results"]["bindings"]:
           ratio.append({
            "CaseName": result["CaseName"]["value"],
            "ratioLabel": result["ratioLabel"]["value"]
            })
      res={}
      for i in ratio:
        if i['CaseName'] in res:
          res[i['CaseName']].append(i['ratioLabel'])
        else:
          res[i['CaseName']]= [i['ratioLabel']]
      return res
    

   def section_for_ratio(self,name):       
      query_t="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

      SELECT distinct ?provision ?statute WHERE 
      {  
          ?ratio rdfs:label ?name;
                 nyon:hasProvision ?section.   
          ?section nyon:hasProvision ?provision;
                   nyon:hasStatute ?statute.     
      FILTER(?factLabel = ?name)    
      }
      """  

      query = query_t.replace("?name", "'" + name.replace("'", "\\'") + "'@en")
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      section = []
      for result in results["results"]["bindings"]:
           section.append({
            "provision": result["provision"]["value"],
            "statute": result["statute"]["value"]
            })
      return section
   

   def prerel_for_case(self,name):       
      query="""      
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?prerelLabel  WHERE 
      {
         ?case nyon:hasCaseName '""" + name+"""'@en;
               nyon:hasPreRelied ?prerel.
         ?prerel rdfs:label ?prerelLabel;
                nyon:hasStartIndex ?start.               
      }         
      order by ?start 
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      prerel = []
      for result in results["results"]["bindings"]:
           prerel.append( result["prerelLabel"]["value"])
      return prerel
    

   def allcase_prerel(self):       
      query="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT distinct ?CaseName ?prerelLabel  WHERE 
      {
         ?case nyon:hasCaseName  ?CaseName;
               nyon:hasPreRelied ?prerel.
         ?prerel rdfs:label ?prerelLabel;
                nyon:hasStartIndex ?start.               
      }
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      prerel = []
      for result in results["results"]["bindings"]:
           prerel.append({
            "CaseName": result["CaseName"]["value"],
            "prerelLabel": result["prerelLabel"]["value"]
            })
      res={}
      for i in prerel:
        if i['CaseName'] in res:
          res[i['CaseName']].append(i['prerelLabel'])
        else:
          res[i['CaseName']]= [i['prerelLabel']]
      return res
    

   def section_for_prerel(self,name):       
      query_t="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

      SELECT distinct ?provision ?statute WHERE 
      {  
          ?prerel rdfs:label ?name;
                 nyon:hasProvision ?section.   
          ?section nyon:hasProvision ?provision;
                   nyon:hasStatute ?statute.     
          FILTER(?factLabel = ?name)    
      }
      """  

      query = query_t.replace("?name", "'" + name.replace("'", "\\'") + "'@en")
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      section = []
      for result in results["results"]["bindings"]:
           section.append({
            "provision": result["provision"]["value"],
            "statute": result["statute"]["value"]
            })
      return section
   

   def issue_for_case(self,name):       
      query="""      
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?issueLabel  WHERE 
      {
         ?case nyon:hasCaseName '""" + name+"""'@en;
               nyon:hasIssue ?issue.
         ?issue rdfs:label ?issueLabel;
                nyon:hasStartIndex ?start.               
      }         
      order by ?start 
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      issue = []
      for result in results["results"]["bindings"]:
           issue.append( result["issueLabel"]["value"])
      return issue
    

   def allcase_issue(self):       
      query="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT distinct ?CaseName ?issueLabel  WHERE 
      {
         ?case nyon:hasCaseName  ?CaseName;
               nyon:hasIssue ?issue.
         ?issue rdfs:label ?issueLabel;
                nyon:hasStartIndex ?start.               
      }
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      issue = []
      for result in results["results"]["bindings"]:
           issue.append({
            "CaseName": result["CaseName"]["value"],
            "issueLabel": result["issueLabel"]["value"]
            })
      res={}
      for i in issue:
        if i['CaseName'] in res:
          res[i['CaseName']].append(i['issueLabel'])
        else:
          res[i['CaseName']]= [i['issueLabel']]
      return res
    

   def section_for_issue(self,name):       
      query_t="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

      SELECT distinct ?provision ?statute WHERE 
      {  
          ?issue rdfs:label ?name;
                 nyon:hasProvision ?section.   
          ?section nyon:hasProvision ?provision;
                   nyon:hasStatute ?statute.     
          FILTER(?factLabel = ?name)    
      }
      """  

      query = query_t.replace("?name", "'" + name.replace("'", "\\'") + "'@en")  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      section = []
      for result in results["results"]["bindings"]:
           section.append({
            "provision": result["provision"]["value"],
            "statute": result["statute"]["value"]
            })
      return section


   def prenotrel_for_case(self,name):       
      query="""      
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?prenotrelLabel  WHERE 
      {
         ?case nyon:hasCaseName '""" + name+"""'@en;
               nyon:hasPreNotRelied ?prenotrel.
         ?prenotrel rdfs:label ?prenotrelLabel;
                nyon:hasStartIndex ?start.               
      }         
      order by ?start 
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      prenotrel = []
      for result in results["results"]["bindings"]:
           prenotrel.append( result["prenotrelLabel"]["value"])
      return prenotrel
    

   def allcase_prenotrel(self):       
      query="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT distinct ?CaseName ?prenotrelLabel  WHERE 
      {
         ?case nyon:hasCaseName  ?CaseName;
               nyon:hasPreNotRelied ?prenotrel.
         ?prenotrel rdfs:label ?prenotrelLabel;
                nyon:hasStartIndex ?start.               
      }
      """  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      prenotrel = []
      for result in results["results"]["bindings"]:
           prenotrel.append({
            "CaseName": result["CaseName"]["value"],
            "prenotrelLabel": result["prenotrelLabel"]["value"]
            })
      res={}
      for i in prenotrel:
        if i['CaseName'] in res:
          res[i['CaseName']].append(i['prenotrelLabel'])
        else:
          res[i['CaseName']]= [i['prenotrelLabel']]
      return res
    

   def section_for_prerel(self,name):       
      query_t="""  
      PREFIX nyon: <https://w3id.org/def/NyOn#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

      SELECT distinct ?provision ?statute WHERE 
      {  
          ?prenotrel rdfs:label ?name;
                 nyon:hasProvision ?section.   
          ?section nyon:hasProvision ?provision;
                   nyon:hasStatute ?statute.     
          FILTER(?factLabel = ?name)    
      }
      """  

      query = query_t.replace("?name", "'" + name.replace("'", "\\'") + "'@en")  
    
      print(query)
      
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      section = []
      for result in results["results"]["bindings"]:
           section.append({
            "provision": result["provision"]["value"],
            "statute": result["statute"]["value"]
            })
      return section


# code added on 22march2025 in order to allow search cases by bench name :by yogeshjat

   def casename_searchbybench(self, bench_name):
      query = f"""
         PREFIX nyon: <https://w3id.org/def/NyOn#>
         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

         SELECT ?CaseName ?date ?court ?type ?decision
         WHERE {{
               ?case nyon:hasCourtOfficial ?official.
               ?official rdfs:label ?benchName.

               FILTER(CONTAINS(LCASE(?benchName), LCASE("{bench_name}")))

               ?case nyon:hasCaseName ?CaseName;
                     nyon:hasDate ?date;
                     nyon:hasCourt ?courtEntity;
                     nyon:hasCaseType ?type;
                     nyon:hasCourtDecision ?decisionEntity.

               ?courtEntity rdfs:label ?court.
               ?decisionEntity rdfs:label ?decision.
         }}
      """
      print(query)  # Debugging: Print the query to verify it's formatted correctly

    # Execute the SPARQL query
      self.sparql.setQuery(query)        
      self.sparql.setReturnFormat(JSON)
      results = self.sparql.query().convert()

      print("Result is:")
      print(results)  # Debugging: Print raw results

    # Extract results into a list of dictionaries
      case = []
      for result in results["results"]["bindings"]:
         case.append({
            "CaseName": result["CaseName"]["value"],
            "date": result["date"]["value"],
            "court": result["court"]["value"],
            "type": result["type"]["value"],
            "decision": result["decision"]["value"],
         })
    
      return case
