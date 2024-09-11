# Project LIA Setting Agent
# Created : 2024.03.02 By Mint

print("[alert] Settings Load Complete")
global llama_file
llama_file = "llama3.1"

def setting(name):
    global version_type
    global icon_url
    global thumbnail
    if name == "LIA":
        version_type = "Release"
        icon_url = ""
        thumbnail = ""
    else:
        version_type = "Debug"
        icon_url = ""
        thumbnail = ""
        llama_file = "llama3.1"
