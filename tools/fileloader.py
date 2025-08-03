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


            # 正則表達式 @(\S+) 會捕獲 @ 後面所有非空格的字符作為 keyword (group 1)
            matches = list(re.finditer(r'@(\S+)', content))
            for match in reversed(matches):
                file_path_str = match.group(1)
                cleaned_file_path_str = file_path_str.rstrip('.,;!?')
                file_path = Path(cleaned_file_path_str)

                try:

                    file_content = file_path.read_text(encoding='utf-8')
                    

                    content = content[:match.start()] + file_content + content[match.end():]
                    
                    print(f"[{self.__class__.__name__}] Success: Loaded and replaced '{cleaned_file_path_str}'")

                except FileNotFoundError:
                    print(f"[{self.__class__.__name__}] Skipped: File not found for '{cleaned_file_path_str}'")
                    pass
                except Exception as e:
                    print(f"[{self.__class__.__name__}] Skipped: Error reading '{cleaned_file_path_str}': {e}")
                    pass
            context.messages[-1]['content'] = content
                        
        return context