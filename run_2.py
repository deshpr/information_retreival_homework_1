import os
from os import listdir
import math
from os.path import isfile, join
import re
import pdb
from operator import itemgetter
import csv

def get_file_content(filename):
    content = ""
    with open(filename, 'r') as myfile:
        content = myfile.read().replace(os.linesep, '')
    return content

def get_stop_words():
    curren_directory = os.getcwd()
    stop_words_location = ".\stop_words_english.txt"
    stop_words_location = os.path.join(curren_directory, stop_words_location)
    filename = stop_words_location    
    if os.path.isfile(filename): 
        separator = "\n" # os.linesep
        stop_words = get_file_content(filename).split(separator)
#    else:
#        stop_words = ['the', 'that', 'to', 'as', 'there', 'has', 'and', 'or', 'is', 'not', 'a', 'of', 'but', 'in', 'by', 'on', 'are', 'it', 'if']
    return stop_words

def get_special_characters():
    curren_directory = os.getcwd()
    special_characters_location = ".\special_characters_english.txt"
    special_characters_location = os.path.join(curren_directory, special_characters_location)
    filename = special_characters_location    
    separator = "\n" # os.linesep
    special_characters = get_file_content(filename).split(separator)
#    print(special_characters)
    return special_characters
    

def replace_ignore_case(content, to_replace, replace_with):
    regex = re.compile(to_replace, re.IGNORECASE)
    return regex.sub(content, replace_with)

"""
def remove_stop_words(words, stop_words):
    for stop_word in stop_words:
        if stop_word.strip() in words:
            if stop_word.strip() == "it":
                print("\n\nhere\n\n")
            words = [i for i in words if i != stop_word.strip()]
#            words= list(filter(lambda a: a.strip() != stop_word, words))
    return words
"""

def remove_stop_words(words, stop_words):
    result = []
    for word in words:
#        if word == "it":
#            print("\n\n found one\n\n")
        is_stop_word = False
        for stop_word in stop_words:
#            if stop_word == "it" and word == "it":
#                print("\n\n found other\n\n")            
            if stop_word.strip() == word.strip():
#                if word == "it":
#                    print("\n\n is stop word\n\n")
                is_stop_word = True
                break
        if not is_stop_word:
            result.append(word)        
    return result


def porter_stem_word(word):
    from nltk.stem import PorterStemmer
    stemmer = PorterStemmer()
    return stemmer.stem(word)

def remove_special_characters(words, special_characters):
    result = []
    for word in words:
#        done = False
        for character in special_characters:
            if character in word:
#                if word == "gay?" and character == "?":
#                    done = True
#                    print("old word = {}".format(word))
                word = word.replace(character, "")

#                if done:
#                    print("new word = {}".format(word))
        if word:
            result.append(word)
#        if done:
#            print(result)
    return result

def phase_remove_special_characters(words):
    special_characters = get_special_characters()
    for content in content_list:     
#        print("before = {}".format(content))   
        content = remove_special_characters(content, special_characters)
#        input("Press Enter to continue...")
#        print("after = {}".format(content))

def porter_stem(words):
    result = []
    for word in words:    
        result.append(porter_stem_word(word))
    return result

def remove_spaces(words):
    result = []
    for word in words:
        if word:
            result.append(word)
    return result

def phase_process_content(directoryname, ext = ".txt"):
    stop_words = get_stop_words()
#    print(stop_words)
    special_characters = get_special_characters()
    files_no_stop_words = {}
    for file in listdir(directoryname):
        # get file content
        if file.endswith(ext):
            full_file_name = os.path.join(directoryname, file)
            content = get_file_content(full_file_name)
            content = content.lower()
#            print("before = {}".format(content))   

            tokenized = tokenize(content)
            tokenized = remove_stop_words(tokenized, stop_words)

            tokenized = remove_special_characters(tokenized, special_characters)

            tokenized = porter_stem(tokenized)
            tokenized = remove_stop_words(tokenized, stop_words)
            tokenized = remove_spaces(tokenized)
#            print("\n\n")
#            print("Content after = {}".format(tokenized))
#            input("Press Enter to continue...")

            files_no_stop_words[full_file_name] = tokenized
    return files_no_stop_words


def write_result(directoryname, file_name,  content_files):
    curren_directory = os.getcwd()
    directory = os.path.join(curren_directory, directoryname)
    if not os.path.exists(directory):
        os.makedirs(directory)
    i = 0
    for filename, words in content_files.items():
        output_file_name = file_name + str(i) + ".txt"

        with open(os.path.join(directory,output_file_name), 'w') as output_file:
            output_file.write(" ".join(words))
        i = i + 1
    print("written = {} files".format(len(content_files)))


