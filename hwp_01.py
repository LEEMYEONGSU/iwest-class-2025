import os
import subprocess

def find_업무분장_hwp_files(base_path: str):
    """
    지정 경로 내의 모든 하위 디렉토리에서
    파일명에 '업무분장'이 포함되고 확장자가 .hwp인 파일의 경로를
    리스트로 반환합니다.
    """

    hwp_files = []
    for root, __, files in os.walk(base_path):
        for filename in files:
            if "업무분장" in filename and filename.lower().endswith(".hwp"):
                # full_path = os.path.join(dirpath, filename)
                # hwp_files.append(full_path)
                hwp_files.append(os.path.join(root, filename))
    return hwp_files

def run_convert_cmd(hwp_path: str):
    output_path = os.path.splitext(hwp_path)[0] + ".html"
    cmd = [
        "hwp5html", "--html", "--output", output_path, hwp_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
      raise RuntimeError(f"명령 실행 실패: {result.stderr}")
    else:
      print(f"변환 성공: {output_path}")

def main():
    hwp_files = find_업무분장_hwp_files(".")
    print("찾은 업무분장 hwp 파일들:", hwp_files)
    for hwp_path in hwp_files:
        # html_path = run_convert_cmd(hwp_path)
        html_str = hwp_to_html(hwp_path=hwp_path)
        print("created")
        print(html_str)  # 앞 500자만 출력
main() 