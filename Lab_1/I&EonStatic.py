import math
from collections import Counter

texts = {
    "1": {
        "ua": "Недалеко от Богуслава, в довгому покрученому яру розкинулось село Семигори. "
                  "Яр в'ється гадюкою між крутими горами, між зеленими терасами; од яру на всі боки розбіглись, "
                  "неначе гілки дерева, глибокі рукави й поховались десь далеко в густих лісах. На дні довгого яру блищать "
                  "рядками ставочки в очеретах, в осоці, зеленіють левади. Греблі обсаджені столітніми вербами. "
                  "В глибокому яру ніби в'ється оксамитовий зелений пояс, на котрому блищать ніби вправлені в зелену оправу прикраси з срібла. "
                  "Два рядки білих хат попід горами біліють, неначе два рядки перлів на зеленому поясі. Коло хат зеленіють густі старі садки. "
                  "На високих гривах гір кругом яру зеленіє старий ліс, як зелене море, вкрите хвилями. Глянеш з високої гори на той ліс, і здається, "
                  "ніби на гори впала оксамитова зелена тканка, гарно побгалась складками, позападала в вузькі долини тисячами оборок та жмутів. "
                  "В гарячий ясний літній день ліс на горах сяє, а в долинах чорніє. Ті долини здалека дишуть тобі в лице холодком, лісовою вогкістю.",
        "en": "Not far from Boguslav, in a long twisted ravine, lies the village of Semigory. The ravine winds like a viper between steep mountains, "
                  "between green terraces; deep branches have scattered from the ravine in all directions, like tree branches, and are hidden somewhere "
                  "far away in dense forests. At the bottom of a long ravine, ponds in reeds and sedge glisten in rows, and levades turn green. "
                  "The dams are lined with century-old Willows. In a deep ravine, a velvet green belt seems to curl, on which silver jewelry set in a green frame glitters. "
                  "Two rows of white huts under the mountains turn white, like two rows of pearls on a green belt. Dense old gardens turn green around the houses. "
                  "On the high manes of the mountains around the ravine, the old forest turns green, like a green sea covered with waves. "
                  "You look down from a high mountain at that forest, and it seems as if a velvety green cloth has fallen on the mountains, beautifully arranged in folds, "
                  "and fallen into narrow valleys with thousands of frills and Tufts. On a hot, clear summer day, the forest on the mountains shines, "
                  "and in the valleys it turns black. Those valleys from afar breathe cold, forest dampness into your face.",
        "de": "In der Nähe von Bohuslav hat sich das Dorf Semigory in einer langen, verdrehten Schlucht ausgebreitet. "
                  "Die Schlucht windet sich mit einer Viper zwischen steilen Bergen, zwischen grünen Terrassen, von der Schlucht sind sie wie Äste, "
                  "tiefe Ärmel in alle Richtungen gelaufen und haben sich irgendwo weit in dichten Wäldern versteckt. Am Boden einer langen Schlucht glänzen die Teiche im Schilf, "
                  "in der Segge, die Levaden werden grün. Die Dämme sind mit hundertjährigen Weiden bepflanzt. In einer tiefen Schlucht, als würde sich ein grüner Samtgürtel winden, "
                  "auf dem Silberschmuck glänzt, der in einen grünen Rahmen gerichtet ist. Zwei Zeilen weißer Häuser unter den Bergen sind weiß, "
                  "als wären zwei Perlenstiche am grünen Gürtel. An den Häusern sind dicke alte Gärten grün. Auf den hohen Mähnen der Berge "
                  "um die Schlucht grünt der alte Wald wie ein grünes Meer, das von Wellen bedeckt ist. Schaust du von einem hohen Berg in den Wald, und es scheint, "
                  "als wäre ein samtiggrüner Stoff auf die Berge gefallen, hat sich schön in Falten geschoren und Tausende von Rüschen und Fetzen in die engen Täler geworfen. "
                  "An einem heißen, klaren Sommertag scheint der Wald auf den Bergen und in den Tälern wird es schwarz. Diese Täler atmen dir von weitem Kälte, Waldfeuchte ins Gesicht."
    },
    "2": {
        "ua": "Під однією горою, коло зеленої левади, в глибокій западині стояла чимала хата Омелька Кайдаша. Хата потонула в старому садку. "
                    "Старі черешні росли скрізь по дворі й кидали од себе густу тінь. Вся Кайдашева садиба ніби дихала холодком. "
                    "Одного літнього дня перед паликопою Омелько Кайдаш сидів в повітці на ослоні й майстрував. Широкі ворота були одчинені навстіж. "
                    "Густа тінь у воротах повітки, при ясному сонці, здавалась чорною. Ніби намальований на чорному полі картини, сидів Кайдаш в білій сорочці "
                    "з широкими рукавами. Кайдаш стругав вісь. Широкі рукава закачались до ліктів; з-під рукавів було видно здорові загорілі жилаві руки. "
                    "Широке лице було сухорляве й бліде, наче лице в ченця. На сухому високому лобі набігали густі дрібні зморшки. "
                    "Кучеряве посічене волосся стирчало на голові, як пух, і блищало сивиною. Коло повітки на току два Кайдашеві сини, молоді парубки, "
                    "поправляли поди під стіжки: жнива кінчались, і начиналась возовиця. Старшого Кайдашевого сина звали Карпом, меншого — Лавріном.",
        "en": "English text 2",
        "de": "German Text 2"
    }
}

alphabets  = {
    "ua" : "",
    "en" : "",
    "de" : ""
}

print("Оберіть варіант: ")
print("1. Той самий текст (за замовчуванням)")
print("2. Дорівнює по символам")
v_choice = input("Ваш вибір (1/2): ")
if v_choice not in ["1", "2"]:
    v_choice = "1"

print("Оберіть мову: ")
print("ua. Українська (за замовчуванням)")
print("en. Англійська")
print("de. Німецька")
l_choice = input("Ваш вибір (ua/en/de): ").lower().strip()
if l_choice not in ["ua", "en", "de"]:
    l_choice = "ua"

text = texts[v_choice][l_choice]
alphabet = alphabets[l_choice]

print(f"Обраний текст: {text}")

n = len(text)
counts = Counter(text)

print("Оберіть тип даних (одиниць виміру):")
print("1. Біти (основа 2)")
print("2. Ніти (основа e)")
print("3. Діти (основа 10)")
choice = input("Ваш вибір (1/2/3): ")

if choice == '2':
    base = math.e
    unit = "нит"
elif choice == '3':
    base = 10
    unit = "дит"
else:
    base = 2
    unit = "бит"

entropy = 0
print("\n--- Аналіз символів ---")
print(f"{'Символ':<10} | {'Кількість':<10} | {'Верогідність':<12}")
print("-" * 40)

for char, count in sorted(counts.items(), key=lambda item: item[1]):
    p = count / n
    entropy -= p * math.log(p, base)
    display_char = repr(char)
    print(f"{display_char:<10} | {count:<10} | {p:<12.4f}")

info_amount = n * entropy

print(f"Символів тексту: {n}")
print(f"Кількість унікальних символів в тексті: {len(counts)}")
print("Об'єм алфавіту мови: ")
print(f"Энтропія: {entropy:.4f} {unit}/символ")
print(f"Кількість інформації: {info_amount:.4f} {unit}")
