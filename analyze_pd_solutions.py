from bs4 import BeautifulSoup
import re

def clean_str(str):
    str.replace("\n","") 
    return ' '.join(str.split())

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')


    pattern = r"Question (\d+) Answer: (\d) (.+)"
    answers = []

    questions_number = 0
    matches_number = 0

    for li_tag in soup.find_all('p', recursive=False):

        #filtering the the "good <p>", we discart the <p> that have math or further explanation about the question
        raw_line = li_tag.text.strip()
        raw_line = clean_str(raw_line)


        if raw_line.startswith("Question") :

            questions_number = questions_number +1 

            match = re.match(pattern, raw_line)

            if match:

                matches_number = matches_number + 1
                question_number = match.group(1)
                answer_number = match.group(2)
                explanation = match.group(3)

                # Print the extracted information
                # print("Question Number:", question_number)
                # print("Answer Number:", answer_number)
                # print("Explanation:", explanation)

                answer = {
                    'question_number': question_number,
                    'answer_number': answer_number,
                    "explanation" : explanation,
                }

                answers.append(answer)
            else:
                print("No match found.")
    
    print(f"number of questions that start with Question: {questions_number}")
    print(f"number of questions that match: {matches_number}")

    return answers

def read_html_file(file_path):
    with open(file_path,"r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content

if __name__ == "__main__":
    print("beginning  for solutions .....")
    html_file_path = "./pd_solutions.html"

    html_content = read_html_file(html_file_path)

    answers_data = parse_html(html_content)

    number_set = set(range(1, 1001))



    for i, answer in enumerate(answers_data, start=1):


        q_number = int(answer['question_number'])
        if q_number in number_set :
            number_set.remove(q_number)
        else :
            print (f" the number {q_number} is not in the set")
            
        # print(f"Question {answer['question_number']}:")
        # print(f"  Answer: {answer['answer_number']}")
        # print(f"  Explanation: {answer['explanation']}")
            
    
    print(f"the bad questions are {number_set}")


    print("end---")
