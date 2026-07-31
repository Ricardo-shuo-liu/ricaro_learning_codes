macro hello(x)
    # 打印传入的源代码表达式
    println("传入源码AST: ", x)
    # 返回一段执行代码：println(x的值)
    return :(println($x))
end

# 使用
a = "hello world"
@hello a

