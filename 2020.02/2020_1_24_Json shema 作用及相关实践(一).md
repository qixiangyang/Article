###  Json Schema 是什么？

Json Schema 是用来描述 Json 数据格式的一种描述性文件。

```
Json Schema 定义了一套词汇和规则，这套词汇和规则用来定义Json元数据，且元数据也是通过Json数据形式表达的。
Json元数据定义了Json数据需要满足的规范，规范包括成员、结构、类型、约束等。
```
参考链接：
https://www.cnblogs.com/terencezhou/p/10474617.html

它本身就是一个 Json 文件，格式如下：

```
{ 
    "type": "object",
    "properties": {
        "city": { "type": "string" },
        "number": { "type": "number" },
        "user": { 
            "type": "object",
            "properties": {
                "name" : {"type": "string"},
                "age" : {"type": "number"}
            }                       
        }
    }
}
```

### Json Schema 的用途是什么？

在接口开发中，有很多场景需要对请求的 Json 格式进行验证。

使用 Json Schema Validator，即可以通过 Json Schema 文件来验证请求 Json 数据的合法性。

避免在代码中，出现大量数据验证的逻辑。将数据验证逻辑与业务逻辑解耦，有助于开发者写出更清晰、更易维护的代码。


### 怎么写 Json Schema 文件？

一、 Json Schema 初体验

整体来看，Json Schema 是一个嵌套的 Json。他是通过分层来进行描述的。

在每一层，Json Schema 相对于原始的 Json 都会多一层描述性内容。

来看一个简单的例子：


```
# 原始 Json
{
    "city" : "chicago", 
    "number": 20
}

# Json Schema
{ 
    "type": "object",
    "properties": {
        "city": { "type": "string" },
        "number": { "type": "number" },                      
        }
}
```

可以看到，在 Schema 中，最外层先定义了这是一个 object 对象。 

然后通过 properties 定义了这个对象的属性，分别是 city 和 number。

对于者两个属性，由分别进行了定义，其中 city 的数据类型是 string，number 的类型为 number。

所以看起来 Json Schema 相比于原始的 Json 就是多了一层描述，并在 properties 中具体描述字段属性。

在来看一个嵌套 Json 的例子：

```
# 原始 Json
{
    "city" : "chicago", 
    "number": 20, 
    "user" : {
        "name":"Alex", 
        "age":20
        }
}

# Json Schema
{ 
    "type": "object",
    "properties": {
        "city": { "type": "string" },
        "number": { "type": "number" },
        "user": { 
            "type": "object",
            "properties": {
                "name" : {"type": "string"},
                "age" : {"type": "number"}
            }                       
        }
    }
}
```

在这个例子中， user 是一个嵌套的 Json 对象。

跟前面的表述一样，对于这个对象，对多一层描述，然后在 properties 中 描述具体的数据类型。

再来看一个 array 的类型的例子：


```
# 原始 Json
{
    "city": "chicago",
    "number": 20,
    "user": [
        {"name": "dick"},
        {"name": "eric"}
    ]

}
# Json Schema
{
    "type": "object",
    "properties": {
        "city": {"type": "string"},
        "number": {"type": "number"},
        "user": {
            "type": "array",
            "items": [
                {"type": "object",
                 "properties": {
                     "name": {"type": "string"}
                 }
                 }
            ]
        }
    }
}

```


### Python 中怎么使用 Json Schema Validator？
