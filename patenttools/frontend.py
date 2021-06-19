# A Flask-based web frontend for PatentTools.

# Import the necessary modules and instantiate the app
from flask import Flask, render_template, request
from lookup import USPTOLookup
from distiller import TextDistiller
from requests.exceptions import ConnectionError

app = Flask(__name__)

# Define routes
@app.route("/")
def build_search():
    display = render_template("search_form.html")  
    return display

@app.route("/results", methods = ["POST", "GET"])
def display_results():
    
    # This route should be accessed only from the search form at /.
    # If it is accessed directly via GET, provide a link to / instead.
    if request.method == "POST":
        
        # Capture the user's search parameters
        form_submission = request.form
        raw_pat_num = form_submission["raw_pat_num"]
        bigram_freq_filter = int(form_submission["bigram_freq_filter"])
        
        # If any query at all is present, try to proceed.
        if raw_pat_num != "":
            
            try:
                # Instantiate a USPTOLookup to parse basic patent information
                patent_info = USPTOLookup(raw_pat_num)
                
                if patent_info.number == "unrecognized input":
                    error = """The patent number you provided could not be interpreted.<p>
                    Please <a href = '/'>enter a new query</a>."""
                    return error
                
                # Instantiate a TextDistiller to extract bigrams
                pat_distiller = TextDistiller(" ".join(patent_info.claims) + patent_info.description)
                bigrams = pat_distiller.gen_bigrams(min_freq = bigram_freq_filter)   
                
                
                display = render_template("results.html",
                              pat_num = patent_info.number,
                              pat_title = patent_info.title,
                              pat_url = patent_info.url,
                              pat_class = patent_info.primary_class,
                              pat_assignee = patent_info.assignee,
                              pat_file_date = patent_info.filing_date,
                              pat_bigrams = bigrams,
                              wordcloud = pat_distiller.wordcloud)
                return display
            
            except ConnectionError:
                conn_err1 = "<b>Error: The USPTO server is unreachable.</b><p>"
                conn_err2 = "Please try again later."
                return conn_err1 + conn_err_2
            
            except:
                error = """An error occured.<p>
                    Please <a href = '/'>enter a new query</a>."""
                return error 

        else:
            error = """No query entered.<p>
                    Please <a href = '/'>enter a new query</a>."""
            return error 
    else:
        error = """No query entered.<p>
                    Please <a href = '/'>enter a new query</a>."""
        return error 

@app.route("/<unspecified_str>")
def handle_unknown(unspecified_str):
    error = """Invalid path.<p>Please <a href = '/'>enter a new query</a>."""
    return error

# Run the app
if __name__ == "__main__":
  app.run()