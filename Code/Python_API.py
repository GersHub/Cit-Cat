from pybliometrics.scopus import AbstractRetrieval
from pybliometrics.scopus import CitationOverview
from pybliometrics.scopus import ScopusSearch
import opencitingpy
import pandas as pd
import numpy as np

client = opencitingpy.client.Client()
years = [2018, 2021]
min_citations = 20
key = ['Smart Energy', 'Modelling']

def get_papers_per_keywords(key):
    keys= 'KEY(' + ' AND '.join(key) + ')'
    result = ScopusSearch(keys)
    df = pd.DataFrame(pd.DataFrame(result.results))
    df["year"] = np.nan # remove this. 
    df['coverDate']= pd.to_datetime(df['coverDate'], format='%Y-%m-%d')
    df['year'] = pd.DatetimeIndex(df['coverDate']).year
    return df
    

def select_papers_per_year(papers, years):
    selected_papers = papers[papers['year'].between(years[0], years[1])]  
    return selected_papers
    


def get_paper_that_cite(target_paper):
    metadata = client.get_metadata(target_paper)     
    try:
        citin_papers = metadata[0].citation
        
    except Exception as e:
        print ("metadata empty")
        citin_papers = []
    return citin_papers    
    
    
def get_paper_with_minimum_ciations(target_paper, min_citations):
    target_paper_min_citations = target_paper[target_paper.citedby_count > min_citations]
    return target_paper_min_citations



def sample(results_frame, number):
    result_sampled = results_frame.sample(n=100)

def main():
    papers = get_papers_per_keywords(key)
    target_paper = select_papers_per_year(papers, years)
    selected_papers_cit = get_paper_with_minimum_ciations(target_paper, min_citations)
    print('number of selected papers: {}'.format(len(selected_papers_cit.index)))
    print('Paper have in total citations: {}'.format(selected_papers_cit['citedby_count'].sum()))
    
    
    
    results_frame = pd.DataFrame()
    results_frame['DOI_source'] = ''
    results_frame['DOI_citing'] = ''
    
    
    for index, row in selected_papers_cit.iterrows():
        if row['doi'] != None:
            doi = row['doi']
            title = row['title']
            authors = row['author_names']
            citing_papers = get_paper_that_cite(doi)
            if citing_papers:
                for ref in citing_papers:
                    df2 = {'DOI_source': ref, 'DOI_citing': doi}
                    results_frame = results_frame.append(df2, ignore_index = True)
            else: 
                print ("ref empgy")
            
    
    print('Fund citations: {}'.format(len(results_frame)))



if __name__=='__main__':
    main()

