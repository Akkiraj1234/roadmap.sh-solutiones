import sys, os, json, time
location = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


class syntax_error(Exception):
    def __init__(self, *args):
        super().__init__(*args)

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
        if filter == "All":
            return list(self.data.values())

        # Otherwise, filter items based on the `mark` field
        filtered_items = [item for item in self.data.values() if item.get("status") == filter]
        return filtered_items

class parser:
    
    def __init__(self):
        pass
    

class Decorater:
    
    def __init__(self):
        pass
    
    
def main():
    database = Database()
    # database.Add("my first task ")
    # print(database.Delete('1'))
    # database.Update("5", "I am edited task 2")
    # database.Mark("0", "done")
    # database.Mark("4", "in-progress")
    # print(database.List('todo'))
    
    


if __name__ == "__main__":
    main()

    

