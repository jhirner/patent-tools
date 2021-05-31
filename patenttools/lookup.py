# A set of tools for retrieving US patent information.
# The tools are available to instances of the USPTOLookup class.

# Import necessary modules
import re
import requests
from bs4 import BeautifulSoup


class USPTOLookup:

    """
    Instances of this class are used to retrieve and parse a patent based on 
    a user-provided patent number.
    At present, it only supports US patents.
    """
    
    def __init__(self, patent_num):
        
        # Define class variables, which will later be assigned when the 
        # parsing function is called.
        self.title = None
        self.filing_date = None
        self.assignee = None
        self.abstract = None
        self.claims = None
        self.description = None
        
        
        # Pass to a cleaner function to remove letters, punctiuation
        self.number = self.clean_num(patent_num)
        
        # If the patent number could not be interpreted, quit.
        if self.clean_num == "unrecognized input":
            quit()
        
        # Assemble the query URL & access the patent.
        url_template = """http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1
        &Sect2=HITOFF&d=PALL&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.htm&r=1&f=G&
        l=50&s1=num-goes-here.PN.&OS=PN/num-goes-here&RS=PN/num-goes-here"""
        
        self.url = re.sub(r"\s", "", url_template)
        self.url = re.sub(r"num-goes-here", self.number, self.url)
        cust_header = {"user-agent" : "Automated Python patent parsing tool, powered by requests 2.22.0"}
        patent_html = requests.get(self.url, headers = cust_header).text
        
        # pass to a parsing function to get title, abstract, claims, & description
        # self.title, self.filing_date, self.assignee, self.abstract, self.claims, self.description = 
        self.parse_us_pat(patent_html)
        
        return

    def parse_us_pat(self, patent_html):
        # This function does the heavy lifting of the Fetcher class. It uses
        # BeautifulSoup to parse the HTML patent into a title, filing date,
        # abstract, claims, and description.
        
        soup = BeautifulSoup(patent_html, "html.parser")
        
        # Check for successful patent lookup. Will need to improve this error
        # handling.
        if len(soup.find_all(string=re.compile("No patents have matched"))) > 0:
            return None
        
        try:
            # There are no labels to indicate which text is the patent's title, but
            # it is conveniently the only text written in a large font.
            self.title = self.clean_text(soup.find("font", size = "+1").text)

            self.filing_date = self.clean_text(soup.find(string = re.compile("Filed:")).find_next().text).strip()
            self.assignee = self.clean_text(soup.find(string = re.compile("Assignee:")).find_next().text).strip()
            self.abstract = self.clean_text(soup.find(string = re.compile("Abstract")).find_next().text).strip()

            # Extract the claims section by getting everything after the bolded
            # Claims header, then removing everything at or after "Description"
            claims_in_prog = soup.find("b", string = re.compile("Claims")).find_all_next(string = True)
            claims_in_prog = list(claims_in_prog)[:list(claims_in_prog).index("Description") - 1]
            self.claims = [self.clean_text(claim).strip() for claim in claims_in_prog]

            # Extract the description section in a similar fashion.
            desc_in_prog = soup.find("b", string = re.compile("Description")).find_all_next(string = True)
            desc_in_prog = [re.sub("\n", " ", desc) for desc in desc_in_prog]
            desc_in_prog = "\n\n".join(desc_in_prog)
            self.description = re.sub(r"\*", "", desc_in_prog).strip()
        except ValueError:
            pass
        
        return
        
        
    def clean_num(self, raw_patent_num):
        # In this order, remove: leading US, trailing A1 or similar, and
        # commas or unexpected other punctuation.
        
        cleaned_num = re.sub(r"US", "", raw_patent_num)
        cleaned_num = re.sub(r"[a-zA-Z]+[0-9]*", "", cleaned_num)
        cleaned_num = re.sub(r"[,.\\\!\?\#-]*", "", cleaned_num)
        cleaned_num = re.sub(r"\s+", "", cleaned_num)
        
        # Test to confirm that the user's patent number could be interpreted.
        try:
            int(cleaned_num) 
            return str(cleaned_num)
        except ValueError:
            return "unrecognized input"
            
        return str(cleaned_num)
    
    
    def clean_text(self, ugly_text):
        # This function scrubs out line breaks, extra spaces, etc.
        cleaned_text = re.sub(r"[\s]{2,}", " ", ugly_text)
        cleaned_text = re.sub(r"\n", " ", cleaned_text)
        return cleaned_text