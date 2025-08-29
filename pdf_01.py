from dataclasses import dataclass
import PyPDF2

# key가 고정된 dict를 반환할 때, dataclass를 대신 써보세요.
@dataclass
class Document:
    title: str
    author: str
    subject: str
    page_content_list: list[str]

# 들여쓰기(Indentation)
def get_pdf_info(pdf_path: str) -> Document:
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        title = reader.metadata.get("/Title","")
        author = reader.metadata.get("/Author","")
        subject = reader.metadata.get("/Subject","")

        page_content_list = []
        reader = PyPDF2.PdfReader(f)
        for page_no, page in enumerate(reader.pages, start=1):
            page_content: str = page.extract_text()
            page_content_list.append(page_content)
            # print(f"##페이지 {page_no} ##")
            # print(page_content)
            # print()

        # return{
        #     "title": title,
        #     "author": author,
        #     "subject": subject,
        # }
        return Document(
            title = title, # 속성명 = 값
            author =author,
            subject = subject,
            page_content_list=page_content_list
        )
    
def main():
    pdf_path = "./PDFs/sample2.pdf"
    document = get_pdf_info(pdf_path)
    print("title :", repr(info["title"]))

main()