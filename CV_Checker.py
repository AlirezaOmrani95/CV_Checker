"""
File: CV_Checker.py
Author: Ali Reza (ARO) Omrani
Email: omrani.alireza95@gmail.com
Date: 23rd March 2025

Description:
------
This file uses LLM models to compare CVs with the Job advertisements.
Various LLM models can be selected for the comparisons. Also, zero-shot or one-shot learning can be chosen too.

Functions:
- parse_argument(): Parses command-line arguments and returns them as a namespace object.
- payload(text, client, example, model, mode): Feeds a prompt to an LLM model for the evaluation.
- run_playwright(url): Extracts information from the webpage.
- json_writer(): Writs a json file of the examples.
- json_loader(file_address): Reads the json file examples.

Requirements:
------
- pymupdf4llm
- playwright
- openai
- os
- requests
- json
- argparse

Notes:
------
- The CV address can be also a URL.
"""
import pymupdf4llm
from playwright.sync_api import sync_playwright
import openai

import os
import requests
import json
import argparse

def parse_argument():
    '''
    Parses command-line arguments and returns them as a namespace object.

    Parameters:
    -----
        None

    Returns:
    -----
        argparse.Namespace: A namespace object containing the parsed command-line arguments.

    Example usage:
        $ python CV_Checker.py --cv 'cv.pdf' --learn_mode 'one-shot' --model_type 'google/gemma-3-27b-it:free'
        After execution, you can access the arguments as:
        args.cv             # Path to the CV file 
        args.learn_mode     # Mode of Learning ("zero-shot", "one-shot")
        args.model_type     # Model type for comparison
    '''
    #list of available free models.
    with open('free_model_names.txt', 'r') as file:
        model_name = [line.strip() for line in file.readlines()]    

    parser = argparse.ArgumentParser(description='The script uses LLM models to compare CVs with the Job advertisements.')
    parser.add_argument('--cv', type= str, required= True, help= 'Path to the CV file (URL can be entered too)\nThe Acceptable formats: PDF, DOC/DOCX, XLS/XLSX, PPT/PPTX, HWP/HWPX.')
    parser.add_argument('--learn_mode', type= str, choices= ['zero-shot','one-shot'], default= 'one-shot', help= 'The learning mode for the model.')
    parser.add_argument('--model_type', type= str, choices= model_name, default= 'google/gemma-3-27b-it:free', help= 'Specify model type (choose from the available models).')

    return parser.parse_args()

def payload(text, client, example, model = 'google/gemma-3-27b-it:free', mode = 0):
    '''
    Feeding a prompt to an LLM model for the evaluation.

    Parameters:
    -----
        text (str): The pandas dataframe containing the data. 
        client (openai object): An instance of the OpenAI API client.
        example (str): The example for the shot learning.
        model (str): The model's name.
        mode (int): The type of evaluation. Default value is 0.

    Returns:
    -----
        result (str): The model's response.

    Note:
    -----
    - The options for mode are 0 or 1.

    '''

    if mode == 0: # mode 0: Info procedure, or extracting info from job requirements and responsibilities sections.
        
        # Expected message for LLM model.
        messages =[{"role": "user", "content": f"""Please follow the example below exactly as shown and do not add any extra information or details.\nIf the text is not in English, translate it to English first. Then parse me Responsibilities and Requirements from the following text:

                    Example:
                    
                    {example}

                    Now, given the following job description, extract the 'Responsibilities' and 'Requirements' in the same format as the example above:

                    {text}"""}]
        
        # Expected output structure.
        response_format = {
            "type": "json_schema",
            "json_schema":{
                "name": "Output",
                "strict": True,
                "schema":{
                    "type":"object",
                    "properties":{
                        "Requirements":{
                            'type':'list of strings',
                            'description': "Requirement for the job"
                        },
                        "Responsibilities":{
                            'type':'list of strings',
                            'description':'Future responsibilities in the job'
                        }
                    },
                    'required':['Requirements','Responsibilities'],
                    'additionalProperties': False,
                },
            },
            },
    
    elif mode == 1: # mode 1: Comparison procedure, or making a comparison of info from the CV and the extracted info from the job.
        
        # Expected message for LLM model.
        messages = [{"role": "user",
                     "content": f"""Please follow the example below exactly as shown and do not add any extra information or details.\nOnly include the similar keywords that are in both job description and CV, and only inlcude the keywords that are in the job description but not in the CV.
                      
                     Example:

                     {example} 
                      
                     Now, given the following **Job Description** and **CV**, compare in the same format as the example above:

                     {text}"""}]
        
        # Expected output structure.
        response_format = {
            "type": "json_schema",
            "json_schema":{
                "name": "Output",
                "strict": True,
                "schema":{
                    "type":"object",
                    "properties":{
                        "The Semantic Similarity Percentage":{
                            'type':'float:.1f',
                            'description': "the value is in Percentage"
                        },
                        "Similar keywords":{
                            'type':'list of strings',
                            'description':'Similar keywords between the job and CV'
                        },
                        "Different keywords":{
                            'type':'list of strings',
                            'description':'Different keywords between the job and CV'
                        },
                        "Similarity percentage of the keywords":{
                            'type':'float:.1f',
                            'description':'the value is in Percentage'
                        },
                    },
                    'required':['The Semantic Similarity Percentage','Similar keywords',
                                'Different keywords','Similarity percentage of the keywords'],
                    'additionalProperties': False,
                },
            },
            },
    
    try:
        completion = client.chat.completions.create(
            model = model,
            messages = messages,
            response_format = response_format
            )
        result = completion.choices[0].message.content
        return result
    
    except openai.OpenAIError as e:
        print(f"Error occurred: {e}")

