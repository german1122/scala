import requests
import json

def cpanel(cpanel_user, cpanel_password, cpanel_domain):
    # Your cPanel account information
    cpanel_user = "your_cpanel_username"
    cpanel_password = "your_cpanel_password"
    cpanel_domain = "your_cpanel_domain"

    # The URL for cPanel's email API
    api_url = "https://" + cpanel_domain + ":2083/json-api/listpopswithdisk?api.version=1&user=" + cpanel_user

    # Set up the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + (cpanel_user + ":" + cpanel_password).encode("base64").strip()
    }

    # Send the API request to retrieve the list of email accounts
    response = requests.get(api_url, headers=headers)

    # Check if the API request was successful
    if response.status_code == 200:
        # Load the JSON response into a dictionary
        email_accounts = json.loads(response.content)

        # A set to store the unique sender email addresses
        sender_emails = set()

        # Loop through each email account
        for email_account in email_accounts["cpanelresult"]["data"]:
            # The URL for the email account's inbox
            inbox_url = "https://" + cpanel_domain + ":2083/json-api/cpanel?cpanel_jsonapi_module=Email&cpanel_jsonapi_func=listpop&cpanel_jsonapi_version=2&user=" + cpanel_user + "&email=" + email_account["email"]

            # Send a request to the email account's inbox to retrieve the list of emails
            inbox_response = requests.get(inbox_url, headers=headers)

            # Check if the request was successful
            if inbox_response.status_code == 200:
                # Load the JSON response into a dictionary
                emails = json.loads(inbox_response.content)

                # Loop through each email in the inbox
                for email in emails["cpanelresult"]["data"][0]["msgnum"]:
                    # The URL for the individual email
                    email_url = "https://" + cpanel_domain + ":2083/json-api/cpanel?cpanel_jsonapi_module=Email&cpanel_jsonapi_func=fetchpop&cpanel_jsonapi_version=2&user=" + cpanel_user + "&email=" + email_account["email"] + "&msg=" + str(email)

                    # Send a request to retrieve the individual email
                    email_response = requests.get(email_url, headers=headers)

                    # Check if the request was successful
                    if email_response.status_code == 200:
                        # Load the JSON response into a dictionary
                        email_data = json.loads(email_response.content)

                        # Add the sender's email address to the set
                        sender_emails.add(email_data["cpanelresult"]["data"][0]["header"]["from"][0]["address"])

        # Convert the set of sender email addresses to a list
        sender_email_list = list(sender_emails)

        # Print the list of sender email addresses
        print("Sender email addresses:")
        for sender_email in sender_email_list:
            print(sender_email)
    else:
        # If the API request was not successful, print an error message
        print("An error occurred while retrieving the email accounts:", response.content)
