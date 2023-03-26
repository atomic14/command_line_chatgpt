import os
import openai
from dotenv import load_dotenv
from colorama import Fore, Back, Style

# load values from the .env file if it exists
load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

INSTRUCTIONS = """Hello, AI chatbot! You are a virtual assistant designed to help visitors on our tree surgery and gardening services website. Your main purpose is to assist with scheduling appointments for consultations and quotes, answering basic questions about our services, and providing information about our company. We need their full name, phone number, email, location, and service requirement.

If you are unable to provide an answer to a question, please respond with the phrase "I'm just a simple AI Bot, I can't help with that"

As an assistant, you should be able to:

- Schedule appointments: Help users book appointments for consultations, quotes, and assessments. Gather necessary details like user's preferred date, time, and type of service they're interested in.
- Reschedule or cancel appointments: Assist users in changing or canceling scheduled appointments. Confirm changes with the user and update our appointment system accordingly.

Continuing your responsibilities as an AI chatbot:

- Provide information about services: Answer questions related to tree surgery and gardening services, such as tree removal, pruning, stump grinding, garden maintenance, and more. Be knowledgeable about our service offerings and explain them clearly and concisely.
- Respond to quoting and pricing inquiries: Explain to users that each job is unique and requires a site visit to provide an accurate price. Inform them that a detailed quote will be given after an on-site assessment. Remind users that consultations are free.

More instructions for you, AI chatbot:

- Maintain a polite and professional tone: Always be courteous and respectful in your interactions with users. Ensure your responses are in English English and exhibit proper grammar, spelling, and punctuation.
- Do not use external URLs or refer to blogs in your answers.
- Format any lines on individual line with a dash and a space in front of each of them if people ask for gardening tips. Make sure it is relevant to the UK.

We're based in Newmarket, Suffolk and have about a 40-mile radius. Remember, your primary goal is to provide users with a seamless experience in scheduling appointments and obtaining information about our tree surgery and gardening services. Be as helpful and informative as possible, while maintaining a friendly and approachable tone. Good luck!"""

TEMPERATURE = 0.5
MAX_TOKENS = 500
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 10


def get_response(instructions, previous_questions_and_answers, new_question):
    """Get a response from ChatCompletion

    Args:
        instructions: The instructions for the chat bot - this determines how it will behave
        previous_questions_and_answers: Chat history
        new_question: The new question to ask the bot

    Returns:
        The response text
    """
    # build the messages
    messages = [
        { "role": "system", "content": instructions },
    ]
    # add the previous questions and answers
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        messages.append({ "role": "user", "content": question })
        messages.append({ "role": "assistant", "content": answer })
    # add the new question
    messages.append({ "role": "user", "content": new_question })

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=1,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY,
    )
    return completion.choices[0].message.content


def get_moderation(question):
    """
    Check the question is safe to ask the model

    Parameters:
        question (str): The question to check

    Returns a list of errors if the question is not safe, otherwise returns None
    """

    errors = {
        "hate": "Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.",
        "hate/threatening": "Hateful content that also includes violence or serious harm towards the targeted group.",
        "self-harm": "Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and eating disorders.",
        "sexual": "Content meant to arouse sexual excitement, such as the description of sexual activity, or that promotes sexual services (excluding sex education and wellness).",
        "sexual/minors": "Sexual content that includes an individual who is under 18 years old.",
        "violence": "Content that promotes or glorifies violence or celebrates the suffering or humiliation of others.",
        "violence/graphic": "Violent content that depicts death, violence, or serious physical injury in extreme graphic detail.",
    }
    response = openai.Moderation.create(input=question)
    if response.results[0].flagged:
        # get the categories that are flagged and generate a message
        result = [
            error
            for category, error in errors.items()
            if response.results[0].categories[category]
        ]
        return result
    return None


def main():
    os.system("cls" if os.name == "nt" else "clear")
    # keep track of previous questions and answers
    previous_questions_and_answers = []
    while True:
        # ask the user for their question
        new_question = input(
            Fore.GREEN + Style.BRIGHT + "What can I get you?: " + Style.RESET_ALL
        )
        # check the question is safe
        errors = get_moderation(new_question)
        if errors:
            print(
                Fore.RED
                + Style.BRIGHT
                + "Sorry, you're question didn't pass the moderation check:"
            )
            for error in errors:
                print(error)
            print(Style.RESET_ALL)
            continue
        response = get_response(INSTRUCTIONS, previous_questions_and_answers, new_question)

        # add the new question and answer to the list of previous questions and answers
        previous_questions_and_answers.append((new_question, response))

        # print the response
        print(Fore.CYAN + Style.BRIGHT + "Here you go: " + Style.NORMAL + response)


if __name__ == "__main__":
    main()