def run_playwright(url):
    '''
    Extracting information from the webpage.

    Parameters:
    -----
        url (str): The Job position URL.

    Returns:
    -----
        web_text (str): Extracted job description.
    '''

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use headless=False to see the browser
        page = browser.new_page()

        page.goto(url)
        page.wait_for_timeout(2000) # Wait 2 additional seconds to avoid possible problem.
        page.wait_for_selector('body')  # Wait for the page to load
        web_text = page.inner_text('body')  # Get the text content of the body
        browser.close()
    
    return web_text

def json_writer():
    '''
    Writing a json file of the examples.

    Parameters:
    -----
        None
    Returns:
    -----
        None
    '''
    data = {
        "info": "Text:\nSkip to main content\n\nThis site uses cookies in order to provide you with the best browsing experience. By using this site, you agree to our use of cookies. Learn more about our Cookie Policy.\n\nDecline\nAccept Cookies\nSign In\nSwift Homepage\nSearch for Jobs\nAI/ML Security Engineer page is loaded\nAI/ML Security Engineer\nApply\nlocations\nManassas, United States\nLeiden area, Netherlands\nposted on\nPosted 25 Days Ago\njob requisition id\n2024-14041\n\nABOUT US\n\nWe’re the world’s leading provider of secure financial messaging services, headquartered in Belgium. We are the way the world moves value – across borders, through cities and overseas. No other organisation can address the scale, precision, pace and trust that this demands, and we’re proud to support the global economy.\xa0\n\nWe’re unique too. We were established to find a better way for the global financial community to move value – a reliable, safe and secure approach that the community can trust, completely. We’re always striving to be better and are constantly evolving in an ever-changing landscape, without undermining that trust. Five decades on, our vibrant community reflects the complexity and diversity of the financial ecosystem. We innovate diligently, test exhaustively, then implement fast. In a connected and exciting era, our mission has never been more relevant. Swift now has a presence in 200+ countries and legal territories to serve a community of more than 12,000 banks and financial institutions.\xa0\xa0\xa0\n\nWhat to expect:\nDesign, develop, and implement security frameworks and strategies to protect AI/ML models and their use, and related data, applications and systems from adversarial attacks and other security threats.\nDevelop standards and best practices for a secure use, development, deployment, and operationalization of AI/ML (predictive AI, generative AI and Large Language Models).\nAnalyze potential security risks in AI/ML applications, such as model poisoning, data leakage, and other adversarial machine learning threats, and define mitigations that can be effectively implemented.\nCollaborate with cross-functional teams to ensure AI/ML systems are integrated, deployed or leveraged with robust security practices throughout the development lifecycle of proprietary models, or through the implementation of pre-trained models, AI-based SaaS solutions, ...\nResearch and stay ahead of emerging security threats in AI/ML and propose innovative defense strategies.\nConduct security assessments and robustness testing of AI/ML models, with appropriate tooling, identifying weaknesses and providing recommendations for improvement.\nCollaborate with internal teams to ensure compliance with relevant regulations, standards, and security frameworks in AI/ML-related initiatives.\nProvide guidance and act as centre of expertise for business, technical, legal, privacy and risk teams on assessing risks and implementing controls for AI/ML projects.\nEffectively communicate complex AI/ML security assessments, risks, controls and mitigations to management, technical teams and non-technical stakeholders.\n\nWhat you need to be successful:\n\nUniversity degree in Computer Science, AI/ML, Cybersecurity or related field, or equivalent experience.\n8-10 years of relevant experience, including in AI/ML models development and deployment. \nProficiency in programming languages such as Python, Java, or C++, and in AI/ML frameworks and libraries such as TensorFlow, PyTorch, scikit-learn, Keras, and XGBoost.\nStrong understanding of security concepts, including secure coding practices, threat modeling, and risk assessment.\nExpertise in securing AI/ML systems, including protection against adversarial attacks, data poisoning, ensuring the integrity of model training and inference processes, confidentiality of model and trained data.\nStrong analytical and problem-solving skills, attention to detail, and ability to work in a collaborative team environment.\nExcellent communication skills, including the ability to translate complex technical information for a non-technical audience.\n\nWhat we offer\n\nWe put you in control of career\n\nWe give you a competitive package\n\nWe help you perform at your best\n\nWe help you make a difference\n\nWe give you the freedom to be yourself\n\nWe give you the freedom to be yourself. We are creating an environment of unique individuals – like you – with different perspectives on the financial industry and the world. A diverse and inclusive environment in which everyone’s voice counts and where you can reach your full potential.\n\nIf you believe you require a reasonable accommodation to participate in the job application or interview process, please contact us to request accommodation.\n\nDon’t meet every single requirement? At Swift, we are dedicated to building a workplace where people can bring their full selves and ideas to the team, so if you are excited about this role, we encourage you to apply even if you do not meet every single qualification.\n\nSimilar Jobs (5)\nSecurity Architect\nlocations\n2 Locations\ntime type\nFull time\nposted on\nPosted 17 Days Ago\nPKI Security Architect\nlocations\n2 Locations\nposted on\nPosted Yesterday\nHybrid Platform Security Architect\nlocations\nManassas, United States\nposted on\nPosted 16 Days Ago\nView All 5 Jobs\nLoading\nFollow Us\n© 2025 Workday, Inc. All rights reserved.\n\nOutput:\nResponsibilities:\n- Design, develop, and implement security frameworks and strategies to protect AI/ML models and their use, and related data, applications and systems from adversarial attacks and other security threats.\n- Develop standards and best practices for a secure use, development, deployment, and operationalization of AI/ML (predictive AI, generative AI and Large Language Models).\n- Analyze potential security risks in AI/ML applications, such as model poisoning, data leakage, and other adversarial machine learning threats, and define mitigations that can be effectively implemented.\n- Collaborate with cross-functional teams to ensure AI/ML systems are integrated, deployed or leveraged with robust security practices throughout the development lifecycle of proprietary models, or through the implementation of pre-trained models, AI-based SaaS solutions, ...\n- Research and stay ahead of emerging security threats in AI/ML and propose innovative defense strategies.\n- Conduct security assessments and robustness testing of AI/ML models, with appropriate tooling, identifying weaknesses and providing recommendations for improvement.\n- Collaborate with internal teams to ensure compliance with relevant regulations, standards, and security frameworks in AI/ML-related initiatives.\n- Provide guidance and act as centre of expertise for business, technical, legal, privacy and risk teams on assessing risks and implementing controls for AI/ML projects.\n- Effectively communicate complex AI/ML security assessments, risks, controls and mitigations to management, technical teams and non-technical stakeholders.\n\nRequirements:\n- University degree in Computer Science, AI/ML, Cybersecurity or related field, or equivalent experience.\n- 8-10 years of relevant experience, including in AI/ML models development and deployment. \n- Proficiency in programming languages such as Python, Java, or C++, and in AI/ML frameworks and libraries such as TensorFlow, PyTorch, scikit-learn, Keras, and XGBoost.\n- Strong understanding of security concepts, including secure coding practices, threat modeling, and risk assessment.\n- Expertise in securing AI/ML systems, including protection against adversarial attacks, data poisoning, ensuring the integrity of model training and inference processes, confidentiality of model and trained data.\n- Strong analytical and problem-solving skills, attention to detail, and ability to work in a collaborative team environment.\n- Excellent communication skills, including the ability to translate complex technical information for a non-technical audience.",        
        "compare":"Job Description:\n\nResponsibilities:\n- Design, develop, and implement security frameworks for AI/ML models.\n- Collaborate with cross-functional teams for AI/ML security.\n- Conduct security assessments for AI/ML systems.\n\nRequirements:\n- 8-10 years of experience in AI/ML.\n- Expertise in Python, TensorFlow, and security concepts for AI/ML systems.\n- Data Leakage\n- Master's or a University degree in Computer Science or related field, or equivalent experience.\n- PySpark\n- SQL\n- LLM\n\nCV:\n- Skills: Python, TensorFlow, Data Security, Threat Modeling, AI/ML, Pytorch, Scikit-Learn\n- Experience: AI/ML development, Security of AI/ML models, Threat modeling expertise, collaborative, Image Processing, Computer Vision, Vision Transformer, \n- Education: PhD in Artificial Intellgience\n\nOutput:\nThe Semantic Similarity Percentage: 72.5%\n\nSimilar keywords:\n- Python\n- Tensorflow\n- AI/ML\n- Security\n- collaboration\n- PhD\n\nDifferent keywords:\n- Data Leakage\n- SQL\n- PySpark\n- LLM\n\nThe Similarity percentage between the similar and different keywords: 66%"}
    
    with open('examples.json','w') as j_file:
        json.dump(data,j_file,indent=4)

