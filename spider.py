# os
import os
# requests
import requests
# from lxml, import html
from lxml import html

# global
global_page_num = 0;

# e.g. num == 2
def get_page_number(num):
    #构建函数，用来查找该页内所有图片集的详细地址。目前一页包含15组套图，所以应该返回包含15个链接的序列。
    # e.g. http://www.mmjpb.com/home/2
    url = 'http://www.mmjpg.com/home/' + num
    #构造每个分页的网址
    # requests, get url, content vs text
    response = requests.get(url).content
    #调用requests库，获取二进制的相应内容。
    #注意，这里使用.text方法的话，下面的html解析会报错，大家可以试一下。
    #这里涉及到.content和.text的区别了。简单说，如果是处理文字、链接等内容，建议使用.text，
    #处理视频、音频、图片等二进制内容，建议使用.content。
    # html form_string, response === selector....
    selector = html.fromstring(response)
    # 使用lxml.html模块构建选择器，主要功能是将二进制的服务器相应内容response转化为可读取的元素树（element tree）。
    # lxml中就有etree模块，是构建元素树用的。如果是将html字符串转化为可读取的元素树，
    # 就建议使用lxml.html.fromstring，毕竟这几个名字应该能大致说明功能了吧。
    # url array
    urls = []
    #准备容器
    # forloop i in selector_xpath
    # ul li a @href
    for i in selector.xpath("//ul/li/a/@href"):
    # url appends... to url array
    #利用xpath定位到所有的套图的详细地址
        urls.append(i)
        #遍历所有地址，添加到容器中
    # return ...urls...
    return urls
    #将序列作为函数结果返回


# get title with url
def get_image_title(url):
    #现在进入到套图的详情页面了，现在要把套图的标题和图片总数提取出来
    # res === requests, get url, content
    response = requests.get(url).content
    # selector == html, form_string(res)
    selector = html.fromstring(response)
    # img_title = selector.xpath, //h2/text(), [0]
    image_title = selector.xpath("//h2/text()")[0]
    #需要注意的是，xpath返回的结果都是序列，所以需要使用[0]进行定位
    # get title
    return image_title

def get_image_amount(url):
    #这里就相当于重复造轮子了，因为基本的代码逻辑跟上一个函数一模一样。想要简单的话就是定义一个元组，然后把获取标题、获取链接、获取图片总数的3组函数的逻辑揉在一起，最后将结果作为元组输出。不过作为新手教程，还是以简单易懂为好吧。想挑战的同学可以试试写元组模式
    response = requests.get(url).content
    selector = html.fromstring(response)
    image_amount = selector.xpath("//div[@class='page']/a[last()-2]/text()")[0]
    # a标签的倒数第二个区块就是图片集的最后一页，也是图片总数，所以直接取值就可以
    return image_amount


# get img detail website url
def get_image_detail_website(url):
    #这里还是重复造轮子。
    # with content return res
    response = requests.get(url).content
    # html form string ....
    selector = html.fromstring(response)
    # detail array
    image_detail_websites = []
    # selector xpath
    # img_amount, selector, path, div -> div class=page -> a[last-2] -> text, [0]
    image_amount = selector.xpath("//div[@class='page']/a[last()-2]/text()")[0]
    #这里重复构造变量，主要是为了获取图片总数。更高级的方法是使用函数间的传值，但是我忘了怎么写了，所以用了个笨办法。欢迎大家修改
    #构建图片具体地址的容器
    for i in range(int(image_amount)):
        # for i in img_amount
        #
        image_detail_link = '{}/{}'.format(url, i+1)

        # test print
        #print('--- test ---')
        #print(url)
        #print(image_detail_link)


        # res
        response = requests.get(image_detail_link).content

        # selector
        sel = html.fromstring(response)
        # div class=content -> a -> img -> @src, [0]
        image_download_link = sel.xpath("//div[@class='content']/a/img/@src")[0]
        #这里是单张图片的最终下载地址
        #append
        image_detail_websites.append(image_download_link)
    return image_detail_websites


# write to file
def download_image(image_title, image_detail_websites):
    #将图片保存到本地。传入的两个参数是图片的标题，和下载地址序列
    # num == 1
    num = 1
    # amount === len
    amount = len(image_detail_websites)
    #获取图片总数
    # forloop
    for i in image_detail_websites:
        # file name
        filename = 'img/%s/%s%s.jpg' % (global_page_num, image_title, num)

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # downloading
        print('Downloading: %s - %s/%s total，' % (image_title, num, amount))
        # open file
        with open(filename, 'wb') as f:
            # f write
            f.write(requests.get(i).content)
        num += 1

# if it is main program
if __name__ == '__main__':
    # input, page_number
    page_number = input('Please enter the page number that you want to scrape:')

    # global_page_num
    global_page_num = page_number;

    # forloop each link in get_page_number
    for link in get_page_number(page_number):
        # download image
        # get image_title, link
        # get_img_detail_website, link
        download_image(get_image_title(link), get_image_detail_website(link))
