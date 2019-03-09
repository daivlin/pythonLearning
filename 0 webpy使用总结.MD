
## 子应用
1. 子应用中，web.ctx.fullpath是剥离了主应用的path，如果设置url（如：分页url，判断登陆转到主页）时，需手动设置：加上子应用前缀，或将web.ctx.fullpath改为web.ctx.homedomain。
2. web.seeother与web.ctx有关，注意路径问题。
