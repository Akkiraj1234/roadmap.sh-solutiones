import sys, os, json, time
location = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
# verstion 1.0

class CILcolor:
    """
    A class for handling text styling with foreground and background colors, as well as basic text styles (bold, italic, underline) for terminal output.
    Supports both named ANSI colors and RGB values for custom color application.
    """
    
    # ANSI escape codes for foreground colors
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

    # ANSI escape codes for background colors
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
        """Initializes an instance of the CILcolor class, preparing the ANSI color and style management methods."""
        pass

    def color(self, string: str, color: str | tuple | list) -> str:
        """
        Applies a foreground color to the given string.

        Parameters:
            string (str): The text to color.
            color (str | tuple | list): The name of the color (as a key in fg_color) or an RGB tuple/list.

        Returns:
            str: The colored string with ANSI escape codes.
        """
        return self.__check_color(string, color, self.fg_color, 38, 39) if color else string

    def style(self, string: str, color: str | tuple | list = None, background: str | tuple | list = None, bold: bool = False, italic: bool = False, underline: bool = False) -> str:
        """
        Applies multiple styles (foreground color, background color, bold, italic, underline) to the given string.

        Parameters:
            string (str): The text to style.
            color (str | tuple | list, optional): Foreground color as a name or RGB tuple/list.
            background (str | tuple | list, optional): Background color as a name or RGB tuple/list.
            bold (bool, optional): If True, applies bold styling.
            italic (bool, optional): If True, applies italic styling.
            underline (bool, optional): If True, applies underline styling.

        Returns:
            str: The styled string with ANSI escape codes.
        """
        if color: string = self.__check_color(string, color, self.fg_color, 38, 39)
        if background: string = self.__check_color(string, background, self.bg_color, 48, 49)
        if bold: string = f"\x1b[1m{string}\x1b[0m"
        if italic: string = f"\x1b[3m{string}\x1b[0m"
        if underline: string = f"\x1b[4m{string}\x1b[0m"
        return string

    def __check_color(self, string: str, color: str | tuple | list, dict_: dict, code: int, code_end: int) -> str:
        """
        Converts a color name or RGB tuple to an ANSI color escape code and applies it to the given string.

        Parameters:
            string (str): The text to color.
            color (str | tuple | list): Color name (str) or RGB values (tuple or list).
            dict_ (dict): The dictionary of named ANSI color codes (foreground or background).
            code (int): Base ANSI code for custom colors (38 for foreground, 48 for background).
            code_end (int): ANSI code to reset color (39 for foreground, 49 for background).

        Returns:
            str: The string with the applied ANSI color.
        """
        if isinstance(color, (tuple, list)) and len(color) == 3:
            ansi_code = f'\x1b[{code};2;{color[0]};{color[1]};{color[2]}m'
            string = f"{ansi_code}{string}\x1b[{code_end}m"
        elif isinstance(color, str):
            ansi_color_code = dict_.get(color, f"\x1b[{code_end}m")
            string = f"{ansi_color_code}{string}\x1b[{code_end}m"
        return string
Color = CILcolor()


class SyntaxError(Exception):
    """
    Custom SyntaxError Exception class that provides enhanced error messages with customizable colors and 
    formatted output for easier debugging. 
    
    Example:
    --------
    >>> try:
    >>>     raise SyntaxError("Unexpected token", ["print", "(", "5", "+"], 3)
    >>> except SyntaxError as e:
    >>>     print(e)
    The error message would display 'Unexpected token' in red and 'print ( 5 +)' with '+' in bright red.

    Notes:
    ------
    - Uses the `Color.color` utility to apply colors to the specified parts of the error message.
    - Assumes `Color.color` is defined to handle colors 'red' for error text, 'b-red' for bright red, and 'cyan' 
      for highlighting the '>>>' pointer.
    
    """
    def __init__(self, text:str = None, data_list:list = None, index:int = 0):
        """
        Initializes the SyntaxError instance, formats the error message with appropriate color highlights, and 
        prepares the message with the '^' marker to point at the error's approximate location.

        Args:
            text (str, optional): The main error message text to display. It will be shown in red color. Defaults to None.
            data_list (list, optional): A list of strings representing parts of the code or tokens. Defaults to None.
            index (int, optional): Specifies the position in `data_list` to highlight, marking the location of the syntax error. Defaults to 0.
        """
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
    """
    Exception raised for errors related to database operations.

    This exception is intended to be used when an error occurs during
    database interactions, allowing for better error handling and
    debugging by providing a formatted error message.

    Attributes:
        message (str): A formatted message describing the error.
        error (str): An optional additional error message that provides more context.

    Parameters:
        text (str): The main error message to be displayed.
        error (str, optional): An additional error message to provide more details.
                               If not provided, defaults to an empty string.

    Example:
        raise Database_error("Failed to connect to the database", "Timeout error")
    """

    def __init__(self, text, error=None):
        message = Color.color(text, color='red')
        error = Color.color(error if error else '', color='b-red')
        super().__init__(message + ':' + error)


