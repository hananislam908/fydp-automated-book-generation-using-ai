from openai import OpenAI
from process import Agent_TableOfContent ,NumberOfSubheadings , writeChapterContent, extraContentGenration , getfrontCover,getbackCover, download_image, bigChapterAgent_TableOfContent, bigSubHeadingAgent_TableOfContent, getWordsPerSubheading
import json

client = OpenAI(api_key="...")



# bookName ="Fundamental of Data Engineering"
# totalNumbersOfWords = 1000
# noOfChapters = 3
# noOfWordsForEveryChaper = NumberOfSubheadings(totalNumbersOfWords,noOfChapters)

# tableOfContent = Agent_TableOfContent(client, bookName, noOfChapters,noOfWordsForEveryChaper)
# book_content = writeChapterContent(client,tableOfContent)
# copyRightPage = copyRightGenration(client, bookName,tableOfContent,book_content)



# Flask code

from flask import Flask, render_template,request #request is used to handle form data submitted by user
app = Flask(_name_)  #app is the main application. 

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'POST':
        bookName = request.form['bookname'] #checks the data  submitted
        description = request.form['description']
        noOfChapters = request.form['noOfChapters']
        noOfWords = request.form['noOfwords']
        authorName = request.form['authorName']
        font = request.form.get('font') # avoid error 
        print("Font: ", font)
        wordsPerSubheading = getWordsPerSubheading(font)
        print(wordsPerSubheading)
        noOfSubheadingsForEveryChaper = NumberOfSubheadings(int(noOfWords), int(noOfChapters))

        ## Table of Content 
        if int(noOfWords)<0:
            print("less than 10000")
            tableOfContent_json=Agent_TableOfContent(client, bookName, noOfChapters,noOfSubheadingsForEveryChaper)
            # print(tableOfContent_json)
            tableOfContent = json.loads(tableOfContent_json)
            with open('copyright.txt', 'w',encoding='utf-8',errors='ignore') as file:
            # Write some text to the file
                file.write(str(tableOfContent))
        else:
            chapters = bigChapterAgent_TableOfContent(client, bookName,description, noOfChapters)
            chapters = json.loads(chapters)
            print("Chaptersss: ",chapters)
            tableOfContent = bigSubHeadingAgent_TableOfContent(client, bookName,description, chapters,noOfSubheadingsForEveryChaper)
            bookNametoSaveFile = bookName.split(" ")[0]
            with open(f'{bookNametoSaveFile}_TOC.txt', 'w',encoding='utf-8',errors='ignore') as file:
            # Write some text to the file
                file.write(str(tableOfContent))
            # with open('ALLERGY AND IMMUNE COMPLEX DISEASES PANDEMIC: A COMPREHENSIVE GUIDE FOR PRACTICING CLINICIANS_TOC.txt', 'r') as file:
            #     tableOfContent = eval(file.read())

        
        print("Chapters: ",noOfChapters)
        print("No of words: ",noOfWords)
        print("No of Subheadings per Chapter: ",noOfSubheadingsForEveryChaper)
        print("Toc: ",tableOfContent)


        

        # ChapterPlot = writeChaptersPlot(client,bookName,description,tableOfContent)
        # Book COntent 
        book_content = writeChapterContent(client,tableOfContent,172,bookName,bookNametoSaveFile)
        for i in range(len(book_content)):
                for key in list(book_content[i].keys()):
                    if len(str(book_content[i][key])) > 300:
                        new_key = 'Content'
                        book_content[i][new_key] = book_content[i].pop(key)
                        break
        for i in range(len(book_content)):
            if 'Content' in book_content[i]:
                print("Present")
            elif len(book_content[i])>1:
                book_content[i]['Content'] = book_content[i].pop(list(book_content[i].keys())[1])
                print(list(book_content[i].keys())[1])
        with open(f'{bookNametoSaveFile}_Content.txt', 'w') as file:
            # Write some text to the file
            file.write(str(book_content))
        # book = json.loads(book_content)
        
        # print(copyRightPage)




        copyRightPage = extraContentGenration(client, bookName,tableOfContent,authorName)


        # with open('ALLERGY AND IMMUNE COMPLEX DISEASES PANDEMIC: A COMPREHENSIVE GUIDE FOR PRACTICING CLINICIANS_Content.txt', 'r') as file:
        #     content = file.read()
        #     book_content = eval(content)
        #     print(len(book_content))
        #     for i in range(len(book_content)):
        #         for key in list(book_content[i].keys()):
        #             if len(str(book_content[i][key])) > 300:
        #                 new_key = 'Content'  # New key name
        #                 book_content[i][new_key] = book_content[i].pop(key)
        #                 break
        #             # print("data:::",type(str(book_content[i][key])))
        #     for i in range(len(book_content)):
        #         if 'Content' in book_content[i]:
        #             # print("Present")
        #             pass
        #         elif len(book_content[i])>1:
        #             book_content[i]['Content'] = book_content[i].pop(list(book_content[i].keys())[1])
        #             print(list(book_content[i].keys())[1])





            
        coverfrontPageUrl = getfrontCover(client,bookName)
        download_image(coverfrontPageUrl, "static/images/front.jpg")
        coverbackPageUrl = getbackCover(client,bookName)
        download_image(coverbackPageUrl, "static/images/back.jpg")
        ## copywrite
        # copyRight = ""
        # with open('copyright.txt', 'r' , encoding='utf-8') as file:
        #     copyRight = file.read()
        # # ## disclaimer
        # disclaimer = ""
        # with open('disclaimer.txt', 'r' , encoding='utf-8') as file:
        #     disclaimer = file.read()
        # ## table of content
        # tableOfContent = json.loads(tableOfContent_json)
        # print(tableOfContent)

        # print(copyRightPage[0])

        copyRight =copyRightPage[0]['copyright']
        disclaimer =copyRightPage[1]['disclaimer']
        prologue =copyRightPage[2]['prologue']
        forword =copyRightPage[3]['foreword']
        epilogue =copyRightPage[4]['epilogue']
        backcover =copyRightPage[5]['back-cover']
        # print(type(book_content))
        # print(book_content)
        # print(type(book_content[0]))
        # print(book_content[0])
        

        
        return render_template('index.html',bookName=bookName,tableOfContent=tableOfContent, copyRight=copyRight,disclaimer=disclaimer,prologue=prologue,forword = forword,epilogue=epilogue,backcover=backcover, book=book_content,words=int(noOfWords),authorName = authorName, font = font )
    return render_template('index.html')



if _name_ == '_main_':
    app.run(debug=True,port=5000)