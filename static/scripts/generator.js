var key_pressed=null;
var indent_spaces = 2;
$(document).ready(function()
{    
    $('#id_response_body').keyup(function()
    {
    clearTimeout(key_pressed);
    key_pressed = setTimeout(generate_jsd,500);       
   	});    
});

function generate_jsd()
{
    var $input = $('#id_response_body');
    var input = $input.val();
    var format =$('#id_response_format').val();
	if (format === 'application/json')
    {
    	try
    	{
        	eval("var my_javascript_object="+input+";");
        	$input.removeClass('error');
    	}
    	catch(e)
    	{
        	$input.addClass('error');        
        	return;
    	}
    }
    else{$input.removeClass('error');}
    prettyPrint();
}
// function parse(object, item_schema)
// {
    // if(item_schema === undefined)
        // item_schema = {};
    // var jsd_schema = item_schema;
//     
    // if(typeof(object) === 'string')
        // jsd_schema = parseString(object,jsd_schema);
    // else if(typeof(object) === 'number')
        // jsd_schema = parseNumber(object,jsd_schema);
    // else if(typeof(object) === 'boolean')
        // jsd_schema = parseBoolean(object,jsd_schema);
    // else if(object instanceof Array)
        // jsd_schema = parseArray(object,jsd_schema);
    // else if(object instanceof Function)
        // jsd_schema = parseFunction(object,jsd_schema);
    // else if(object instanceof Date)
        // jsd_schema = parseDate(object,jsd_schema);
    // else if(object instanceof Object)
        // jsd_schema = parseObject(object,jsd_schema);
        // /*
    // if(object instanceof Date)
        // return "date";
    // if(object instanceof Array)
        // return "string";*/
    // //return JSON.stringify(object,undefined,2);
//     
    // return jsd_schema;
// }
function parseString(object, jsd_schema)
{
    jsd_schema.Type = "String";
    return jsd_schema;
}

function parseNumber(object, jsd_schema)
{
    jsd_schema.Type = "Number";
    return jsd_schema;
}

function parseBoolean(object, jsd_schema)
{
    jsd_schema.Type = "Boolean";
    return jsd_schema;
}

function parseArray(object, jsd_schema)
{
    jsd_schema.Type = "Array";    
    var found_schemas=[];
    for(var i=0; i< object.length;i++)
    {
        if(jsd_schema.Values === undefined)
            jsd_schema.Values = [];            
        var item = object[i];
        var item_schema = parse(item);
        var schema_text = stringify(item_schema);        
        if(found_schemas.indexOf(schema_text)!=-1)
            continue;
        found_schemas.push(schema_text);
        jsd_schema.Values.push(item_schema);        
    }
    return jsd_schema;
}

function parseFunction(object, jsd_schema)
{
    jsd_schema.Type = "Function";
    return jsd_schema;
}

function parseDate(object, jsd_schema)
{
    jsd_schema.Type = "Date";
    return jsd_schema;
}

function parseObject(object, jsd_schema)
{
    jsd_schema.Type = "Object";    
    for(var i in object)
    {
        if(!object.hasOwnProperty(i))
            continue;            
        if(jsd_schema.Attributes === undefined)
            jsd_schema.Attributes = [];            
        var item = object[i];
        var item_schema = { Name: i };
        item_schema = parse(item, item_schema);
        jsd_schema.Attributes.push(item_schema);        
    }
    return jsd_schema;
}

function stringify(object, indent)
{
    indent = indent!==undefined?indent:0;
    var indentation = getIndentation(indent);
    var single_indent = getSingleIndent();
    
    var output="";
 
    if(typeof(object) === 'string')
        output += "\""+object+"\"";
    else if(typeof(object) === 'number')
        output += object.toString();
    else if(typeof(object) === 'boolean')
        output += object.toString();
    else if(object instanceof Array)
    {
        output += "\n"+indentation+"[\n";
        var first = true;
        var new_indent = indent+1;
        for(var i in object)
        {
            if(first)
                first=false;
            else
                output += ",\n";
                
            output += indentation + single_indent + stringify(object[i],new_indent);
        }
        output += "\n"+indentation+"]";
    }
    else if(object instanceof Object)
    {
        output +="{\n";
        var first = true;
        var new_indent = indent+1;
        for(var i in object)
        {
            if(!object.hasOwnProperty(i))
                continue;
            
            if(first)
                first=false;
            else
                output += ',\n';
              
            var item = object[i];
            
            output += indentation + single_indent +i+": ";
            output += stringify(item,new_indent);
        }
        output +="\n"+indentation+"}";
    }
    
    return output;
}

function getIndentation(indent_count)
{
    var indent = "";
    for(var i=0; i<indent_count*indent_spaces; i++)
    {
        indent+=" ";
    }
    return indent;
}

function getSingleIndent()
{
    var indent = "";
    for(var i=0; i<indent_spaces; i++)
    {
        indent+=" ";
    }
    return indent;
}





























