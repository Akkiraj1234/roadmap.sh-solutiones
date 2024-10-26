import sys, os, json, time
location = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


class CILcolor:
    
    fg_color = {
        'black': '\x1b[30m',
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'yellow': '\x1b[33m',
        'blue': '\x1b[34m',
        'magenta': '\x1b[35m',
        'cyan': '\x1b[36m',
        'white': '\x1b[37m',         
        'none': '\x1b[39m',
        'b-black': '\x1b[90m',
        'b-red': '\x1b[91m',
        'b-green': '\x1b[92m',
        'b-yellow': '\x1b[93m',
        'b-blue': '\x1b[94m',
        'b-magenta': '\x1b[95m',
        'b-cyan': '\x1b[96m',
        'b-white': '\x1b[97m',
    }
    bg_color = {
        'black': '\x1b[40m',
        'red': '\x1b[41m',
        'green': '\x1b[42m',
        'yellow': '\x1b[43m',
        'blue': '\x1b[44m',
        'magenta': '\x1b[45m',
        'cyan': '\x1b[46m',
        'white': '\x1b[47m',         
        'none': '\x1b[49m',
        'b-black': '\x1b[100m',
        'b-red': '\x1b[101m',
        'b-green': '\x1b[102m',
        'b-yellow': '\x1b[103m',
        'b-blue': '\x1b[104m',
        'b-magenta': '\x1b[105m',
        'b-cyan': '\x1b[106m',
        'b-white': '\x1b[107m',
    }    
    
    def __init__(self) -> None:
        pass
    
    def color(self, string:str, color:str|tuple|list) -> str:
        return self.__check_color(string, color, self.fg_color, 38, 39) if color else string
    
    def style(self, string:str, color:str|tuple|list = None, background:str|tuple|list = None, bold:bool = False, italic:bool = False, underline:bool = False ) -> str:
        
        if color: string = self.__check_color(string, color, self.fg_color, 38, 39)
            
        if background: string = self.__check_color(string, background, self.bg_color, 48, 49)
        
        if bold: string = f"\x1b[1m{string}\x1b[0m"
        
        if italic: string = f"\x1b[3m{string}\x1b[0m"
        
        if underline: string = f"\x1b[4m{string}\x1b[0m"
            
        return string

    def __check_color(self,string, color:str, dict_:dict, code:int, code_end:int):
        
        if isinstance(color, tuple) or isinstance(color, list) and len(color) >= 2:
            ansi_code = f'\x1b[{code};2;{color[0]};{color[1]};{color[2]}m'
            string = f"{ansi_code}{string}\x1b[{code_end}m"
        
        elif isinstance(color, str):
            ansi_color_code = dict_.get(color, f"\x1b[{code_end}m")
            string = f"{ansi_color_code}{string}\x1b[{code_end}m"
            
        return string
Color = CILcolor()


class SyntaxError(Exception):
    def __init__(self, text = None, data_list = None, index:int = 0):
        error_message = ''
        
        if text:
            error_message+=f"{Color.color(text, 'red')}\n"
        
        if data_list:
            data_list[index] = Color.color(data_list[index], 'b-red')
            error_message += f"{Color.color('>>>', 'cyan')} {' '.join(data_list)}\n"
        
        len_ = lambda value: len(value) + 1
        lenght = sum(map(len_, data_list[:index])) if data_list else len(text) if text else 0
        error_message += f"{Color.color('>>>','cyan')} {'-'*lenght}^"
        
        super().__init__(error_message)


