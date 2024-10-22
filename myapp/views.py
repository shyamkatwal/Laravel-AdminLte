from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection


# Create your views here.
def dashboard(request):
    return render(request, "myapp/dashboard.html")


def showdata(request):
    return render(request, 'myapp/showdata.html', {})


def custom_query(request):
    try:
        query = "SELECT * FROM tbl_addressbook"
        with connection.cursor() as cursor:
            queryset = cursor.execute(query)
            data = cursor.fetchall()
            return render(request, "myapp/showdata.html", {"records": data})


    except Exception as e:
        print(e)
        return render(
            request, "myapp/error.html", context={"error": str(e)}
        )  # Render an error page if needed


def accountdetails(request):
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")  # Get the search term
     
    
    try:
        # Get total records
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM tbl_addressbook")
            total_records = cursor.fetchone()[0]

            # Prepare the search query
            search_query = ""
            params = []
            if search_value:
                search_query = "WHERE LOWER(fld_fname) LIKE LOWER(%s)"
                params.append(f"%{search_value}%")  # Add search value to parameters
                
            # Fetch user details with pagination
            query = f"""
                SELECT * FROM tbl_addressbook {search_query}
                LIMIT %s OFFSET %s
            """
            params.append(length)  # Length for LIMIT
            params.append(start)    # Start for OFFSET
            
            # Execute the query
            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Prepare data for response
            data = []
            for row in rows:
                try:
                    data.append(
                        [
                            row[1],  # Assuming row[1] is name
                            row[2],  # Assuming row[2] is position
                            row[6],  # Assuming row[3] is office
                            row[7],  # Assuming row[4] is age
                        ]
                    )
                except IndexError as e:
                    print(f"Error processing row {row}: {e}")

        # Construct the response
        response = {
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data,
        }

        return JsonResponse(response)

    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({"error": str(e)}, status=500)

def account_view(request):
    return render(request, "myapp/account.html")