def tokenize(content):
    return content.split()


def calculate_total_words(content_list):
    count = 0
    for filename, token_list in content_list.items():
        count += len(token_list)
    return count

def unique_word_count(content_list):
    hashtable = {}
    for filename, token_list in content_list.items():
        for token in token_list:
            if token not in hashtable:
                hashtable[token] = ""
    return len(hashtable.keys())


def get_frequency_table(content_list):
    hashtable = {}
    for filename, token_list in content_list.items():
        for token in token_list:
            if token not in hashtable:
                hashtable[token] = 0
            else:
                hashtable[token] += 1
    return hashtable

def write_csv(filename, elements):
    with open(filename, 'a') as csvfile:
        for element in elements:
#            print(element)
#            to_write = ",".join(element)
#            print(element.split(","))
            csvfile.write(element + "\n")

def append_csv(filename, content):
    with open(filename, 'a') as csvfile:
        csvfile.write(content + "\n")


def get_words_of_frequency(content_list, required_frequency):
    hashtable = get_frequency_table(content_list)
    return len([key for key, value in hashtable.items() if value == 1])

def calculate_average_word_count(content_list):
    total_word_count = calculate_total_words(content_list)
    total_documents = len(content_list)
    return total_word_count/total_documents

def get_highest_frequency_tokens(content_list, top = 30):
    sorted_hash_table = {}
    hashtable = get_frequency_table(content_list)
    sorted_hash_table = dict(sorted(hashtable.items(), key=lambda k:k[1])[-top:][::-1])
    return sorted_hash_table

def calculate_term_frequency(content_list, term):
    count = 0
    for filename, content in content_list.items():
        count_1 = len([element for element in content if element == term])
        count += count_1
    return count

def calculate_inverse_document_frequency(content_list, term):
    count = 0
    number_of_documents = len(content_list)
    for filename, content in content_list.items():
        if term in content:
            count += 1
    return math.log(number_of_documents/count)/math.log(10)
    
def calculate_complete_content_probability(content_list, word):
    complete_content = []
    for filename, content in content_list.items():
        for token in content:
            complete_content.append(token)
    return calculate_individual_probability(complete_content, word)

def calculate_individual_probability(content, word):
    total = len(content)
    word_count = len([i for i in content if i == word])
    return word_count/total


def print_statistics(content_list):
    
    curren_directory = os.getcwd()
    filename_output = 'output.csv'    
    total = calculate_total_words(content_list)
    print("Total word count: {}".format(total))
    append_csv(filename_output, "Total word count: {}".format(total))
    


    total_unique_word_count = unique_word_count(content_list)
    print("Unique word count: {}".format(total_unique_word_count))
    append_csv(filename_output, "Unique word count: {}".format(total_unique_word_count))


    one_word_count = get_words_of_frequency(content_list, 1)
    print("Words that occurred only once: {}".format(one_word_count))
    append_csv(filename_output, "Words that occurred only once: {}".format(one_word_count))


    word_average = calculate_average_word_count(content_list)
    print("Average count of words per document: {}".format(int(word_average)))
    append_csv(filename_output, "Average count of words per document: {}".format(int(word_average)))


    highest_frequency_tokens = get_highest_frequency_tokens(content_list, 30)
    print("Highest frequency tokens:")
    for element, count in highest_frequency_tokens.items():
        append_csv(filename_output, element)
    
    
    print(highest_frequency_tokens)
    
    
    to_write = []
    to_write.append("Term, Term Frequency, Inverse Document Frequency, TF * IDF, Probability")
    print("Term, Term Frequency, Inverse Document Frequency, TF * IDF, Probability")
    for token, count in highest_frequency_tokens.items():
        term_frequency = calculate_term_frequency(content_list, token)
        inverse_document_frequency = calculate_inverse_document_frequency(content_list, token)
        multiplication = term_frequency * inverse_document_frequency
        probability =  calculate_complete_content_probability(content_list, token)
        print("{}, {}, {}, {}, {}".format(token, term_frequency, inverse_document_frequency, multiplication, probability)) 
        to_write.append("{}, {}, {}, {}, {}".format(token, term_frequency, inverse_document_frequency, multiplication, probability)) 
    

   
    output_file = os.path.join(curren_directory, filename_output)
    write_csv(output_file, to_write)

    print("Program Complete.")

def phase_convert_lower(content):
    return content.lower()

def run(directoryname, ext = ".txt"):

    print("removing stop words..")

    content_no_stop_words = phase_process_content(directoryname, ext)
    print_statistics(content_no_stop_words)


run("C:\\Users\\Rahul Deshpande\\Desktop\\UW Tacoma\\Spring\\HW_1\\transcripts\\transcripts")