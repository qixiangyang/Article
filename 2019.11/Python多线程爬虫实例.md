### 多线程能解决什么问题？

众所周知，GIL的存在使得Python（CPython）的多线程是不完整的，仅在 I/O 密集型的任务中才能发挥部分功效，计算密集型的就指望不上了。

而另一方面，爬虫就是一个典型的 I/O 密集型的应用，使用多线程还是能提升不少的效率的。

下面尝试从一个菜鸡的经验来阐释多线程及多线程的爬虫写法。

### 理解多线程

#### 理解多线程需要先理解阻塞

什么是阻塞呢？

对于一个爬虫任务来讲，有网络请求、数据计算、数据存储等步骤，其中网络请求和数据存储就是阻塞的。

怎么来理解呢，计算机发出一个网络请求后，需要对方服务器响应并传输数据。

对于一个普通程序，这时候就进入阻塞的状态了，因为这时候程序需要等待对方服务器传输完所有的数据后，才能进行下一步的计算操作。

这种等待的状态就是阻塞。同理，存储也是一个阻塞过程。

毫无疑问，阻塞会造成计算资源的浪费。多线程就是为了减少阻塞造成的等待时间,提升程序运行的效率。

#### 多线程是怎样提升效率的？

用一个生活经验来看待阻塞问题。当一件事情需要等待的时候，我们就会去做下一件事情，等这个事情完成了，我们在回来解决他，这就是多线程的思路。

在程序世界里，多线程也是相似的，当网络阻塞时，就去请求下一个资源、下下一个资源，直到有完整的网络请求返回来，再去处理处理返回的数据。

通过多线程，一组任务可以被多个人并行执行，效率自然快很多了。

### 多线程最佳应用场景

在 Python（CPython）多线程中，当遇到遇到 I/O 请求时，当前线程会被挂起，等待任务状态完成时，线程调度会重启该线程。

何为 I/O 操作？

可以从三个角度来理解：



参考：https://www.jianshu.com/p/fa7bdc4f3de7

对于爬虫来讲，主要就是网络请求和数据写入。所以爬虫很适合用多线程来进行操作。

### 一个多线程爬虫实例

一组任务要被多个人执行，一个朴素的思想就是把任务按照人头数平分，然后交给这几个人。最后一个人做完，整个任务就算完成了。

按照这个朴素的想法，写出了下面这段代码。

```
import threading
import requests
from lxml import etree

url = 'https://qixiangyang.cn/'
headers = {'cookie': 'test_thread'}
def get_data(index, x):
    res = requests.get(url, headers=headers)
    print('线程ID：{} 任务ID：{} 请求状态：{}'.format(index, x, res.status_code))
    # time.sleep(1)
    return res.text


def get_title(index, text_info, x):
    page_dom = etree.HTML(text_info)
    title_list = page_dom.xpath('/html/body/div/div/div[1]/div/h2/a/text()')
    print('线程ID：{} 任务ID：{} 结果：{}'.format(index, x, str(title_list)))
    return title_list


def main(index, task_id_list_seg):

    for x in task_id_list_seg:
        text_info = get_data(index, x)
        get_title(index, text_info, x)


task_id_list = list(range(101, 200))
seg = 10
ths = []

for _ in range(seg):
    th = threading.Thread(target=main, args=(_, task_id_list[_*seg: (_+1)*seg]))
    th.start()
    ths.append(th)

for th in ths:
    th.join()
```

"""
对待爬取的url种子进行分片，然后每个线程取特定的分片里的数据。
This is work, 但是需要更加 Pythonic 的方式。就是使用队列，。
deque 是线程安全的。勘误不是
deque.Queue 是线程安全的
参考地址：https://juejin.im/post/5b129a1be51d45068a6c91d4
deque 双向队列
Queue 先进先出队列 FIFO
"""


```
import threading
import requests
import time
from lxml import etree
from queue import Queue


class SpiderTest:
    url = 'https://qixiangyang.cn/'
    headers = {'cookie': 'test_thread'}

    def __init__(self, id_list, nums):
        self.id_list = id_list
        self.nums = nums
        self.q = Queue(len(id_list))

    def get_url(self):
        for _ in self.id_list:
            self.q.put(_)

    def get_data(self, index, x):
        res = requests.get(self.url, headers=self.headers)
        print('线程ID：{} 任务ID：{} 请求状态：{}'.format(index, x, res.status_code))
        return res.text

    @staticmethod
    def get_title(index, text_info, x):
        page_dom = etree.HTML(text_info)
        title_list = page_dom.xpath('/html/body/div/div/div[1]/div/h2/a/text()')
        print('线程ID：{} 任务ID：{} 结果：{}'.format(index, x, str(title_list)))
        return title_list

    def get_info(self, t_num):
        while not self.q.empty():
            x = self.q.get()
            text_info = self.get_data(t_num, x)
            self.get_title(t_num, text_info, x)

    def run(self):
        self.get_url()
        ths = []
        for _ in range(self.nums):
            th = threading.Thread(target=self.get_info, args=(_,))
            th.start()
            ths.append(th)
        for th in ths:
            th.join()


url_id = list(range(101, 200))
a = SpiderTest(url_id, 20)
a.run()
```