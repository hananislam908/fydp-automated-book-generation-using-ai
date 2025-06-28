import json
import requests
from openai import RateLimitError
# this function is for the table of content
def Agent_TableOfContent(client, bookName,noOfChapters, noOfSubheadings):

    response = client.chat.completions.create( 

    model='gpt-4-turbo',
    max_tokens=3500,
    response_format={"type": "json_object"},
    messages=[{'role':"system","content":f"""You're a world class book writer. 
              You are tasked with creating a table of contents for a comprehensive guide on given topic.
              The guide aims to provide a structured overview of all major aspects of topic, concepts, covering key subtopics and methodologies. 
              Please ensure that the table of contents is well-organized and captures the essential elements of the subject matter.

Instructions:


1. Ensure coherence and logical flow throughout the table of contents.
2. Include key terms and concepts relevant to the topic.
3. Aim for completeness and comprehensiveness, covering all major aspects of the topic.
4. Avoid redundancy and irrelevant information.
5. The table of contents should be detailed enough to provide a clear roadmap for readers, but concise enough to be easily digestible.
6. User will provide you with: 1. Book Title, 2. Number of Chapters to be written and 3. Number of Subheadings per chapter.

Important: Your response must be in json format, like this:
{{
  "BookTitle": "Book Title here",
  "Chapters": [
    {{
      "Chapter1": "Chapter 1 Title here",
      "Subheadings": ["Name of subheading 1","Name of subheading 2","Name of subheading 3", ...]
    }},
    {{
      "Chapter2": "Chapter 2 Title here",
      "Subheadings": ["Name of subheading 1","Name of subheading 2","Name of subheading 3", ...]
    }},
    {{
      "Chapter3": "Chapter 3 Title here",
      "Subheadings": ["Name of subheading 1","Name of subheading 2","Name of subheading 3", ...]
    }},
    ...
  ]
}}

Do you understand?"""},
             {'role':"assistant","content":"Ok, Understood!"},
             {'role':"user","content":f"""The book name is {bookName},
              number of chapter to be written is {noOfChapters},
              and the number of Subheadings per chapter is {noOfSubheadings}. Must write {noOfSubheadings} per Chapter."""}],
    )
    content = response.choices[0].message.content
    # print(content) 
    return content


def bigChapterAgent_TableOfContent(client, bookName,description ,noOfChapters):
    try:
      response = client.chat.completions.create(

      model='gpt-4-turbo',
      max_tokens=3500,
      response_format={"type": "json_object"},
      messages=[{'role':"system","content":f"""You're a world class book writer. 
                You are tasked with creating a table of contents for a comprehensive guide on given topic.
                The guide aims to provide a overview of all major aspects of topic, concepts, covering key methodologies. 
                Please ensure that the table of contents is well-organized and captures the essential elements of the subject matter.

  Instructions:

  1. Provide a comprehensive table of contents.
  2. Ensure coherence and logical flow throughout the table of contents.
  3. Include key terms and concepts relevant to the topic.
  4. Aim for completeness and comprehensiveness, covering all major aspects of the topic.
  5. Avoid redundancy and irrelevant information.
  6. The table of contents should be detailed enough to provide a clear roadmap for readers, but concise enough to be easily digestible.
  7. User will provide you with: 1. Book Title, 2. Book Description 2. Number of Chapters to be written.
  8. Just provide the Chapter titles, don't write sections or subsections.

  Important: Your response must be in json format, like this:
  {{
    "BookTitle": "Book Title here",
    "Chapters": [
      {{
        "Chapter1": "Chapter 1 Title here",
      }},
      {{
        "Chapter2": "Chapter 2 Title here",
      }},
      {{
        "Chapter3": "Chapter 3 Title here",
      }},
      ...
    ]
  }}

  Do you understand?"""},
              {'role':"assistant","content":"Ok, Understood!"},
              {'role':"user","content":f"""The book name is {bookName},
  Description: {description},
  number of chapter to be written is {noOfChapters}.
                
                Must follow the number of chapters, description of the book"""}],
      )
      content = response.choices[0].message.content
    except RateLimitError as e:
      print("Not enough credits in OpenAI's API account! add some bucks..")
    return content

