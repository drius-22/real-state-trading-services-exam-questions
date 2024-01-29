from bs4 import BeautifulSoup
import re
import csv


# also do "</span>"
def clean_str(str):
    str.replace("\n","") 
    return ' '.join(str.split())

def parse_questions(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    questions = []
    bad_counter = 0

    question_counter= 0 
    for li_tag in soup.find_all('li', recursive=False):

        question_counter = question_counter +1 

        question_text = li_tag.find('p').text.strip()

        if "[SKIP]" not in question_text :


            l = len(li_tag.find_all('p',  recursive=False))
            if l != 1:
                print(li_tag.find('p',  recursive=False))
                raise ValueError(f" there are {l} <p> than expected in question --------------- >> {question_counter} << ------- : ")
        
            #cleaning string
            question_text = clean_str(question_text)
            answers = [clean_str(answer_tag.text.strip()) for answer_tag in li_tag.find_all('li')]

            if len(answers) != 4:
                #format is bad so try this.
                bad_counter = bad_counter +1

        else:
            question_text = f"Question {question_counter} SKIPPED due to format"
            answers: ['1','2','3','4']

        question_data = {
            'question': question_text,
            'answers': answers
        }

        questions.append(question_data)

    print (f"bad questions: {bad_counter}")
    return questions



def parse_answers(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')


    pattern = r"Question (\d+) Answer: (\d) (.+)"
    answers = []
    counter= 1

    for li_tag in soup.find_all('p', recursive=False):

        #filtering the the "good <p>", we discart the <p> that have math or further explanation about the question
        raw_line = li_tag.text.strip()
        raw_line = clean_str(raw_line)
        if raw_line.startswith("Question") :

            match = re.match(pattern, raw_line)

            if match:
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
                print(f"No match found. {counter}")
                counter= counter+1

    return answers
        


def read_html_file(file_path):
    with open(file_path,"r", encoding="utf-8") as file:
        html_content = file.read()
    return html_content




#####
if __name__ == "__main__":
    print("beginning questions  .....")
    questions_path = "./pq.html"

    questions_content = read_html_file(questions_path)

    questions_data = parse_questions(questions_content)

    print(f"lenght of questions {len(questions_data)}")

    # for i, question_data in enumerate(questions_data, start=1):
    #     print(f"Question {i}:")
    #     print(f"  Text: {question_data['question']}")
    #     print("  Answers:")
    #     for j, answer in enumerate(question_data['answers'], start=1):
    #         print(f"    ({j}) {answer}")
    #     print("\n")



    print("beginning answers  .....")

    answers_path = "./pd_solutions.html"
    answers_content =  read_html_file(answers_path)

    answers_data = parse_answers(answers_content)

    print(f"lenght of answers {len(answers_data)}")

    # for i, answer in enumerate(answers_data, start=1):
    #     print(f"Question {answer['question_number']}:")
    #     print(f"  Answer: {answer['answer_number']}")
    #     print(f"  Explanation: {answer['explanation']}")

    csv_file_path = "./latest_500_questions_and_answers.csv"

    with open(csv_file_path, mode='w', newline='') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)

        # for number in range(0, 500): 
        for number in range(500, 1000):
            question_number = number+1
            print (f"Question {question_number}")

            question = questions_data[number]
            questions_answers = question['answers']
            question_str = f"Question {question_number}: {question['question']} \n(1){questions_answers[0]} \n(2){questions_answers[1]} \n(3){questions_answers[2]} \n(4){questions_answers[3]}"

            answer = answers_data[number]
            answer_str = f"Answer: {answer['answer_number']} Explanation: {answer['explanation']}"

            csv_writer.writerow([question_str, answer_str])
            # print(question_str)
            # print(answer_str)

    





    print("end---")
