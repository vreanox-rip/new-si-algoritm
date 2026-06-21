from pathlib import Path
from datetime import datetime

class SimpleAI:
    #sodda boshlang'ich ong tizimli algoritm
    
    def __init__(self):
        # Katalog yaratish
        self.data_dir = Path("ai_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Fayllar
        self.laws_file = self.data_dir / "laws.txt"
        self.knowledge_file = self.data_dir / "knowledge.txt"
        self.user_data_file = self.data_dir / "file.txt"
        self.history_file = self.data_dir / "history.txt"
        
        # Hamma fayl mavjud ekanligini tekshirish
        self._create_files()
    
    def _create_files(self):
    #agar fayl yo'q bo'lsa yaratadi
        if not self.laws_file.exists():
            self.laws_file.write_text("# QONUNLAR\n")
        if not self.knowledge_file.exists():
            self.knowledge_file.write_text("# BILIM BAZASI\n")
        if not self.user_data_file.exists():
            self.user_data_file.write_text("")
        if not self.history_file.exists():
            self.history_file.write_text("")
    
    def read_laws(self):
    #qonunlarni o'qish
        return self.laws_file.read_text(encoding='utf-8')
    
    def read_knowledge(self):
    #bilim bazasini o'qiydi
        return self.knowledge_file.read_text(encoding='utf-8')
    
    def read_user_data(self):
    #file.txt o'qish
        return self.user_data_file.read_text(encoding='utf-8')
    
    def save_knowledge(self, text):
        #bilim bazasini kengaytirish
        current = self.read_knowledge()
        new_text = current + f"\n\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n{text}"
        self.knowledge_file.write_text(new_text, encoding='utf-8')
    
    def save_history(self, user_input, response):
        #suxbat tarixiga yozish
        entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n"
        entry += f"Siz: {user_input}\nAI: {response}\n" + "="*50 + "\n"
        with open(self.history_file, 'a', encoding='utf-8') as f:
            f.write(entry)
    
    def simple_response(self, user_input):
        #sodda javob text fayllardan qidirish
        user_lower = user_input.lower()
        knowledge = self.read_knowledge().lower()
        user_data = self.read_user_data().lower()
        
        #agar sorov knowledge'da bo'lsa, uniandiflarni qaytarish
        if any(word in knowledge for word in user_lower.split()):
            return "📚 Bilim bazasida topildi:\n" + self.read_knowledge()
        
        #agar shaxsiy ma'lumot so'ralsa
        if "kim" in user_lower or "siz" in user_lower or "men" in user_lower:
            if self.read_user_data().strip():
                return "👤 Sizning ma'lumotlar:\n" + self.read_user_data()
            else:
                return "❌ file.txt bo'sh. Iltimos, o'z ma'lumotlaringizni qo'shing."
        
        # Default javob
        return "Sizning savolingizni qabul qildim: " + user_input
    
    def process_command(self, user_input):
        #buyruq ustida qayta ishlash
        
        # LEARN komandasi
        if user_input.lower().startswith("learn:"):
            info = user_input[6:].strip()
            self.save_knowledge(info)
            return f"Saqlandı: {info}"
        
        # READ LAWS
        elif user_input.lower() == "read_laws":
            return " QONUNLAR:\n" + self.read_laws()
        
        # READ KNOWLEDGE
        elif user_input.lower() == "read_knowledge":
            return " BILIM BAZASI:\n" + self.read_knowledge()
        
        # READ DATA
        elif user_input.lower() == "read_data":
            return " FOYDALANUVCHI MA'LUMOTLARI:\n" + self.read_user_data()
        
        # READ HISTORY
        elif user_input.lower() == "history":
            return " SUHBAT TARIXI:\n" + self.history_file.read_text(encoding='utf-8')
        
        # EXIT
        elif user_input.lower() in ["exit", "quit", "chiqish"]:
            return None  # Dastur to'xtaydi
        
        # Boshqa - sodda javob
        else:
            response = self.simple_response(user_input)
            return response
    
    def run(self):
    #terminalda ishga tushirish
        print("=" * 60)
        print(" OFFLINE AI ASSISTANT")
        print("=" * 60)
        print("\nKomandalar:")
        print("  learn: <ma'lumot>  - Bilim bazasiga qo'shadi")
        print("  read_laws          - Qonunlarni ko'rsatadi")
        print("  read_knowledge     - Bilim bazasini ko'rsatadi")
        print("  read_data          - file.txt ni ko'rsatadi")
        print("  history            - Tarixni ko'rsatadi")
        print("  exit/quit          - Chiqadi")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n Siz: ").strip()
                
                if not user_input:
                    continue
                
                response = self.process_command(user_input)
                
                if response is None:
                    print("Xayr!")
                    break
                
                print(f"\n AI: {response}")
                
                # Tarixga yozish
                if user_input.lower() not in ["read_laws", "read_knowledge", "read_data", "history"]:
                    self.save_history(user_input, response)
            
            except KeyboardInterrupt:
                print("\n\n Dastur to'xtatildi")
                break
            except Exception as e:
                print(f" Xato: {str(e)}")


if __name__ == "__main__":
    ai = SimpleAI()
    ai.run()