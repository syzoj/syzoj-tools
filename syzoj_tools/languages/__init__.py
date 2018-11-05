from .compiled import ProblemCLanguage, ProblemCppLanguage, ProblemPasLanguage

all_languages = {
    ".c": ProblemCLanguage,
    ".cpp": ProblemCppLanguage,
    ".pas": ProblemPasLanguage
}

