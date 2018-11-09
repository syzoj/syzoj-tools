import os

all_languages = None

def load_languages():
    global all_languages
    if all_languages == None:
        from .compiled import ProblemCLanguage, ProblemCppLanguage, ProblemPasLanguage
        all_languages = {
            ".c": ProblemCLanguage,
            ".cpp": ProblemCppLanguage,
            ".pas": ProblemPasLanguage
        }

def get_all_languages():
    global all_languages
    load_languages()
    return all_languages

def get_language(ext):
    global all_languages
    load_languages()
    return all_languages.get(ext)
