# -*- coding: utf-8 -*-
from . import calc

def get_help_summary(client, message):
    session = calc.Session()
    return (
        "Calculator",
        (
            "`!calc <math> [;<math>]` will perform calculations; the equation-format is the common scholastic standard.",
            "`<math>` can be variable-assignment (`x = 22 * sqrt(9)`), functions (`f(x) = x * 2`), or expressions (`x + 2 / f(7)`); the order in which these are supplied does not matter, but at least one expression must be performed to produce output.",
            "Built-in operators: {}".format(', '.join('`{}`'.format(i) for i in ('+', '-', '*', '/', '\\', '^', '%', '<', '>',))),
            "Built-in functions: {}".format(', '.join('`{}`'.format(i) for i in (session.listFunctions()))),
            "Built-in constants: {} (`?` is used for linear-equation-solving)".format(', '.join('`{}`'.format(i) for i in (session.listVariables()))),
            "Linebreaks can be used in place of semicolons for readability.",
            "Function parameters must be scalars or variables; directly nesting a function will prevent expression-compilation.",
        ),
    )

def _try_int(value):
    try:
        int_value = int(value)
        if int_value == value:
            return "{:,}".format(int_value)
    except Exception:
        pass
    return "{:,.10f}".format(value).rstrip('0')

async def handle_message(client, message):
    if message.content.startswith(('!calc ', '!calc\n')):
        request = message.content[6:]
        request_lower = request.lower()
        
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
