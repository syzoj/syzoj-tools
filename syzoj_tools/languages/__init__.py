import os

all_languages = None
ext_language = {
    ".c": "c",
    ".cpp": "cpp",
    ".pas": "pascal"
}

def load_languages():
    global all_languages
    if all_languages == None:
        from .compiled import ProblemCLanguage, ProblemCppLanguage, ProblemPasLanguage
        all_languages = {
            "c": ProblemCLanguage,
            "cpp": ProblemCppLanguage,
            "pascal": ProblemPasLanguage
        }

def get_all_languages():
    global all_languages
    load_languages()
    return all_languages

def guess_language(ext):
    global ext_language
    return ext_language[ext]

def get_language(ext):
    global all_languages
    load_languages()
    return all_languages.get(ext)
