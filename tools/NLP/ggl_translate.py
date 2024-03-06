import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

# https://okumuralab.org/~okumura/python/urldecode.html
class GoogleTranslate:
    def __init__(self, jp_txt):
        self.url = f'https://translate.google.com/?hl=en&sl=ja&tl=en&text={requests.utils.quote(jp_txt)}&op=translate'
        self.driver = webdriver.Chrome()
        self.soup = None

    def _update_soup(self, sec=0):
        self.driver.get(self.url)
        sleep(sec)
        html = self.driver.page_source
        self.soup = BeautifulSoup(html, 'html.parser')

    def _parse_content(self):
        block = self.soup.findAll("div", {"class": 'OPPzxe'})[0]
        translated_block = block.findAll("div", {"class": 'lRu31'})[0]
        translated_block = translated_block.findAll("span", {"class": 'HwtZe'})[0]
        spans = translated_block.findAll("span", {"class": 'ryNqvb'})
        input_block = block.findAll("textarea")[0]
        original = input_block.contents[0]

        translated_word = []
        for row in spans:
            if isinstance(row.contents[0], str):
                translated_word.append(row.contents[0])
        return ''.join(translated_word), original

    def run(self, sec=0):
        self._update_soup(sec)
        translated, original = self._parse_content()
        print(translated)
        print(original)


if __name__ == '__main__':
    jp = '''
          NY原油先物8月限（WTI）（終値）
    1バレル＝72.53（+1.34　+1.88%）
    　ニューヨーク原油は反発。終値の前営業日比（速報値）は期近２限月は１．３４ドル高。その他の限月は０．０４～１．３４ドル高。
    　パウエル米連邦準備制度理事会（ＦＲＢ）議長の証言から最終的な金利水準に接近していることが示唆され、ドル安に振れたことが買い手がかりとなった。パウエルＦＲＢ議長は目標を達成する金利水準は不明としながらも、「金利は年末までに幾分高くなると当局者はみている」、「もっと緩やかなペースで金利を上げるのが理に適っている公算」と述べ、目標に向けて利上げペースが一段と鈍化していくこととの認識を示した。とうもろこし価格が急伸しており、バイオ燃料の混合率低下が石油需要を押し上げる可能性があることも支援要因。
    　時間外取引で８月限は前日終値付近で推移し、方向感は限定的だった。ただ、通常取引開始後は買いが優勢となり７２．７２ドルまで上げた。
    '''
    cls = GoogleTranslate(jp)
    cls.run()


a = '''パウエルＦＲＢ議長は目標を達成する金利水準は不明としながらも、「金利は年末までに幾分高くなると当局者はみている」、「もっと緩やかなペースで金利を上げるのが理に適っている公算」と述べ、目標に向けて利上げペースが一段と鈍化していくこととの認識を示した。とうもろこし価格が急伸しており、バイオ燃料の混合率低下が石油需要を押し上げる可能性があることも支援要因。
　時間外取引で８月限は前日終値付近で推移し、方向感は限定的だった。ただ、通常取引開始後は買いが優勢となり７２．７２ドルまで上げた。'''
b = '''パウエルＦＲＢ議長は目標を達成する金利水準は不明としながらも、「金利は年末までに幾分高くなると当局者はみている」、「もっと緩やかなペースで金利を上げるのが理に適っている公算」と述べ、目標に向けて利上げペースが一段と鈍化していくこととの認識を示した。とうもろこし価格が急伸しており、バイオ燃料の混合率低下が石油需要を押し上げる可能性があることも支援要因。
　時間外取引で８月限は前日終値付近で推移し、方向感は限定的だった。ただ、通常取引開始後は買いが優勢となり７２．７２ドルまで上げた。'''


c = '''
Fed Chairman Jerome Powell said it was unclear what level of interest rates would hit his target, but "officials expect rates to rise somewhat by the end of the year," adding that "a more gradual pace of rate hikes likely makes sense." '', acknowledging that the pace of interest rate hikes will slow further toward the target. Soaring corn prices and the potential for lower biofuel mixes to boost oil demand are also supportive.
In after-hours trading, the August contract was near the previous day's closing price, and the sense of direction was limited. However, after the start of normal trading, buying dominated and the price climbed to $72.72.
'''

d = '''
While Powell FRB is unknown the interest rate level to achieve the goal, "the authorities see that the interest rate is somewhat higher by the end of the year", and "it is easy to raise interest rates at a more gentle pace. He said that the interest rate hike would slow down for the goal. It is also a support factor that corn prices are growing rapidly, and the decrease in mixture of biofuels may boost the demand for oil.
The August limit was overtime, and the direction was limited to the closing price of the previous day, and the sense of direction was limited. However, after the start of normal transactions, buying was dominant and increased to $ 72.72.
'''
