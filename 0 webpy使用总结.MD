
## 子应用
1. 子应用中，web.ctx.fullpath是剥离了主应用的path，如果设置url（如：分页url，判断登陆转到主页）时，需手动设置：加上子应用前缀，或将web.ctx.fullpath改为web.ctx.homedomain。
2. web.seeother与web.ctx有关，注意路径问题。

## UTC时间差
```
import datetime
#服务器时间转化为当前时间
timenow = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
currentTime = timenow.strftime("%Y-%m-%d %H:%M")
```
## 设置csrf_token
1. 后台
```
#设置csrf_token
def  csrf_token():
    if "csrf_token" not in web.ctx.session:
        from uuid import uuid4
        web.ctx.session.csrf_token = uuid4().hex
    return web.ctx.session.csrf_token

#判断csrf_token
if not ("csrf_token" in i and i.csrf_token == web.ctx.session.pop('csrf_token',None)):
    raise web.HTTPError(
        "400 Bad request",{"content-type":"text/html"},"""Cross-site request forgery(CSRF) attempt"""
    )
```
2. 前端（在form中）
```
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
```
## 其他
1. 富文本编辑器nicedit使用:在表单验证里，如果设置nicedit不能为空。输入无效，不能提交表单，这个bug待修复。
2. POST提交后，用raise 重定向