class Database_error(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Database:
    
    def __init__(self):
        self.database_name = 'Database.json'
        self.database_path = os.path.join(location, self.database_name)
        self.data = self._load()
    
    def _create(self) -> dict:
        try:
            with open(self.database_path, encoding="Utf-8", mode="w") as fp:
                fp.write("{}")
        except PermissionError as e:
            print(e)
        return {}
    
    def _load(self) -> dict:
        try:
            with open(self.database_path, mode="r", encoding='Utf-8') as fp:
                return json.load(fp)
        except (json.JSONDecodeError):
            return {}
        
        except (FileNotFoundError):
            return self._create()
        
    def _update(self, data:dict) -> None:
        try:
            with open(self.database_path, mode="w", encoding="utf-8") as fp:
                fp.write(json.dumps(data, ensure_ascii=False))
                
        except (FileNotFoundError, PermissionError) as e:
            raise Database_error(f"Error updating database: {e}")
    
    def _unique_id(self) -> int:
        try:
            # Get the last key and convert it to an integer, then increment by 1
            last_key = int(next(reversed(self.data)))
            unique_id = last_key + 1
        except (StopIteration, ValueError):
            # If dictionary is empty or last key isn't numeric, start from 0
            unique_id = 0
        
        return unique_id
    
    def Add(self,description:str) -> bool:
        data = {
            'description': description,
            'status': 'todo',
            'createdAt': time.time(),
            'updatedAt': time.time()
        }
        self.data[self._unique_id()] = data
        
        try: self._update(self.data)
        except Database_error: return False
        finally: return True
    
    def Delete(self, id_:int) -> dict|None:
        data = self.data.pop(id_, None)
        self._update(self.data)
        return data

    def Update(self, id_:int, description:str|None = None, status:str|None = None) -> None:
        if not id_ in self.data.keys():
            return False
        
        self.data[id_]['description'] = description if description else self.data[id_]['description']
        self.data[id_]['status'] = status if status else self.data[id_]['status']
        
        self._update(self.data)
    
    def Mark(self, id_:int, status:str) -> None:
        self.Update(id_, description=None, status=status)
    
    def List(self, filter = "All") -> list[dict]:
        # If the filter is "All", return all elements
        if filter.lower() == "all":
            return list(self.data.values())

        # Otherwise, filter items based on the `mark` field
        filtered_items = [item for item in self.data.values() if item.get("status") == filter]
        return filtered_items


class token:
    def __init__(self, argument:dict, fallback:dict|None, optiones:dict|None, method, help_text):
        self.argument = argument
        self.fallback = fallback
        self.optiones = optiones
        self.method = method
        self.help_text = help_text
    
    def generate_key(self, data_list: list) -> dict:
        if len(data_list) != len(self.argument):
            raise ValueError("Data list length must match argument keys length.")

        return {name: data for name, data in zip(self.argument.keys(), data_list)}


class Parser:
    def __init__(self, valid_keywords: dict):
        self.valid_keywords = valid_keywords
        
    def check_syntax(self, token: list | tuple) -> callable:
        
        #check if token[0] the operator is valid or not
        if not token[0].lower() in self.valid_keywords.keys():
            raise SyntaxError(text="Invalid command", data_list=token, index=0)
        
        #gathering important info
        args_provided = token[1:]
        validate = self.valid_keywords[token[0]]
        expected_args = list(validate.argument.keys())
        options = validate.optiones if validate.optiones is not None else {}
        fallbacks = validate.fallback if validate.fallback is not None else {}
        
        if len(args_provided) < len(expected_args):
            for missing_arg in expected_args[len(args_provided):]:
                if missing_arg in fallbacks:
                    args_provided.append(fallbacks[missing_arg])
                else:
                    raise SyntaxError(text=f"Missing required argument: {expected_args[len(args_provided)]}",data_list=token+['_______'],index=len(args_provided)+1)
        
        elif len(args_provided) > len(expected_args):
            raise SyntaxError(text="Too many arguments provided", data_list=token, index=len(token) - 1)
        
        
        for num, (arg, (arg_name, expected_type)) in enumerate(zip(args_provided, validate.argument.items())):
            
            #check if provided have sam eoption or not
            try:
                arg_cast = expected_type(arg)
            except ValueError:
                raise SyntaxError(text=f"Argument '{arg}' should be of type {expected_type.__name__}", data_list=token, index=num + 1)
            
            #check if options remain or not
            if arg_name in options:
                if not arg in options[arg_name]:
                    raise SyntaxError(text=f"Argument '{arg}' should be one of {options[arg_name]}", data_list=token, index=num + 1)
            
        
        return lambda: validate.method(**validate.generate_key(args_provided))
    
    def get(self):
        token = sys.argv[1:]
        if token == [] or None:
            return None
        
        if token[0].lower() == 'help':
            return self.help

        return self.check_syntax(token)

    def help(self) -> None:
        help_texts = []
        for keyword, tok in self.valid_keywords.items():
            # Highlighted command name and description
            command_name = Color.color(keyword, 'cyan')
            description = Color.color(tok.help_text, 'green')
            help_text = f"{command_name}: {description}\n"
            
            # Argument details with type, fallback, and options
            for arg_name, arg_type in tok.argument.items():
                arg_display = Color.color(arg_name, 'yellow')
                arg_type_display = Color.color(arg_type.__name__, 'blue')
                fallback_value = tok.fallback.get(arg_name, "None") if tok.fallback else "None"
                fallback_display = Color.color(fallback_value, 'magenta')
                
                # Options details if available
                options = tok.optiones.get(arg_name) if tok.optiones and arg_name in tok.optiones else None
                options_display = f"{Color.color(str(options), 'red')}" if options else "None"
                
                help_text += (
                    f"  - {arg_display} (Type: {arg_type_display}, "
                    f"Fallback: {fallback_display}, Options: {options_display})\n"
                )
            
            help_texts.append(help_text)
        
        return "\n".join(help_texts)


class Decorater:
    
    def __init__(self):
        pass


def main():
    database = Database()
    keywords = {
        'add': token(
            argument={'description': str},
            fallback=None,
            optiones=None,
            method=database.Add,
            help_text='Adds a new item with the specified description.'
        ),
        'update': token(
            argument={'id_': int, 'description': str},
            fallback=None,
            optiones=None,
            method=database.Update,
            help_text='Updates the item with the specified ID to the new description.'
        ),
        'delete': token(
            argument={'id_': int},
            fallback=None,
            optiones=None,
            method=database.Delete,
            help_text='Deletes the item with the specified ID.'
        ),
        'mark-in-progress': token(
            argument={'id_': int, 'status': str},
            fallback={'status': 'in-progress'},
            optiones=None,
            method=database.Mark,
            help_text='Marks the item with the specified ID as in-progress.'
        ),
        'mark-done': token(
            argument={'id_': int, 'status': str},
            fallback={'status': 'done'},
            optiones=None,
            method=database.Mark,
            help_text='Marks the item with the specified ID as done.'
        ),
        'list': token(
            argument={'filter': str},
            fallback={'filter': 'all'},
            optiones={'filter': ('done', 'todo', 'in-progress', 'all')},
            method=database.List,
            help_text='Lists items based on the specified filter.'
        ),
    }
    
    parser = Parser(keywords)
    decorater = Decorater()

    method_ = parser.get()
    if method_ is None:
        pass
    
    print(method_())


if __name__ == "__main__":
    main()