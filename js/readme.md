### Lodash
内部封装了诸多对字符串、数组、对象等常见数据类型的处理函数

- Array，适用于数组类型，比如填充数据、查找元素、数组分片等操作
- Collection，适用于数组和对象类型，部分适用于字符串，比如分组、查找、过滤等操作
- Function，适用于函数类型，比如节流、延迟、缓存、设置钩子等操作
- Lang，普遍适用于各种类型，常用于执行类型判断和类型转换
- Math，适用于数值类型，常用于执行数学运算
- Number，适用于生成随机数，比较数值与数值区间的关系
- Object，适用于对象类型，常用于对象的创建、扩展、类型转换、检索、集合等操作
- Seq，常用于创建链式调用，提高执行性能（惰性计算）
- String，适用于字符串类型



### query-string
/**
 * query-string: 
 * Parse and stringify URL query strings
 * https://www.npmjs.com/package/query-string
 * parse: 对?\#\Array格式的查询字符串进行格式化，返回object
 * stringify：跟parse api相反的作用
 * extract：Extract a query string from a URL that can be passed into .parse() . 通常这样的查询字符串是通过location对象获取的
 * parseUrl：Extract the URL and the query string as an object.
 * 
 */


 ### axios 
- 从浏览器中创建 XMLHttpRequest
- 从 node.js 发出 http 请求
- 支持 Promise API
- 拦截请求和响应
- 转换请求和响应数据
- 取消请求
- 自动转换JSON数据
- 客户端支持防止 CSRF/XSRF
