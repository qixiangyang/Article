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

在业务逻辑加入大量的数据验证的代码，会使得代码部分有很多额外的工作。

这时候就可以将数据验证的工作交给 Json Schema Validator， 由他来统一验证请求数据格式的合法性。

这样做的好处是，将数据验证逻辑与业务逻辑解耦，有助于开发者写出更清晰、更易维护的代码。

使用 Json Schema，必须会它的格式，下面就是对它介绍。


### 怎么写 Json Schema 文件？

整体来看，Json Schema 就是一个嵌套的 Json。

他是通过分层来进行描述数据格式的。在每一层，Json Schema 相对于原始的 Json 都会多一层描述性内容。

在这些描述行文件中，可以对数据的格式作出限制

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

当让，描述性的字段，不仅仅是 properties， 还有一些其他字段，比如 required 等，后面再介绍。

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

跟前面的表述一样，对于 user 这个对象，多一层描述，然后在 properties 中，描述了具体的数据类型。

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

在这个例子中，user 变成了一个 array 对象，它用来存放 object 对象。

同理根据 Json Schema 的规则，在每一层都对这些数据格式进行了描述。

这篇文章，主要是对 Json Schema 进行介绍，后面会有一篇文章专门介绍复杂的 Json Schema 写法。

### Python 中怎么使用 Json Schema Validator？

在 Python 中可以使用 jsonschema 包进行 Json 格式对验证。

以下代码是在 flask 中对 request 的 json 进行验证的 demo，请参考。

```
from jsonschema import validate

def parse_json(schema: dict) -> dict:
    body = flask.request.get_json(force=True)
    try:
        jsonschema.validate(body, schema)
    except Exception as e:
        raise ClientError(message="invalid json :[{0}].".format(repr(e)))
    else:
        return body
```