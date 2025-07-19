import re, time, json, datetime as dt


header = f"""

// ==UserScript==
// @name         Banana4Ape
// @namespace    http://tampermonkey.net/
// @version      {dt.datetime.now().strftime("%d.%m.%y")}
// @description  try to take over the world!
// @author       APES_COMMUNITY
// @match        https://apes.io/
// @icon         https://www.google.com/s2/favicons?sz=64&domain=apes.io
// @grant        none
// @run-at       document-start
// ==/UserScript==

"""

def update_js() -> None:
    file_paths = json.load(open("config.json"))["file_paths"]
    vars_section = []
    api_section = []
    init_section = []

    for file_path in file_paths:
        text = open(file_path).read()
        lines = text.split("\n")

        vars_section_begin_index = None
        vars_section_end_index = None
        api_section_begin_index = None
        api_section_end_index = None
        init_section_begin_index = None
        init_section_end_index = None

        for i, line in enumerate(lines):
            if vars_section_begin_index is None and line == "// [SECTION VARS BEGIN]":
                vars_section_begin_index = i
            elif vars_section_end_index is None and line == "// [SECTION VARS END]":
                vars_section_end_index = i
            elif api_section_begin_index is None and line == "// [SECTION API BEGIN]":
                api_section_begin_index = i
            elif api_section_end_index is None and line == "// [SECTION API END]":
                api_section_end_index = i
            elif init_section_begin_index is None and line == "// [SECTION INIT BEGIN]":
                init_section_begin_index = i
            elif init_section_end_index is None and line == "// [SECTION INIT END]":
                init_section_end_index = i

            try:
                comment_begin_index = line.index("//")
                
                if line[comment_begin_index:comment_begin_index + 10] == "// [LOAD \"":
                    j = 0
                    path_begin_index = None
                    path_end_index = None

                    while True:
                        s = line[j]
                        
                        if s == "\"":
                            if path_begin_index is not None:
                                path_end_index = j
                                break
                            
                            path_begin_index = j + 1

                        j += 1
                    
                    lines[i] = line[:comment_begin_index] + f"`{open(line[path_begin_index:path_end_index]).read()}`;"
                else:
                    lines[i] = line[:comment_begin_index]
            except ValueError:
                ...

        if vars_section_begin_index is not None:
            vars_section.append(
                "\n".join(lines[vars_section_begin_index + 1:vars_section_end_index])
            )
        if api_section_begin_index is not None:
            api_section.append(
                "\n".join(lines[api_section_begin_index + 1:api_section_end_index])
            )
        if init_section_begin_index is not None:
            init_section.append(
                "\n".join(lines[init_section_begin_index + 1:init_section_end_index])
            )

    with open("compiled.js", "w") as f:
        text = re.sub(r'\s+', " ", (
            "\n".join(vars_section) +
            "\n".join(api_section) +
            "\n".join(init_section)
        ).replace("\n", ""))

        f.write(
            header[2:] + text
        )


while 1:
    update_js()

    time.sleep(5)
