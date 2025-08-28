import os
import requests
from openai import OpenAI
from openai.types.shared.chat_model import ChatModel

def make_response(
        user_content: str, 
        system_content: str | None = None, 
        temperature: float = 0.25,
        model: str | ChatModel = "gpt-4o",
        api_key: str | None = None) -> str:
    """OpenAI 챗봇 모델을 사용하여 응답을 생성합니다.

    Args:
        user_content (str): 사용자 입력 메시지.
        system_content (str | None, optional): 모델의 역할을 정의하는 시스템 메시지. Defaults to None.
        temperature (float, optional): 응답의 창의성/무작위성 (0.0 ~ 2.0). 0에 가까울수록 결정론적입니다. Defaults to 0.25.
        model (str | ChatModel, optional): 사용할 OpenAI 모델. Defaults to "gpt-4o".
        api_key (str | None, optional): OpenAI API 키. Defaults to None.

    Returns:
        str: 모델이 생성한 응답 메시지. 내용이 없을 경우 빈 문자열을 반환합니다.
    """
    messages = []
    if system_content: # 빈문자열도 아니고 None도 아닐 때
        messages.append({"role": "system", "content": system_content})
    messages.append({"role": "user", "content": user_content})
    
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature = temperature
    )
    
    content = response.choices[0].message.content
    return content if content else ""

def download_file(
    file_url: str, 
    filepath: str | None = None # default parameter
) -> None:
    res = requests.get(file_url)
    print("res ok :", res.ok)

    if filepath is None:
        filepath = os.path.basename(file_url)
        
    file_content = res.content

    dir_path = os.path.dirname(filepath)
    os.makedirs(dir_path, exist_ok=True)

    # 주의 : 같은 경로일 경우, 덮어쓰기가 된다.
    with open(filepath, "wb") as f:
        f.write(file_content)
        print("saved", filepath)

def multiply(a: float, b: float) -> float:
    """두 개의 숫자를 곱한 결과를 반환합니다.

    Args:
        a (float): 첫 번째 숫자.
        b (float): 두 번째 숫자.

    Returns:
        float: a와 b를 곱한 결과.
    """
    return a * b