def bigSubHeadingAgent_TableOfContent(client, bookName,description, ChapterNames, noOfSubheadings):
    notEnoughCredits = False
    for i,Chapter in enumerate(ChapterNames['Chapters']):
      print("CCC",Chapter)
      while True:
        try:
          response = client.chat.completions.create(

          model='gpt-4-turbo',
          max_tokens=3500,
          response_format={"type": "json_object"},
          messages=[{'role':"system","content":f"""You're a world class book writer. 
                    You are tasked with creating a table of contents for a comprehensive guide on given topic.
                    The guide aims to provide a structured overview of all major aspects of topic, concepts, covering key subtopics and methodologies.
                    Please ensure that the subheadings is well-organized and captures the essential elements of the subject matter.

      Instructions:

      1. Provide a hierarchical structure for the subheadings.
      2. Ensure coherence and logical flow throughout.
      3. Include key terms and concepts relevant to the topic.
      4. Aim for completeness and comprehensiveness, covering all major aspects of the topic.
      5. Avoid redundancy and irrelevant information.
      7. User will provide you with: 1. Book Title, 2. Chapter name and 3. Subheadings per chapter.
      8. Just write Subheading names, don't add anything else. don't mention subheading number 1.1, 1.2 etc.

      Important: Your response must be in json format, here is the example format, you must follow:
      {{
        "Subheadings" : ["Name of subheading 1","Name of subheading 2","Name of subheading 3", ...]
      }}
      Do you understand?"""},
                  {'role':"assistant","content":"Ok, Understood!"},
                  {'role':"user","content":f"""The book name is {bookName},
                    Here are the Chapter Name for your context
                    
                    {ChapterNames}

                    and you'll be wrting subheadings for Chapter{i+1}
                    Chapter Name is {Chapter}
                    and the number of Subheadings per chapter is {noOfSubheadings}. Must write {noOfSubheadings} for this Chapter."""}],
          )
          # print(response.choices[0].message.content)
          # print(ast.literal_eval(response.choices[0].message.content))
          print(f"tttt\n\n{response.choices[0].message.content}\n\neeee")
          ChapterNames['Chapters'][i]['Subheadings'] = json.loads(response.choices[0].message.content)['Subheadings']
          print(ChapterNames['Chapters'])
          print("*")
        except json.decoder.JSONDecodeError as e:
          print("JSON Decoder Error Occured: Retrying...")
        except RateLimitError as e:
          print("Not enough credits in OpenAI's API account! add some bucks..")
          notEnoughCredits = True
          break
        except Exception as e:
            print("Error: {e} - Trying Again...")
        else:
          break
      if notEnoughCredits == True:
        break
    return ChapterNames
    # print(content)


def writeChapterContent(client,tableOfContent,wordsPerSubheading,bookName,bookNametoSaveFile):
    book_content =[]
    UnsufficientCredits = False
    
    data = tableOfContent
    bookName = data['BookTitle']
    # book_content = bookName 
    # Extract chapter names and subheadings
    for i,chapter in enumerate(data['Chapters']):
      chapter_no = list(chapter.keys())[0] #key
      chapter_names = chapter[chapter_no]  #value
      subheadings = list(chapter.keys())[1] #key
      subheadings_name = chapter[subheadings] #value
      # book_content += "\n\n "
      # book_content += chapter_names 
      for j,subheading in enumerate(subheadings_name):
        user_msg = f"""I'm writing a book on {bookName}. Here below is the high-level table of content including Chapters and their sub topics.
                \n\n{tableOfContent['Chapters'][i]}

                \n\nYou're tasked to write {wordsPerSubheading} words about subheading no.{j+1} - {subheading} of Chapter no.{i+1} - {chapter_names}. {wordsPerSubheading} words with multiple paragraphs.
        Make it incredibly unique, engaging, and well-written.
                        \n\nHere is the content of previous subheadings. Keep the context of these subheadings in mind while generating the content.
        previous subheadings content: {book_content[-5:]}
        Include only the chapter text, and no surrounding explanations or text.\n\n. There is no need to rewrite the chapter name.
                        
        Important: Subheading must contain multiple paragraphs (3-4 atleast) and Write exactly {wordsPerSubheading} words and Your response must be in json format, like this:
        {{
          "Subheading" : "Name of Subheading {j+1}",
          "Content" : "content here.({wordsPerSubheading} words)."
        }}"""
        while True:
          try:
            print(f"Chapter no.{i+1}, subheading no.{j+1} is being generated...")
            response = client.chat.completions.create(
            model='gpt-4-turbo',
            max_tokens=3000,
            timeout=20,
            response_format={"type": "json_object"},
            messages=[
                    {"role": "system", "content": f"""You are a world-class book writer."""},
                    {"role": "user", "content": user_msg}
                ],
            # stream=True
            )
            data = json.loads(response.choices[0].message.content)
            if len(data['Content'])>300:
              pass
            # book_content += "\n"
            if j==0:
              data['Chapter'] = chapter_names
            book_content.append(data)
            with open(f'{bookNametoSaveFile}_Content.txt', 'w',encoding='utf-8',errors='ignore') as file:
                file.write(str(book_content))
            print("-------------------------------------------------------------")
          except json.decoder.JSONDecodeError as e:
             print("JSON Decoder Error Occured: Retrying...")
          except RateLimitError as e:
             print("Not enough credits in OpenAI's API account! add some bucks..")
             UnsufficientCredits = True
             break
          except UnicodeEncodeError as e:
              print("UnicodeEncodeError Occured: Retrying...")
          except Exception as e:
             print(f"Error: {e} - Trying Again...")
          else:
             break
        if UnsufficientCredits == True:
          break
      if UnsufficientCredits == True:
        break
    # book_content+="\n"     
    return book_content