class Database:
    """
    Database class for managing a JSON-based database of tasks with unique IDs, descriptions, statuses, 
    and timestamps.
    """
    def __init__(self) -> None:
        """
        Initializes the Database object.
        
        Attributes:
            database_name(str): The name of the database file.
            database_path(str): The full path to the database file.
            data(dict): Loaded data from the database file, structured as a dictionary.
        
        Notes:
            Calls the `_load` method to load existing data or create a new file if none exists.
        """
        self.database_name = 'Database.json'
        self.database_path = os.path.join(location, self.database_name)
        self.data = self._load()
    
    def _create(self) -> dict:
        """
        Creates an empty JSON database file.

        Returns:
            dict:  An empty dictionary representing the initial database state.
        """
        try:
            with open(self.database_path, encoding="Utf-8", mode="w") as fp:
                fp.write("{}")
        except PermissionError as e:
            raise Database_error('Permission denied while creating the database', e)
        return {}
    
    def _load(self):
        """
        Loads data from the JSON database file.

        Returns:
            dict: Data loaded from the JSON file.
        
        Note:
            1. if Catch JSONDecodeError data reset to {}
            2. if Catch FileNotFoundError triger `_create()` method
        """
        try:
            with open(self.database_path, mode="r", encoding='Utf-8') as fp:
                return json.load(fp)
        except (json.JSONDecodeError):
            print(Color.color("Failed to decode JSON data:",'red'), Color.color("Data set rest insialized new empty Database",'b-red'))
            return {}
        
        except (FileNotFoundError):
            return self._create()
        
    def _update(self, data:dict) -> None:
        """
        Updates the JSON database file with new data.

        Args:
            data (dict): The data dictionary to write to the JSON file.

        Raises:
            Database_error:  Raised if there is an error updating the database file due to permission or file issues.
        
        Note:
            1. This Method make sure that no data may lost even catch error while writing json
        """
        try:
            with open(self.database_path, mode="w", encoding="utf-8") as fp:
                fp.write(json.dumps(data, ensure_ascii=False))
                
        except (FileNotFoundError, PermissionError) as e:
            raise Database_error(f"Error updating database", e)
    
    def _unique_id(self) -> int:
        """
        Generates a unique identifier for new entries in the database.
        the mthod its use to genrate unique_id is by accsessing the last key
        of dict and + 1 in it resulting always incrementing of ids so no miss match 
        created on single threads system.

        Returns:
            int: based on the last key in `self.data`, or 0 if no keys exist.
        """
        try:
            # Get the last key and convert it to an integer, then increment by 1
            last_key = int(next(reversed(self.data)))
            unique_id = last_key + 1
        except (StopIteration, ValueError):
            # If dictionary is empty or last key isn't numeric, start from 0
            unique_id = 0
        
        return unique_id
    
    def _format(self, tasks: list[dict]) -> str:
        """
        Formats the list of tasks into a readable table-like string.

        Args:
            tasks (list[dict]): A list of tasks to format.

        Returns:
            str: A formatted string representation of the tasks in a table format.
        """
        # Header for the table with colors
        header = f"{Color.color('Task ID', color='b-blue'):<18} | " \
                f"{Color.color('Description', color='b-green'):<60} | " \
                f"{Color.color('Status', color='b-yellow'):<22} | " \
                f"{Color.color('Created At', color='b-cyan'):<25} | " \
                f"{Color.color('Updated At', color='b-cyan'):<25}"
        formatted_tasks = [header]
        formatted_tasks.append("-" * 112)
        
        def create_new_raw(key, task, status, created_at, updated_at):
            task_color = 'green' if status == 'Completed' else 'red'
            formatted_tasks.append(
                f"{Color.color(key, color='red'):<18} | " 
                f"{Color.color(task, color='cyan'):<60} | " 
                f"{Color.color(status, color=task_color):<22} | " 
                f"{Color.color(created_at, color='cyan'):<25} | " 
                f"{Color.color(updated_at, color='cyan'):<25}"
            )
        
        for key, task in tasks:
            # Convert timestamps to readable date format using time module
            created_at = time.strftime("%d %b %y", time.localtime(task['createdAt']))
            updated_at = time.strftime("%d %b %y", time.localtime(task['updatedAt']))
            length = len(task['description'])
            description = task['description']
            
            create_new_raw(key, description[:50], task['status'], created_at, updated_at)
            
            if length > 50:
                remaining_description = description[50:]
                while remaining_description:
                    create_new_raw('', remaining_description[:50], '', '', '')
                    remaining_description = remaining_description[50:]
        
        return '\n'.join(formatted_tasks)

    def Add(self,description:str) -> bool:
        """
        Adds a new task entry to the database.

        Args:
            description (str): Description of the task to add.

        Returns:
            bool: True if the task was added successfully, False if an error occurred.
        
        Notes:
            1. This method automatically assigns a 'todo' status to new entries.
        """
        data = {
            'description': description,
            'status': 'todo',
            'createdAt': time.time(),
            'updatedAt': time.time()
        }
        id = self._unique_id()
        self.data[id] = data
        
        self._update(self.data)
        return Color.color("Task added successfully, ","yellow")+Color.color(f"Task Id: {id}","cyan")
    
    def Delete(self, id_:int) -> dict|None:
        """
        Deletes a task from the database by ID.

        Args:
            id_ (int): The unique ID of the task to delete.

        Returns:
            dict|None: The deleted task's data if the task was found, or None if the ID did not exist.
        """
        if id_ not in self.data:
            raise Database_error(f"Task with ID {id_} does not exist.")
        
        data = self.data.pop(id_)
        self._update(self.data)
        return Color.color("Task deleted: ","yellow")+Color.color(f"'{data['description']}'","cyan")

    def Update(self, id_: int, description: str | None = None, status: str | None = None) -> str:
        """Updates the details of an existing task in the database."""
        if id_ not in self.data:
            raise Database_error(f"Task with ID {id_} does not exist.")
        
        updates = []
        task = self.data[id_]
        
        if description is not None:
            old_description = task.get('description', 'No description')
            task['description'] = description
            updates.append(Color.color("description changed from","cyan")+ Color.color(f" '{old_description}'","yellow")+Color.color(" to ","cyan")+Color.color(f"'{description}'","yellow"))
        
        if status is not None:
            old_status = task.get('status', 'done')
            task['status'] = status
            updates.append(Color.color("status changed from","cyan")+ Color.color(f" '{old_status}'","yellow")+Color.color(" to ","cyan")+Color.color(f"'{status}'","yellow"))
            
        self._update(self.data)
        
        # Formulate the update message
        updated_fields = ', '.join(updates)
        return Color.color(f"Task with ID {id_} updated:","yellow")+f"{updated_fields}."

    def Mark(self, id_:int, status:str) -> None:
        """
        Marks a task with a new status. 
        This method is a shorthand for calling `Update` with only the status parameter.

        Args:
            id_ (int): Unique ID of the task to mark.
            status (str): New status to apply to the task.
        """
        return self.Update(id_, description=None, status=status)
    
    def List(self, filter = "All") -> list[dict]:
        """
        Retrieves a filtered list of tasks from the database.
        If a specific status filter is applied, only tasks matching that status are included.

        Args:
            filter (str, optional): A filter string to match the task's status field. When set to "All", all tasks are returned.. Defaults to "All".

        Returns:
            list[dict]: List of tasks matching the specified filter criteria.
        """
        # If the filter is "All", return all elements
        if filter.lower() == "all":
            data =  list(self.data.items())
        
        else:
            data = [(key,item) for key, item in self.data.items() if item.get("status") == filter]
        
        return self._format(data)


