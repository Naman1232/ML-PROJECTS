import speech_recognition as sr  
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import sys


listener = sr.Recognizer()
machine = pyttsx3.init()


wikipedia.set_lang("en")

def talk(text):
    machine.say(text)
    machine.runAndWait()

def normalize_name(name):
    words = name.split()
    normalized_words = []
    for word in words:
        if len(word) == 1:
            normalized_words.append(word.upper())
        else:
            normalized_words.append(word.capitalize())
    
    if len(normalized_words) >= 2 and all(len(w) == 1 for w in words[:2]):
        normalized_name = ''.join(normalized_words[:2]) + ' ' + ' '.join(normalized_words[2:])
    else:
        normalized_name = ' '.join(normalized_words)
    return normalized_name.strip()

def input_instruction():
    instruction = ""
    try:
        with sr.Microphone() as origin:
            print("Listening...")
            listener.adjust_for_ambient_noise(origin, duration=1)
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "jarvis" in instruction:
                instruction = instruction.replace('jarvis', "").strip()
                print(f"Recognized Instruction: {instruction}")
    except sr.UnknownValueError:
        talk("Sorry, I did not understand that.")
        print("Could not understand audio")
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
        print("Could not request results from speech service")
    except Exception as e:
        talk("An error occurred.")
        print(f"Error: {e}")
    return instruction

def play_Jarvis():
    instruction = input_instruction()
    print(f"Processing instruction: {instruction}")
    
    if not instruction:
        talk("I didn't catch that. Please try again.")
        return

    if "play" in instruction:
        song = instruction.replace('play', "").strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)
    
    if "exit" in instruction:
        talk("Goodbye!")
        print("Exiting the program as per user request.")
        sys.exit()
    
    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"Current time is {time}")
        print(f"Current time is {time}")  
    
    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk(f"Today's date is {date}")
        print(f"Today's date is {date}") 
    
    elif 'how are you' in instruction:
        response = 'I am fine, how about you?'
        talk(response)
        print(response)  
    
    elif 'what is your name' in instruction:
        response = 'I am Jarvis, your personal assistant. What can I do for you?'
        talk(response)
        print(response)  

    elif any(question in instruction for question in ['who is', 'what is', 'where is', 'why is', 'how is','When is','Which is',
'Can you explain',
'Could you describe',
'Are there',
'Do you know',
'Is it possible',
'What are',
'How does',
'Why do',
'Who was',
'What can',
'Where can',
'Should I',
'Would you mind',
'Has anyone',
'Is there a way',
'What might',
'In what way',
'To what extent']):
        question_prefix = next(prefix for prefix in ['who is', 'what is', 'where is', 'why is', 'how is','When is',
'Which is',
'Can you explain',
'Could you describe',
'Are there',
'Do you know',
'Is it possible',
'What are',
'How does',
'Why do',
'Who was',
'What can',
'Where can',
'Should I',
'Would you mind',
'Has anyone',
'Is there a way',
'What might',
'In what way',
'To what extent'] if prefix in instruction)
        query = instruction.replace(question_prefix, "").strip()
        human_normalized = normalize_name(query)
        print(f"Normalized Name: {human_normalized}")
        
        try:
            info = wikipedia.summary(human_normalized, sentences=2)
            print(info)
            talk(info)
        except wikipedia.exceptions.PageError:
            talk(f"Sorry, I couldn't find a page for '{human_normalized}'. Let me search for related topics.")
            search_results = wikipedia.search(human_normalized)
            if search_results:
                best_match = search_results[0]
                try:
                    info = wikipedia.summary(best_match, sentences=2)
                    print(info)
                    talk(info)
                except Exception as e:
                    talk(f"Sorry, I couldn't retrieve information on '{best_match}'.")
                    print(f"Error fetching summary for '{best_match}': {e}")
            else:
                talk(f"Sorry, I couldn't find any information on '{human_normalized}'.")
                print(f"No search results found for '{human_normalized}'.")
        except wikipedia.exceptions.DisambiguationError as e:
            options = ', '.join(e.options[:5])
            talk(f"The term '{human_normalized}' is ambiguous. Did you mean one of the following: {options}?")
            print(f"DisambiguationError: {e}")
        except Exception as e:
            talk("An error occurred while fetching information.")
            print(f"Error: {e}")
    
    else:
        response = 'Please repeat your command.'
        talk(response)
        print(response)  

if __name__ == "__main__":
    while True:
        play_Jarvis()
