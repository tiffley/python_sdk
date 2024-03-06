from tika import parser


fn = "ana.pdf"

tg = ['quality by enabling an organization']
# tg = ['仙台', '羽田']

target_page = 1


def parse(fn) -> list:
    raw_xml = parser.from_file(fn, xmlContent=True)
    body = raw_xml['content'].split('<body>')[1].split('</body>')[0]
    body_without_tag = body.replace("<p>", "").replace("</p>", "").replace("<div>", "").replace("</div>", "").replace(
        "<p />", "")
    text_pages = body_without_tag.split("""<div class="page">""")[1:]
    return text_pages

def find_by_and(text_pages, tg):
    for page in text_pages:
        for row in page.split('\n'):
            if all(e in row for e in tg):
                print(row)

def find_by_or(text_pages, tg):
    for page in text_pages:
        for row in page.split('\n'):
            if any(e in row for e in tg):
                print(row)

def show_target_page(target_page):
    num_pages = len(text_pages)
    print(text_pages[target_page-1])

def bricks(text_pages, tg):
    for page in text_pages:
        for row in page.split('Question'):
            if all(e in row for e in tg):
                print(row)


if __name__ == '__main__':
    text_pages = parse(fn)
    # print(text_pages)
    # bricks(text_pages, tg)
    # find_by_and(text_pages, tg)
    # find_by_or(text_pages, tg)
    show_target_page(target_page)
