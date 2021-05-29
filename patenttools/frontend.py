# A Flask-based web frontend for PatentTools.

# Import the Flask and instantiate the app
from flask import Flask, render_template, request
import lookup
app = Flask(__name__)

# Define routes
@app.route("/")
def greeting():
    display = render_template("search_form.html")  
    return display

@app.route("/results", methods = ["POST", "GET"])
def display_results():
 
    if request.method == "POST":
        form_submission = request.form
        raw_pat_num = form_submission["raw_pat_num"]
        if raw_pat_num != "":
            
            try:
                patent_info = lookup.USPTOLookup(raw_pat_num)
                
                if patent_info.number == "unrecognized input":
                    error = """The patent number you provided could not be interpreted.<p>
                    Please <a href = '/'>enter a new query</a>."""
                    return error
                
                display = render_template("results.html",
                              pat_num = patent_info.number,
                              pat_title = patent_info.title,
                              pat_url = patent_info.url,
                              pat_assignee = patent_info.assignee,
                              pat_file_date = patent_info.filing_date,
                              pat_claims = patent_info.claims)
                return display
            except requests.exceptions.ConnectionError:
                conn_err1 = "<b>Error: The USPTO server is unreachable.</b><p>"
                conn_err2 = "Please try again later."
                return conn_err1 + conn_err_2

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
    display = render_template("unknown_path.html", err_path = unspecified_str)
    return display

# Run the app
if __name__ == "__main__":
  app.run()
