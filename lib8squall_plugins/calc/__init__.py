# -*- coding: utf-8 -*-
from . import calc

HELP_SUMMARY = "`!calc help` to learn how I can crunch numbers for you."

def _try_int(value):
    try:
        int_value = int(value)
        if int_value == value:
            return int_value
    except Exception:
        pass
    return value

async def handle_message(client, message):
    if message.content.startswith(('!calc ', '!calc\n')):
        request = message.content[6:]
        request_lower = request.lower()
        
        if request_lower == 'list':
            session = calc.Session()
            
            output = []
            output.append("Built-in operators:")
            output.append("`{}`".format(',  '.join(('+', '-', '*', '/', '\\', '^', '%', '<', '>'))))
            output.append("Built-in functions:")
            output.append("`{}`".format(',  '.join(session.listFunctions())))
            output.append("Built-in variables:")
            output.append("`{}`".format(',  '.join(session.listVariables())))
            
            await message.reply('\n'.join(output))
        elif request_lower == 'help':
            await message.reply('\n'.join((
                "`!calc <variable | function | equation>[; ...][\\n ...] | list`",
                "The order of input does not matter.",
                "",
                "Function parameters must be scalars or variables;",
                "directly nesting a function will prevent compilation.",
            )))
        else:
            try:
                session = calc.Session(request.replace('\n', ';'))
                (variables, equations) = session.evaluate()
                
                if equations:
                    output = []
                    output.extend("- `{} = {}`".format(name, _try_int(value)) for (name, value) in variables)
                    output.extend("`{}` = `{}`".format(equation, _try_int(value)) for (equation, value) in equations)
                    await message.reply('\n'.join(output))
                else:
                    await message.reply("No expressions provided.")
            except Exception as e:
                await message.reply("Something went wrong. {}: {}".format(
                    e.__class__.__name__,
                    e,
                ))
                raise
        return True
    return False
