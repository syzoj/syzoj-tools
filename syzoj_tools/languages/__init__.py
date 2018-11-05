import os
from .compiled import ProblemCLanguage, ProblemCppLanguage, ProblemPasLanguage

all_languages = {
    ".c": ProblemCLanguage,
    ".cpp": ProblemCppLanguage,
    ".pas": ProblemPasLanguage
}

def get_language(filename):
    (_, ext) = os.path.splitext(filename)
    return all_languages.get(ext)
