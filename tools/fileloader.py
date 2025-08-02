from tools.base import Base
from tools.context import LLMContext
from pathlib import Path
import re

class FileLoader(Base):
    def handle(self, config: dict, context: LLMContext):
        
        if not context.messages:
            return context

        last_message = context.messages[-1]

        if last_message.get('role') == 'user':
            content = last_message.get('content', '')

            match = re.search(r'\[@([^\]]+)\]', content)
            
            if match:
                file_path_str = match.group(1)
                file_path_str = file_path_str.strip('"')
                file_path = Path(file_path_str)

                print(f"[{self.__class__.__name__}] File path found: {file_path}")

                try:

                    file_content = file_path.read_text(encoding='utf-8')
  
                    new_content = re.sub(r'\[@([^\]]+)\]', file_content, content, count=1)

                    context.messages[-1]['content'] = new_content
                    
                    print(f"[{self.__class__.__name__}] File content loaded and replaced successfully.")
                    
                except FileNotFoundError:
                    context.messages[-1]['content'] = "FileNotFoundError"
                    print(f"[{self.__class__.__name__}] Error: File not found: {file_path_str}")
                except Exception as e:
                    context.messages[-1]['content'] = "Failed to read file"
                    print(f"[{self.__class__.__name__}] Error: Failed to read file: {e}")

        return context