import os

# Projcet LIA
# token selector
# Created : 2024.03.04 by Mint

selector = input("[alert] Release -> 1, Debug -> else : ")


if selector == "1" or selector.lower() == "release":
    # LIA Live Server
    print("[alert] LIA Live Server OPEN")
    type = "Release"
    token = "라이브 서버 토큰"
else:
    # LIA_DEBUG
    print("[alert] LIA Debug OPEN")
    type = "Debug"
    token = "테스트 서버 토큰"
