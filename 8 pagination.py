#coding:utf-8
# for flask
# auth : daivlin
# date : 2020-02-22

class Pagination(object):
    '''
        分页类
        参数：
            per_page：每页数量
            total_data：总数目
            cur_page：当前页。
        用法：(flask，html中自定义css)
            py:
                page = int(request.args.get("page",1))  #获取args参数'page'
                per_page = 50   #每页的数量
                dsubAll = query_db("SELECT COUNT(id) AS C FROM dsub",one=True)["C"] #总数目
                pages = Pagination(cur_page=page,per_page=per_page,total_data=dsubAll)  #分页类
                dsub = query_db("SELECT * FROM dsub LIMIT ?,?",(pages.offset,pages.limit))  #取offset与limit进行分页
            html:
                <div>{{ pages.get_html() | safe }}</div>       
    '''
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
                    <li><a>首页</a></li> 
                    <li><a>上一页</a></li> 
                    <li><a>下一页</a></li> 
                    <li><a>尾页</a></li>
                </ul>
            '''
        elif self.page_current <= 1:
            html = '''
                <ul>
                    <li><a>首页</a></li> 
                    <li><a>上一页</a></li> 
                    <li><a href="?page={self.page_next}">下一页</a></li> 
                    <li><a href="?page={self.page_max}">尾页</a></li>
                </ul>
            '''.format(self=self)
        elif self.page_current >= self.page_max:
            html = '''
                <ul>
                    <li><a href="?page=1">首页</a></li> 
                    <li><a href="?page={self.page_pre}">上一页</a></li> 
                    <li><a>下一页</a></li> 
                    <li><a>尾页</a></li>
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
                        <li>
                            <a>第<code>{self.page_current}</code>页</a>
                        </li>
                        <li>
                            <a>共<code>{self.page_max}</code>页</a>
                        </li>
                    </ul>
                  '''.format(self=self)
        html = '<div class="pagination">{}</div>'.format(html + banner)
        
        if self.data_count > self.size:
            return html
        else:
            return ""
        
