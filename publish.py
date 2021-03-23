# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pathlib
import re

def main():
    if len(sys.argv) > 1:
        print("Script does not take any arguments")
        return
    #extract_doc_from_dtx("highlightlatex.dtx", "highlightlatex_doc.tex")
    generate_dtx("highlightlatex_doc.tex", "highlightlatex.sty", "publish/highlightlatex.dtx")

    pass

def generate_dtx(docFile, styFile, path):
    with open(path, "w") as outp:
        with open("template_dtx.txt", "r") as templFile:
            templ = iter(templFile)

            for l in templ:
                if "%% DOC-PREAMBLE" in l:
                    m = re.fullmatch(r"(?P<before>.*?)%% DOC-PREAMBLE(?P<after>.*)\n", l)
                    before = m.group("before")
                    after = m.group("after")
                    with open(docFile, "r") as doc:
                        for docline in doc:
                            if "\\begin{document}" in docline:
                                break
                            outp.write(before + docline + after)

                elif "%% DOC-DOCUMENT" in l:
                    m = re.fullmatch(r"(?P<before>.*?)%% DOC-DOCUMENT(?P<after>.*)\n", l)
                    before = m.group("before")
                    after = m.group("after")
                    with open(docFile, "r") as doc:
                        dociter = iter(doc)
                        for docline in dociter:
                            if "\\begin{document}" in docline:
                                break

                        stripIndent = True
                        for docline in dociter:
                            if docline.startswith("\\end{document}"):
                                break
                            line = docline
                            if line.startswith("%"):
                                continue
                            line = line.replace("\t", "    ")
                            if line == r"\def\defaultgobble{8}" + "\n":
                                line = f"\\def\\defaultgobble{{{8 + len(before)}}}\n"

                            line = doHighlightBlockLogic(line, before)

                            # highlBlockBegin = re.fullmatch(
                            #     r"(?P<argsBefore>(?P<indent>\s*)" + 
                            #     r"\\begin\{highlightblock\})\[(?P<args>.*)\]" + 
                            #     r"(?P<argsAfter>\n?)", line)
                            # if highlBlockBegin != None:
                            #     highlighBlockIndent = highlBlockBegin.group("indent")
                            #     newgobble = len(highlighBlockIndent) + 4 + len(before)

                            #     gobbleMatch = re.fullmatch(r"(?P<before>.*,\s*)?gobble=\d+(?P<after>\s*,.*)?", highlBlockBegin.group("args"))
                            #     if gobbleMatch != None:
                            #         line = highlBlockBegin.group("argsBefore") \
                            #         + f"[{gobbleMatch.group('before') or ''}gobble={newgobble}" \
                            #         + f"{gobbleMatch.group('after') or ''}]" \
                            #         + highlBlockBegin.group("argsAfter")

                            # if stripIndent:
                            #     if line.startswith("\t"):
                            #         line = line[1:]
                            #     elif line.startswith("    "):
                            #         line = line[4:]
                            #     else:
                            #         stripIndent = False

                            outp.write(before + line + after)


                elif "%% STY" in l:
                    m = re.fullmatch(r"(?P<before>.*?)%% STY(?P<after>.*)\n", l)
                    before = m.group("before")
                    after = m.group("after")
                    with open(styFile, "r") as doc:
                        for docline in doc:
                            if docline.startswith("%%%"):
                                continue
                            docline = docline.replace("\t", "    ")
                            outp.write(before + docline + after)

                else:
                    outp.write(l)

highlightBlockIndent = None

def doHighlightBlockLogic(line, before):
    global highlightBlockIndent

    if highlightBlockIndent != None:
        m = re.fullmatch(
        r"(?P<argsBefore>(?P<indent>\s*)" + 
        r"\\end\{highlightblock\})(?P<argsAfter>\n?)", line)

        if m != None:
            highlightBlockIndent = None
        return line

    m = re.fullmatch(
        r"(?P<argsBefore>(?P<indent>\s*)" + 
        r"\\begin\{highlightblock\})(\[(?P<args>.*)\])?" + 
        r"(?P<argsAfter>\n?)", line)
    if m == None:
        return line

    highlightBlockIndent = m.group("indent")
    newgobble = len(highlightBlockIndent) + 4 + len(before)

    gobbleMatch = None

    if m.group("args") != None:
        gobbleMatch = re.fullmatch(r"(?P<before>.*,\s*)?gobble=\d+(?P<after>\s*,.*)?",
            m.group("args"))

    if gobbleMatch == None:
        return line
    
    return m.group("argsBefore") \
        + f"[{gobbleMatch.group('before') or ''}gobble={newgobble}" \
        + f"{gobbleMatch.group('after') or ''}]" \
        + m.group("argsAfter")


def extract_doc_from_dtx(dtxFile, texFile):
    with open(texFile, "w") as outp:
        with open(dtxFile, "r") as inpFile:
            inp = iter(inpFile)

            for l in inp:
                if l.startswith("%"):
                    continue
                if "\\DocInput" in l:
                    extract_doc_docinput(dtxFile, outp, indent="\t")
                elif "\\endinput" in l:
                    break
                else:
                    outp.write(l)

def extract_doc_docinput(dtxFile, outp, indent=""):
    with open(dtxFile, "r") as inpFile:
        inp = iter(inpFile)

        while True:
            l = next(inp, None)
            if l == None:
                break

            if l.startswith("% \\iffalse"):
                if "\\fi" in l:
                    continue
                while l != None and not l.startswith("% \\fi"):
                    l = next(inp, None)
                continue

            if "\\Finale" in l:
                break

            if l.startswith("% "):
                l = l[2:]
            elif l.startswith("%"):
                l = l[1:]
            outp.write(indent + l)


if __name__ == "__main__":
    main()
