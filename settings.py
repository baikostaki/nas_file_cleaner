from typing import List, Dict

#FIXME - maybe create it as a module somehow?
class Settings:
    suffixes: Dict[str, List[str]] = {}
       
    def __init__(self) -> None:
        current_category = str()
        with open('extensions.txt', 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                if line.startswith("#"):
                    current_category: str = line[1:]
                    self.suffixes[current_category] = []
                elif line:
                    self.suffixes[current_category].append(line)
    
    def get_suffixes(self) -> Dict[str, List[str]]:
        return self.suffixes    
            
       
    
