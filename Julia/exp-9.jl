mutable struct Rectangle
    xll::Real 
    yll::Real 
    width::Real
    height::Real 
end

function (rect::Rectangle,offset)
    Rectangle(rect.xll + offset[1], 
        rect.yll + offset[2],
        rect.width, rect.height)
end