def json_loader(file_address):
    '''
    Reading a json file of the examples.

    Parameters:
    -----
        file_address(str): The location of json file.
    Returns:
    -----
        json_file(dict): examples for an LLM model.
    '''
    with open(file_address, 'r') as j_file:
        return(json.load(j_file))

if __name__ == '__main__':
    args = parse_argument()
    API_Key = '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'
    api_url = 'https://openrouter.ai/api/v1'
    learning_mode = args.learn_mode

    client = openai.OpenAI(
        base_url=api_url,
        api_key=API_Key
        )
    model_type = args.model_type # Various models can be chosen.

    if learning_mode == 'one-shot':
        model_examples = json_loader('examples.json')
    elif learning_mode == 'zero-shot':
        model_examples = {'info':'',
                          'compare':''}

    #Extracting info from the CV
    cv_address = args.cv
    
    if not os.path.exists(cv_address): #If the address is a URL, it first downloads and then load the file.
        response = requests.get(cv_address)
        cv_address = cv_address.split('/')[-1]
        with open(cv_address, 'wb') as f:
            f.write(response.content)
    
    print('\nParsing the information from the CV...')
    my_cv = pymupdf4llm.to_markdown(cv_address) #Extracting information from the CV using an LLM model 

    while True:
        
        #Extracting Job info from the link
        position_url = input('\nEnter the link of the Positon ( or just enter to quite):\n')
        if position_url == '':
            quit()
        
        print('\nParsing the information from the link...')
        web_texts = run_playwright(position_url)

        web_info = payload(text = web_texts,
                        model = model_type,
                        example = model_examples['info'],
                        client = client,
                        mode = 0)

        print('Making the comparison...\n')
        comparison = payload(text = f"""
                            Job Description:
                            {web_info}
                            CV:
                            {my_cv}""",
                            model = model_type,
                            example = model_examples['compare'],
                            client = client,
                            mode = 1)
        
        print(comparison)