class token:
    """
    A class to represent a customizable token with arguments, fallback options, and an associated method.
    Designed to generate a key dictionary from provided data based on argument keys.

    Attributes:
        argument (dict): A dictionary representing argument names and values.
        fallback (dict | None): Optional fallback dictionary to handle default or backup values.
        optiones (dict | None): Optional dictionary of additional options.
        method (callable): A function or method to be associated with the token.
        help_text (str): A help text description providing details about the token's purpose.
    """
    def __init__(self, argument:dict, fallback:dict|None, optiones:dict|None, method, help_text) -> None:
        """
        Initializes the token with arguments, fallback, options, a method, and help text.

        Parameters:
            argument (dict): Required arguments for the token.
            fallback (dict | None): Fallback values for optional settings.
            optiones (dict | None): Additional options for customizing token behavior.
            method (callable): A method associated with the token.
            help_text (str): Help text explaining the token's usage.
        """
        self.argument = argument
        self.fallback = fallback
        self.optiones = optiones
        self.method = method
        self.help_text = help_text
    
    def generate_key(self, data_list: list) -> dict:
        """
        Generates a dictionary key by matching `data_list` items to `argument` keys.

        Parameters:
            data_list (list): A list of data values to be paired with argument keys.

        Returns:
            dict: A dictionary where each key is from `argument` and each value is from `data_list`.

        Raises:
            ValueError: If `data_list` length does not match the number of `argument` keys.
        """
        if len(data_list) != len(self.argument):
            raise ValueError("Data list length must match argument keys length.")

        return {name: data for name, data in zip(self.argument.keys(), data_list)}


