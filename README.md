Automated Book Generation Using AI
This repository contains the source code and documentation for the Final Year Design Project (FYDP) titled "Automated Book Generation Using AI," developed for the Bachelor of Science in Computer Systems Engineering at The Islamia University of Bahawalpur. The project leverages Artificial Intelligence (AI), specifically Natural Language Processing (NLP) and large language models (LLMs), to automate the creation of structured book content, including chapters, table of contents, and additional sections like copyright and prologue. The system is accessible via a web interface, making it user-friendly for writers, educators, and content creators.
Project Overview
The project aims to streamline the book-writing process by automating content generation using OpenAI's GPT-4-turbo for text and DALL·E 3 for cover images. Users input parameters such as book title, description, number of chapters, word count, author name, and font style through a web interface. The system generates a complete book structure, including a table of contents, chapters with subheadings, and supplementary sections (e.g., copyright, disclaimer, prologue, foreword, epilogue, back cover). The generated content can be previewed in a formatted book layout and downloaded as PDF or Word documents.
The application is built using a modular architecture:

Backend: A Flask-based web server (app.py) handles user requests and coordinates with the AI processing module.
AI Processing: The process.py module uses OpenAI's API to generate text and images, ensuring coherent and contextually relevant content.
Frontend: The user interface (index.html, index.css, index.js) provides an intuitive form for input and dynamic rendering of generated content, styled to resemble an A4 book layout.

Key features include:

Dynamic generation of book content based on user prompts.
Support for customizable fonts (e.g., Roboto, Open Sans, Lato) and word counts.
Asynchronous content updates for a seamless user experience.
Modular design for scalability and future enhancements.

Repository Structure

app.py: Flask backend controller that handles HTTP requests, routes, and rendering of the web interface.
process.py: AI content generation module using OpenAI's GPT-4-turbo for text and DALL·E 3 for cover images.
index.html: Frontend interface with a form for user inputs and dynamic content rendering using Jinja2 templating.
index.css: Stylesheet for the frontend, providing an A4-sized book layout and responsive design.
index.js: JavaScript for handling Word document exports and text formatting.
fydp_report.pdf: The project report documenting objectives, methodology, implementation, and results.
requirements.txt: Lists Python dependencies (e.g., flask, openai, requests).
.gitignore: Excludes sensitive files (e.g., .env, Python cache files).
README.md: This file, providing an overview and setup instructions.

Setup Instructions
To run the project locally, follow these steps:

Clone the Repository:
git clone https://github.com/hananislam908/fydp-automated-book-generation-using-ai.git
cd fydp-book-generation


Install Dependencies:

Ensure Python 3.8+ is installed.
Install required packages:pip install -r requirements.txt




Set Up Environment Variables:

Create a .env file in the project root with your OpenAI API key:OPENAI_API_KEY=your-api-key-here


The .env file is excluded from version control via .gitignore for security.


Run the Flask Application:
python app.py


The app will run at http://127.0.0.1:5000.


Access the Web Interface:

Open a browser and navigate to http://127.0.0.1:5000.
Enter book details (title, description, chapters, word count, author, font).
Submit to generate and preview the book content.
Download the book as a PDF or Word document.



Requirements

Python: 3.8 or higher
Dependencies: Listed in requirements.txt (e.g., flask, openai, requests, python-dotenv)
OpenAI API Key: Required for text and image generation (sign up at x.ai/api).
Browser: Modern browser (e.g., Chrome, Firefox) for the web interface.

Usage

Access the web interface at http://127.0.0.1:5000.
Fill in the form with:
Book title and description
Number of chapters and total word count
Author name and preferred font


Submit the form to generate the book content.
Preview the generated table of contents, chapters, and additional sections.
Use the provided buttons to download the book as a PDF or Word document.

Authors

Muhammad Ahmad Ashraf (F21BCSEN1M01027)
Muhammad Hanan Islam (F21BCSEN1M01023)

Supervisor: Dr. Hira Asghar
Institution: Department of Computer Systems Engineering, Faculty of Engineering, The Islamia University of Bahawalpur

Future Enhancements

Integrate advanced AI models (e.g., fine-tuned LLMs) for improved coherence.
Add user authentication and content history tracking.
Support multi-lingual content generation.
Implement plagiarism detection and ethical safeguards.
Enhance frontend with frameworks like React for richer interactivity.

Note:
For issues or contributions, please open an issue or pull request on this repository.