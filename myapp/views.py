from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection, DatabaseError


# Create your views here.
def dashboard(request):
    return render(request, "myapp/dashboard.html")


def showdata(request):
    return render(request, 'myapp/showdata.html', {})


def custom_query(request):
    # Define your SQL query using explicit JOIN syntax for better readability
    query = """
        SELECT fld_fname, fld_lname, ext_no, fld_mobile, fld_email, d.dept_name
        FROM tbl_addressbook a
        JOIN department d ON a.dept_code = d.dept_code
    """
    try:
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            return render(request, "myapp/showdata.html", {"records": data})


    except DatabaseError as db_error:
        print(f"Database error: {db_error}")
        return render(request, "myapp/error.html", {"error": {db_error}})
    
    except Exception as e:
        print(f"Error: {e}")
        return render(request, "myapp/error.html", {"error": str(e)})



def account_details(request):
    # Get query parameters with defaults
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "").strip()
   

    search_value_with_wildcards = f"%{search_value.lower()}%"
    
    try:
        with connection.cursor() as cursor:
            # Get total records
            cursor.execute("select count(*) from vw_mbl_addbook")
            total_records = cursor.fetchone()[0]
            #print(total_records)

            # Prepare the search query if there is a search value
            search_query, params = prepare_search_query(search_value, search_value_with_wildcards)

            # Final query with pagination
            final_query = f"""
                select * from vw_mbl_addbook {search_query}
                LIMIT %s OFFSET %s
            """
            params += [length, start]  # Append pagination parameters
            
            # Debugging information
            print("SQL Query:", final_query)
            print("Parameters:", params)
            
            # Execute the query
            cursor.execute(final_query, params)
            rows = cursor.fetchall()

            # Prepare data for response
            data = extract_data(rows)

            # Construct the response
            response = {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records if not search_value else len(data),  # Adjust if searching
                "data": data,
            }

            return JsonResponse(response)

    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({"error": str(e)}, status=500)
    
def prepare_search_query(search_value, search_value_with_wildcards):
    """Prepare the search SQL and parameters."""
    if not search_value:
        return "", []  # No search value means no WHERE clause

    
    fields = ['fld_fname', 'fld_lname', 'fld_email', 'fld_mobile']
    search_conditions = " OR ".join([f"LOWER({field}) LIKE LOWER(%s)" for field in fields])
    
    search_query = f"WHERE {search_conditions}"
    params = [search_value_with_wildcards] * len(fields)
    return search_query, params

def extract_data(rows):
    """Extract relevant fields from the database rows."""
    data = []
    for row in rows:
        try:
            # Adjust indices according to your actual row structure
            data.append([row[0], row[1], row[2], row[3], row[4], row[5]])  
        except IndexError as e:
            print(f"Error processing row {row}: {e}")
    return data

def account_view(request):
    return render(request, "myapp/account.html")