def NumberOfSubheadings(totalWords,totalChapter):
    
    # var = 0
    # if totalWords<=5000:
    #     var=150
    # elif totalWords<= 10000 and totalWords>5000:
    #     var=200
    # elif totalWords<= 15000 and totalWords>10000:
    #     var=250
    # elif totalWords<= 20000 and totalWords>15000:
    #     var=400
    # else:
    #     var = 500


        
    wordsPerChapter =totalWords/totalChapter
    return int(round(wordsPerChapter/170))

# def writeChaptersPlot(client,bookName,tableOfContent):
#    response = client.chat.completions.create(

#   model='gpt-4-turbo',
#   max_tokens=3500,
#   response_format={"type": "json_object"},
#   messages=[{'role':"system","content":f"""You're a world class book writer. 
#             You are tasked with writing plot for the give 1. Book Title 2. Description of the Book 2. Table Of Content. 
#             Please ensure that the table of contents is well-organized and captures the essential elements of the subject matter.

#     Instructions:

#     3. Include key terms and concepts relevant to the topic.
#     4. Aim for completeness and comprehensiveness, covering all major aspects of the topic.
#     5. Avoid redundancy and irrelevant information.
#     7. User will provide you with: 1. Book Title 2. Description of the Book 2. Table Of Content.

#     Important: Your response must be in json format, like this:
#     {{
#     "Chapters": [
#       {{
#         "Chapter1": "Chapter 1 Title here",
#         "Plot": "Plot for Chapter3 here"
#       }},
#       {{
#         "Chapter2": "Chapter 2 Title here",
#         "Plot": "Plot for Chapter3 here"
#       }},
#       {{
#         "Chapter3": "Chapter 3 Title here",
#         "Plot": "Plot for Chapter3 here"
#       }},
#       ...
#     ]
#     }}

#     Do you understand?"""},
#     {'role':"assistant","content":"Ok, Understood!"},
#     {'role':"user","content":f"""The book name is {bookName},
#     Table of Content {tableOfContent}"""}],
# )
#    return response.choices[0].message.content


def extraContentGenration(client,bookName,tableOfContent, authorName):
    contentList=[]

    frontBackContent=''
    Content = ['copyright','disclaimer','prologue','foreword','epilogue','back-cover']
    for i,topic in enumerate(Content):
      response = client.chat.completions.create(
          model='gpt-4-turbo',
          max_tokens=3000,
          response_format={"type": "json_object"},
          messages=[
                  {"role": "system", "content": f"""You're a world class book writer. You're tasked to write {topic} for the book entitled as {bookName}, written by {authorName}, Year is 2025,
                  For context, Here is the high-level table of content including Chapters and their sub topics.
                  \n\n{tableOfContent}\n\nand\n\n
                  Important: Write exactly 350 words and Your response must be in json format, like this:
                  {{
                  "{topic}":"{topic} content here. Write 350 words for {topic}.",
                  }}"""},])
      contentList.append(json.loads(response.choices[0].message.content)) 
      print("-------------------------------------------------------------")
    print(response.choices[0].message.content)
    
    return contentList


def getfrontCover(client,prompt):
  response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
  )
  return response.data[0].url

def getbackCover(client,prompt):
  response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
  )
  return response.data[0].url



def download_image(url, save_path):
    try:
        # Send a GET request to the URL to fetch the image
        response = requests.get(url)
        if response.status_code == 200:
            # Open the file in binary write mode and write the content of the response
            with open(save_path, 'wb') as f: #close the file automatically when done due to with block
                f.write(response.content)
            print("Image downloaded successfully")
        else:
            print("Failed to download image. Status code:", response.status_code)
    except Exception as e:
        print("Error:", e)

def getWordsPerSubheading(font):
   if font == 'OpenSans' or font == 'PoetsenOne':
      return 170
   elif font == 'Lato' or font == 'Roboto':
      return 180
   else:
      return 190