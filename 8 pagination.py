# coding:utf-8
# simple pagination 
# auth : daivlin
# date : 2020-02-22

class Pagination(object):
    '''分页类'''
    def __init__(self,per_page=5,total_data=10,cur_page=1):
        import math
        self.size = per_page
        self.data_count = total_data
        self.page_current = int(cur_page)
        self.page_max = int(math.ceil(self.data_count * 0.1 * 10 / self.size ))

        self.page_current = 1 if self.page_current < 1 else self.page_current
        self.page_current = self.page_max if self.page_current > self.page_max else self.page_current
            
        self.offset = ( self.page_current - 1) * self.size
        self.limit = self.size
        
    def get_html(self):
        self.page_pre = self.page_current - 1
        self.page_next = self.page_current + 1
        if self.page_max in (0,1) :
            html = '''
                <ul>
                    <li class="disabled"><a>首页</a></li> 
                    <li class="disabled"><a>上一页</a></li> 
                    <li class="disabled"><a>下一页</a></li> 
                    <li class="disabled"><a>尾页</a></li>
                </ul>
            '''
        elif self.page_current <= 1:
            html = '''
                <ul>
                    <li class="disabled"><a>首页</a></li> 
                    <li class="disabled"><a>上一页</a></li> 
                    <li><a href="?page={self.page_next}">下一页</a></li> 
                    <li><a href="?page={self.page_max}">尾页</a></li>
                </ul>
            '''.format(self=self)
        elif self.page_current >= self.page_max:
            html = '''
                <ul>
                    <li><a href="?page=1">首页</a></li> 
                    <li><a href="?page={self.page_pre}">上一页</a></li> 
                    <li class="disabled"><a>下一页</a></li> 
                    <li class="disabled"><a>尾页</a></li>
                </ul>   
            '''.format(self=self)
        else:
            html = '''
                <ul>
                    <li><a href="?page=1">首页</a></li> 
                    <li><a href="?page={self.page_pre}">上一页</a></li> 
                    <li><a href="?page={self.page_next}">下一页</a></li> 
                    <li><a href="?page={self.page_max}">尾页</a></li>
                </ul>
            '''.format(self=self)
        banner = '''
                    <ul>
                        <li class="disabled">
                            <a>第<code>{self.page_current}</code>页</a>
                        </li>
                        <li class="disabled">
                            <a>共<code>{self.page_max}</code>页</a>
                        </li>
                    </ul>
                  '''.format(self=self)
        html = '<div class="pagination">{}</div>'.format(html + banner)
        
        if self.data_count > self.size:
            return html
        else:
            return ""
        
