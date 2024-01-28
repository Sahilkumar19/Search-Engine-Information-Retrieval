"""
The general skeleton of a website

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Website Title</title>
</head>

<body>

    <!-- Your content goes here -->

</body>

</html>
 

WHAT EACH FUNCTION IS DOING WRITTEN IN THE SRCIPT;

Title Extraction (get_title):

Sends an HTTP GET request to the specified URL.
Retrieves the raw HTML content from the response.
Searches for the <title> tags in the HTML and extracts the text between them.
Prints the extracted title.


Body Text Extraction (get_body):

Sends an HTTP GET request to the URL.
Retrieves the raw HTML content.
Searches for the <body> tag to locate the start of the body content.
Iterates through the HTML content, extracting text between HTML tags within the body (excluding the tags).
Prints the extracted text content.


Links Extraction (get_links):

Sends an HTTP GET request to the URL.
Retrieves the raw HTML content.
Searches for occurrences of URLs starting with "http" within the HTML content.
Appends the extracted links to a list.
Prints the extracted links.

"""

import requests

def get_title(url):
    #send a GET request to the URL and get the raw HTML content.
    response = requests.get(url) #sends an http get request
    raw_content = response.text  #extract the raw html content from the request
    
    #extract the title from the HTML content
    title_start = raw_content.find("<title>") + len("<title>")
    title_end = raw_content.find("</title>")
    title = raw_content[title_start:title_end]
    
    #print the extracted title
    print("Title:", title)

def get_body(url):
    #send a GET request to the URL and get the raw HTML content
    response = requests.get(url)
    html_content = response.text
    
    #extract text content from the body of the HTML
    texts = []
    start_index = html_content.find("<body")

    if start_index != -1:
        start_index = html_content.find(">", start_index) + 1

        while start_index != -1:
            end_index = html_content.find("<", start_index)
            
            if end_index != -1:
                #extract text between HTML tags and add to the texts list
                text = html_content[start_index:end_index].strip()
                if text:
                    texts.append(text)
                start_index = html_content.find(">", end_index) + 1
            else:
                break
    
    #print the extracted text content
    print("Texts:")
    for t in texts:
        print(t + " ")

def get_links(url):
    #send a GET request to the URL and get the raw HTML content
    response = requests.get(url)
    raw_content = response.text

    #extract links from the HTML content
    body_raw_content = raw_content
    links = []
    while len(body_raw_content) > 1:
        start = body_raw_content.find("http")
        end = body_raw_content[start:].find('"')
        links.append(body_raw_content[start : start + end])
        body_raw_content = body_raw_content[start + end + 1:]

    #print the extracted links
    print("Links:")
    for link in links:
        print(link)

def main():
    #get user input for the URL
    url = input("Enter your URL with https: ")
    
    #call functions to extract and print title, body , and links
    get_title(url)
    get_body(url)
    get_links(url)

if __name__ == "__main__":
    #execute the main function when the script is run
    main()