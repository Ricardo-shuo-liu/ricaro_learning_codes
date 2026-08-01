function dig(x)
    dict = Dict()
    for item in x
        dict[x] = get(dict,item,0) + 1
    end

    return dict
end


sex = ["F", "M", "M", "F", "M"]

dict = dig(sex)
@show dict