class Parser:
    """
    A class that parses and validates command-line tokens based on valid keywords.
    It checks for valid syntax, ensures that arguments align with expected types and fallbacks, 
    and provides a help method for displaying command usage information.

    Attributes:
        valid_keywords (dict): A dictionary containing valid keywords and their corresponding token details.
    """
    def __init__(self, valid_keywords: dict):
        """
        Initializes the parser with a dictionary of valid keywords.

        Parameters:
            valid_keywords (dict): Dictionary with keywords as keys and token information as values.
        """
        self.valid_keywords = valid_keywords
        
    def check_syntax(self, token: list | tuple) -> callable:
        """
        Validates the syntax of a command token by verifying the operator, checking argument types, 
        and applying fallback values if needed.
        Desigend spasifically for this verstion of task cli 1.0

        Parameters:
            token (list | tuple): The command token to validate, with the first element as the operator 
                                  and the rest as arguments.

        Returns:
            callable: A lambda function to execute the validated command with arguments.

        Raises:
            SyntaxError: If the command operator is invalid, if there are too many or too few arguments, 
                         or if an argument has the incorrect type or does not match available options.
        """
        
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
    
    def get(self) -> callable:
        """
        Retrieves command-line arguments, processes them, and checks for syntax errors.
        If the 'help' command is provided, it returns the help method instead.

        Returns:
            callable | None: A callable function to execute the command, or None if no command is provided.
        """
        token = sys.argv[1:]
        if token == [] or None:
            raise SyntaxError("There is no command to execute")
        
        if token[0].lower() == 'help':
            return self.help

        return self.check_syntax(token)

    def help(self) -> None:
        """
        Displays help information for each valid command, including argument details,
        types, fallbacks, and options available.

        Returns:
            str: A formatted help text providing information on each valid command's syntax and usage.
        """
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

    # implementation
    try: method_ = parser.get()
    except SyntaxError as e: print(e); return
    
    #running the method
    try: print(method_())
    except (Database_error, ValueError) as e: print(e)


def color_fixer():
    print(Color.color("Loading..", 'red'), flush=True)
    os.system('cls' if os.name == 'nt' else "clear")


if __name__ == "__main__":
    color_fixer()
    main()