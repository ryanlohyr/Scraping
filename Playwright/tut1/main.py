from playwright.sync_api import sync_playwright
import time
import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def get_answer(question_content):
    
    system_prompt = '''
        Keep your answers between 20-50 words in plain text. 
        Respond as if you are a university student in Silicon Valley on a 
        one-year entrepreneurship internship.
        
        Some of context of me, i am currently working at autocomplete, an insurtech company that prices insurace using ai
        I have attended a hackathon called useless build a thon which i won where i built a chrome extension 
    '''
    
    response = completion(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": question_content},
        ],
    )
    
    return response.choices[0].message["content"]

def get_to_assessment(page):
    page.goto("https://growthbeans.coursemology.org/")

    page.wait_for_selector('//button[contains(text(), "Sign in to Coursemology")]')

    page.click('//button[contains(text(), "Sign in to Coursemology")]')

    page.wait_for_selector('//input[@name="email"]')

    page.fill('//input[@name="email"]', "e0969271@u.nus.edu")
    page.fill('//input[@name="password"]', "Animalkaiser12")
    page.click('//button[@type="submit"]')

    page.goto(
        "https://growthbeans.coursemology.org/courses/2797/assessments/70279/submissions/2245540/edit"
    )

def answer_questions(page):
    page.wait_for_selector('xpath=//form[@id="SUBMISSION"]')

    question_divs = page.query_selector_all(
        'xpath=//form[@id="SUBMISSION"]//div[div[h6[starts-with(text(), "Question")]]]'
    )

    print(len(question_divs))
    print(question_divs)

    for i, question_div in enumerate(question_divs):

        # Where the question is located
        elements_between_hr = question_div.query_selector_all(
            "xpath=.//hr[1]/following-sibling::*[following-sibling::hr]"
        )

        # Question context
        question_content = ""
        for element in elements_between_hr:
            question_content += element.inner_html()
        
        ai_answer = get_answer(question_content)
        
        contenteditable_div = question_div.query_selector('xpath=.//div[@contenteditable="true"]')
        contenteditable_div.fill(ai_answer)

         # Verify the content
        print("filled")
        print(contenteditable_div.inner_html())
        
        
        if contenteditable_div:
            try:
                # Use page.evaluate to set the inner HTML of the contenteditable div
                contenteditable_div.evaluate('element => element.innerText = "Your desired text here"')
                print("filled")
                print(contenteditable_div.inner_html())
            except Exception as e:
                print(f"Error filling contenteditable div in div {i + 1}: {e}")
        else:
            print(f"No contenteditable <div> found in div {i + 1}")

with sync_playwright() as p:
    
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    
    get_to_assessment(page)
    
    answer_questions(page)

    time.sleep(100)
    browser.close()
    # page.goto("https://growthbeans.coursemology.org/courses/2797/assessments?category=3781")
