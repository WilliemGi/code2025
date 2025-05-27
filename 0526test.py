# 使用 requests 工具
import requests as req

# 使用 beautifulsoup4 工具
from bs4 import BeautifulSoup as bs

# 使用 regex 工具
import re

# 執行 command 的時候用的
import os

# 使用 GET 方式下載古騰堡網站的中文書籍列表
res = req.get('https://www.gutenberg.org/browse/languages/zh')

# 指定 lxml 作為解析器
soup = bs(res.text, "lxml") 
# 取得所有的 <li.pgdbetext> a[href]> 元素

# 建立 list 來放置列表資訊
list_posts = []

#把「標籤內容」變成純文字 list
result = soup.select('li.pgdbetext > a[href]')

# 建立資料夾（如果還沒存在）
folderPath = 'project_gutenberg'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

# 走訪每一個 <li> 標籤，利用正規表達式來過濾掉英數字的書籍
for tag in result:
    # [^a-zA-Z0-9]+ 代表非英數字的字元
    # 這裡的意思是要過濾掉英數字的書籍
    regex = r'[^a-zA-Z0-9]+'
    match = re.match(regex, tag.text)
    if  match == None:
        # 如果沒有符合的話，就跳過
        continue
    else:    # 如果有符合的話，就印出來
        title_clean = re.sub(r'[\r\n\\/:*?"<>|]', '', tag.get_text().strip())
        list_posts.append({
            'title': title_clean,
            'link': 'https://www.gutenberg.org' + tag['href']
        })
        #加入列表資訊 
        
# 走訪每一個 <li> 標籤，到網頁內面去取得書籍的資訊
for index, obj in enumerate(list_posts):
    res_ = req.get(obj['link'])
    soup_ = bs(res_.text, "lxml")
    
    #取得第二個網址
    result_ = soup_.select('td.unpadded.icon_save > a[href]')[0]
    alink = 'https://www.gutenberg.org' + result_['href']
    page_res = req.get(alink)
    page_soup = bs(page_res.text, "lxml")
    # 抓正文 → 通常在 body 裡
    page_text = page_soup.select('body')[0]
    text_content = page_text.get_text(separator='\n', strip=True)
    regex_chinese = r"[\u4e00-\u9fff\u3000-\u303F\uFF00-\uFFEF]+"
    
    onlychinese = re.findall(regex_chinese, text_content)
    joined_content = ''.join(onlychinese)
    clean_content = joined_content.replace('\u3000', ' ')
    
     # 正規表達式 - 中文與全形標點
        
    # strip=True 會去除掉前後的空白字元
    # 這裡的 separator 是用來分隔每一行的

    # 設定檔案路徑，檔名用 title，加副檔名 .txt
    file_path= os.path.join(folderPath, f"{obj['title']}.txt")
    # 寫入檔案 (以文字方式)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(clean_content))
    print(f"{obj['title']} 已下載完成！")

    

