class News:
  
  def __init__(self, webSiteName, title, annotation, author):
    # self.url = url
    self.webSiteName = webSiteName
    self.title = title
    self.annotation = annotation
    self.author = author
    
  def __str__(self):
    return Color.BLUE + f"{self.title}\n"+ Color.END + Color.GREEN + f"{self.annotation}\n" + Color.END + Color.PURPLE + f"{self.author}\n" + Color.END

# Класс для определения цветов
# Используется для вывода текста в консоль разными цветами
class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
