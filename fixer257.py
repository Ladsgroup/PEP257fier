import codecs
import re
filename = "page_tests.py"


#pep257 *.py -s --ignore=D100,D102,D101,D205,D103 > allout.txt 2>&1
errr = codecs.open("allout.txt", "r", "utf-8")
errors = errr.read().split(u"\n\n\n")
errr.close()


def fix200(a, b):
    doc_line = []
    ok = False
    for line in b.split("\n\n")[1].split("\n"):
        if "\"\"\"" in ":".join(line.split(":")[1:]):
            if not ok:
                ok = True
            elif ok:
                ok = False
            continue
        if ok:
            doc_line.append(":".join(line.split(":")[1:])[1:])
    if doc_line:
        a = re.sub(ur"(\"\"\")\s+?(%s)\s+?\"\"\"" % re.escape(doc_line[0].strip()), ur"\1\2\1", a)
        # a = a.replace("\"\"\"\n"+doc_line[0]+"\n\"\"\"",u"\"\"\"%s\"\"\"" % doc_line[0].strip())
    return a


def fix202(a, b):
    doc_line = []
    for i in range(len(b.split("\n\n")[1].split("\n"))):
        line = b.split("\n\n")[1].split("\n")[i]
        if "\"\"\"" in ":".join(line.split(":")[1:]) and i != 0:
            doc_line.append(":".join(b.split("\n\n")[1].split("\n")[i-1].split(":")[1:])[1:] + "\n"+":".join(line.split(":")[1:])[1:])
    if doc_line and not len(doc_line[-1].replace(" ", "").replace("\n", "")) < 4:
        a = a.replace(doc_line[-1] + "\n\n", doc_line[-1] + "\n")
    return a


def fix203(a, b):
    doc_line = []
    for i in range(len(b.split("\n\n")[1].split("\n"))):
        line = b.split("\n\n")[1].split("\n")[i]
        if "\"\"\"" in ":".join(line.split(":")[1:]) and i+1 < len(b.split("\n\n")[1].split("\n")):
            doc_line.append(":".join(line.split(":")[1:])[1:] + "\n" + ":".join(b.split("\n\n")[1].split("\n")[i+1].split(":")[1:])[1:])
    if doc_line and not len(doc_line[0].replace(" ", "").replace("\n", "")) < 4:
        a = a.replace(doc_line[0], "\n"+doc_line[0])
    return a


def fix204(a, b):
    doc_line = []
    for i in range(len(b.split("\n\n")[1].split("\n"))):
        line = b.split("\n\n")[1].split("\n")[i]
        if "\"\"\"" in ":".join(line.split(":")[1:]) and i != 0:
            doc_line.append(":".join(b.split("\n\n")[1].split("\n")[i-1].split(":")[1:])[1:] + "\n"+":".join(line.split(":")[1:])[1:])
    if doc_line and not len(doc_line[-1].replace(" ", "").replace("\n", "")) < 4:
        a = a.replace(doc_line[-1], doc_line[-1].rstrip() + "\n")
    return a


def fix208(a, b):
    doc_line = []
    for line in b.split("\n\n")[1].split("\n"):
        if "\"\"\"" in ":".join(line.split(":")[1:]):
            doc_line.append(":".join(line.split(":")[1:])[1:])
    if doc_line and not len(doc_line[0].replace(" ", "").replace("\n", "")) < 4:
        g = (" "*(len(doc_line[0][1:]) - len(doc_line[0][1:].strip())))
        a = a.replace(doc_line[0], "%s \"\"\"\n%s " % (g, g) + doc_line[0].split("\"\"\"")[1].strip())
    return a


def fix209(a, b):
    doc_line = []
    for line in b.split("\n\n")[1].split("\n"):
        if "\"\"\"" in ":".join(line.split(":")[1:]):
            doc_line.append(":".join(line.split(":")[1:])[1:])
    if doc_line and not len(doc_line[-1].replace(" ", "").replace("\n", "")) < 4:
        g = (" " * (len(doc_line[0][1:]) - len(doc_line[0][1:].strip())))
        a = a.replace(doc_line[-1], doc_line[-1].split("\"\"\"")[0].rstrip() + "\n%s \"\"\"" % g)
    return a


def fix400(a, b):
    doc_line = []
    for line in b.split("\n\n")[1].split("\n"):
        if ":".join(line.split(":")[1:]).count("\"\"\"") == 2:
            doc_line.append(":".join(line.split(":")[1:])[1:])
    if doc_line:
        a = re.sub(ur"(\"\"\") *?(%s) *?\"\"\"" % doc_line[-1].strip().strip("\"").strip(), ur"\1\2.\1", a)
        # a = a.replace(doc_line[-1],"%s \"\"\"" %(" "*(len(doc_line[-1][1:])-len(doc_line[-1].strip())))+doc_line[-1].split("\"\"\"")[1].strip()+"."+"\"\"\"")
    return a


for error in errors:
    try:
        error.split("\n")[1]
    except IndexError:
        continue
    if error.count("\"\"\"") != 2:
        continue
    filename = error.split(".py")[0].strip() + ".py"
    if "\n" in filename:
        continue
    file = codecs.open(filename, "r", "utf-8")
    content = file.read()
    file.close()
    error_type = error.split("\n")[1].strip().split(":")[0]
    if error_type == "D200":
        content = fix200(content, error)
    if error_type == "D202":
        content = fix202(content, error)
    if error_type == "D203" and error.split("\n")[1].strip().endswith("0"):
        content = fix203(content, error)
    if error_type == "D204" and error.split("\n")[1].strip().endswith("0"):
        content = fix204(content, error)
    if error_type == "D208":
        content = fix208(content, error)
    if error_type == "D209":
        content = fix209(content, error)
    if error_type == "D400":
        content = fix400(content, error)
    file = codecs.open(filename, "w", "utf-8")
    file.write(content)
    file.close()
