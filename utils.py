import os
import requests

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