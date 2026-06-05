import os
import datetime
import re
import shutil
from html import escape

# assets directory (icons shipped with the script)
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')


def ensure_assets(dest_dir: str):
    """Ensure icon files are copied to dest_dir so HTML can reference them relatively."""
    try:
        os.makedirs(dest_dir, exist_ok=True)
        for name in ('folder.svg', 'fish.svg', 'folder.png', 'fish.png'):
            src = os.path.join(ASSETS_DIR, name)
            dst = os.path.join(dest_dir, name)
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.copy2(src, dst)
    except Exception as e:
        print(f"Uwaga: nie udało się skopiować assetów: {e}")

IMAGE_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}


def is_image(fname):
    return os.path.splitext(fname)[1].lower() in IMAGE_EXT


def build_gallery(root_path: str):
    root_path = os.path.abspath(root_path)
    if not os.path.isdir(root_path):
        print(f"Błąd: nie ma takiego katalogu: {root_path}")
        return

    folders = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
    folders.sort(reverse=True)

    sections = []
    for folder in folders:
        folder_path = os.path.join(root_path, folder)
        files = [f for f in os.listdir(folder_path) if is_image(f)]
        files.sort(reverse=True)
        if not files:
            continue
        imgs_html = []
        for f in files:
            rel = os.path.join(folder, f).replace('\\', '/')
            imgs_html.append(f'<div class="item"><a href="{escape(rel)}" target="_blank">'
                             f'<img src="{escape(rel)}" alt="{escape(f)}"></a>'
                             f'<div>{escape(f)}</div></div>')
        section_html = f"<h2 id=\"{escape(folder)}\">{escape(folder)}</h2>\n<div class=\"grid\">" + '\n'.join(imgs_html) + "</div>"
        sections.append(section_html)

    nav_html = ' '.join([f'<a href="#'+escape(folder)+'">'+escape(folder)+'</a>' for folder in folders])
    sections_html = '\n'.join(sections)

    html = f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Galeria - {escape(os.path.basename(root_path))}</title>
  <style>
    body{{font-family:Arial,Helvetica,sans-serif;margin:18px}}
    .grid{{display:flex;flex-wrap:wrap;gap:10px}}
    .item{{width:200px}}
    .item img{{max-width:100%;height:auto;display:block}}
    nav{{margin-bottom:16px}}
    nav a{{margin-right:8px}}
  </style>
</head>
<body>
  <h1>Galeria: {escape(os.path.basename(root_path))}</h1>
  <nav>
    {nav_html}
  </nav>
  {sections_html}
</body>
</html>
"""

    out_file = os.path.join(root_path, 'gallery_index.html')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Wygenerowano: {out_file}")


def extract_time_from_filename(filename: str) -> str:
    """
    Spróbuj wyciągnąć godzinę z nazwy pliku.
    Szuka wzorca HH_MM_SS lub HH-MM-SS w nazwie.
    Zwraca godzinę w formacie HH:MM:SS lub oryginalną nazwę jeśli nie znaleziono.
    """
    import re
    # Szukaj wzorca HH_MM_SS lub HH-MM-SS
    match = re.search(r'(\d{2})[-_](\d{2})[-_](\d{2})', filename)
    if match:
        # zwracamy tylko godziny i minuty (bez sekund)
        return f"{match.group(1)}:{match.group(2)}"
    return filename


def build_gallery_for_day(root_path: str, day: str = None, output_dir: str = None):

    root_path = os.path.abspath(root_path)
    if not os.path.isdir(root_path):
        print(f"Błąd: nie ma takiego katalogu: {root_path}")
        return None

    if output_dir is None:
        output_dir = root_path
    else:
        output_dir = os.path.abspath(output_dir)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    # Jeśli nie podano dnia, bierz dzisiaj
    if day is None:
        day = datetime.date.today().strftime('%Y_%m_%d')

    # Convert day format to date object for display
    try:
        day_obj = datetime.datetime.strptime(day, '%Y_%m_%d').date()
        day_display = day_obj.strftime('%d.%m.%Y')  # np. "05.06.2026"
    except ValueError:
        day_display = day

    day_folder = os.path.join(root_path, day)
    if not os.path.isdir(day_folder):
        print(f"Błąd: folder dla dnia {day} nie istnieje: {day_folder}")
        return None

    # Zbierz obrazy z folderu dnia
    files = [f for f in os.listdir(day_folder) if is_image(f)]
    files.sort(reverse=True)

    if not files:
        print(f"Uwaga: brak obrazów w folderze {day_folder}")
        return None

    # Generuj HTML
    imgs_html = []
    for f in files:
        rel = os.path.join(day, f).replace('\\', '/')
        time_label = extract_time_from_filename(f)
        imgs_html.append(f'<div class="photo-item"><div class="photo-time">{escape(time_label)}</div><a href="{escape(rel)}" target="_blank">'
                         f'<img src="{escape(rel)}" alt="{escape(f)}"></a></div>')

    grid_html = '\n'.join(imgs_html)

    html = f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Galeria - {escape(day_display)}</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    body {{
      font-family: 'Segoe UI', 'Apple Color Emoji', 'Noto Color Emoji', Tahoma, Geneva, Verdana, sans-serif;
      background: #000000; /* czarne tło */
      color: #fff;
      min-height: 100vh;
      padding: 20px;
    }}
    .container {{
      max-width: 1100px;
      margin: 0 auto;
    }}
    .header {{
      background: rgba(255, 255, 255, 0.02);
      border-radius: 10px;
      padding: 20px;
      margin-bottom: 24px;
      color: white;
    }}
    h1 {{
      font-size: 2rem;
      margin-bottom: 6px;
    }}
    .info {{
      font-size: 0.95rem;
      opacity: 0.9;
    }}
    /* jedna kolumna - zdjęcia jedno pod drugim */
    .gallery-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 18px;
    }}
    .photo-item {{
      background: #0b0b0b;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 6px 30px rgba(0, 0, 0, 0.6);
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }}
     .photo-item:hover {{
       transform: translateY(-6px);
       box-shadow: 0 12px 40px rgba(0, 0, 0, 0.8);
     }}
     .photo-item a {{
       display: block;
     }}
     .photo-item img {{
       width: 100%;
       height: auto; /* zachowaj proporcje, większe zdjęcia */
       display: block;
       background: #000;
     }}
     .photo-time {{
       padding: 10px 14px;
       text-align: center;
       font-weight: 700;
       color: #ffffff;
       font-size: 1.05rem;
       background: rgba(0, 0, 0, 0.5);
       border-bottom: 1px solid rgba(255, 255, 255, 0.1);
     }}
    .back-link {{
      display: inline-block;
      margin-bottom: 18px;
      color: white;
      text-decoration: none;
      background: rgba(255, 255, 255, 0.03);
      padding: 8px 14px;
      border-radius: 6px;
      transition: transform 0.2s ease;
    }}
    .back-link:hover {{
      transform: translateX(-6px);
    }}
    @media (min-width: 1400px) {{
      .container {{ max-width: 1300px; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <a href="index.html" class="back-link">← Powrót do listy galerii</a>
    <div class="header">
      <h1><img src="fish.png" alt="fish" style="height:28px;vertical-align:middle;margin-right:8px"> Galeria: {escape(day_display)}</h1>
      <div class="info">{len(files)} zdjęć</div>
    </div>
    <div class="gallery-grid">
      {grid_html}
    </div>
  </div>
</body>
</html>
"""

    out_file = os.path.join(output_dir, f'gallery_{day}.html')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Wygenerowano: {out_file}")
    # Automatycznie wygeneruj index.html
    # ensure icon assets are present in output_dir
    build_index(output_dir)
    return out_file


def build_index(gallery_dir: str):
    """
    Generuje plik index.html zawierający linki do wszystkich dostępnych galerii.

    Szuka wszystkich plików gallery_YYYY-MM-DD.html w podanym katalogu,
    sortuje je malejąco po dacie i generuje ładnie sformatowany index.

    Args:
        gallery_dir (str): Katalog zawierający pliki gallery_*.html

    Returns:
        str: Ścieżka do wygenerowanego index.html lub None jeśli błąd.

    Example:
        build_index('/path/to/gallery_files')
    """
    gallery_dir = os.path.abspath(gallery_dir)
    if not os.path.isdir(gallery_dir):
        print(f"Błąd: nie ma takiego katalogu: {gallery_dir}")
        return None

    # ensure assets copied so icons are available next to index.html
    ensure_assets(gallery_dir)

    # Szukanie wszystkich plików gallery_*.html
    gallery_files = []
    pattern = re.compile(r'^gallery_(\d{4}[-_]\d{2}[-_]\d{2})\.html$')

    for fname in os.listdir(gallery_dir):
        match = pattern.match(fname)
        if match:
            date_str = match.group(1).replace('_', '-')
            full_path = os.path.join(gallery_dir, fname)
            gallery_files.append((date_str, fname, full_path))

    # Sortuj malejąco po dacie (najnowsze najpierw)
    gallery_files.sort(key=lambda x: x[0], reverse=True)

    if not gallery_files:
        print(f"Uwaga: brak plików gallery_*.html w katalogu: {gallery_dir}")
        return None

    # wybierz ikonę folderu (jpg jeśli dostępny, inaczej svg)
    folder_icon = 'folder.png'

    # Generuj HTML z linkami do galerii
    items_html = []
    for date_str, fname, full_path in gallery_files:
        # Parsuj datę aby wyświetlić ją ładnie
        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            date_display = date_obj.strftime('%d.%m.%Y')  # np. "05.06.2026"
            day_name = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela'][date_obj.weekday()]
        except ValueError:
            date_display = date_str
            day_name = 'dzień'

        # Spróbuj wczytać liczbę zdjęć z pliku galerii
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                img_count = content.count('<img src=') - 1
        except:
            img_count = 0

        photo_text = f"{img_count} zdjęć" if img_count > 0 else "brak zdjęć"

        item_html = f'''<div class="gallery-item">
    <a href="{escape(fname)}">
      <img src="{folder_icon}" class="folder-icon" alt="folder icon">
      <div class="folder-label">Folder</div>
      <div class="date">{escape(date_display)}</div>
      <div class="day">{escape(day_name)}</div>
      <div class="photos">{escape(photo_text)}</div>
    </a>
  </div>'''
        items_html.append(item_html)

    items_section = '\n'.join(items_html)

    html = f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Galerie - Akwarium</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    body {{
      font-family: 'Segoe UI', 'Apple Color Emoji', 'Noto Color Emoji', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 20px;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    h1 {{
      color: white;
      text-align: center;
      margin-bottom: 30px;
      font-size: 2.5rem;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }}
    .gallery-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }}
    .gallery-item {{
      background: white;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      transition: all 0.3s ease;
      cursor: pointer;
    }}
    .gallery-item:hover {{
      transform: translateY(-8px);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }}
    .gallery-item a {{
      text-decoration: none;
      color: inherit;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 25px 15px;
      min-height: 220px;
    }}
    .folder-icon {{      
      width: 48px;
      height: 48px;
      object-fit: contain;
      margin-bottom: 8px;
      display: block;
      line-height: 1;      
    }}
    .folder-label {{
      font-size: 0.7rem;
      color: #999;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .date {{
      font-size: 1.3rem;
      font-weight: bold;
      color: #333;
      margin-bottom: 5px;
      margin-top: 3px;
    }}
    .day {{
      font-size: 0.9rem;
      color: #999;
      text-transform: capitalize;
      margin-bottom: 8px;
    }}
    .photos {{
      font-size: 0.85rem;
      color: #666;
      background: #f0f0f0;
      padding: 6px 12px;
      border-radius: 20px;
      margin-top: 8px;
    }}
    footer {{
      text-align: center;
      color: white;
      font-size: 0.9rem;
      margin-top: 40px;
      opacity: 0.8;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Galerie Akwarium</h1>
    <div class="gallery-grid">
      {items_section}
    </div>
    <footer>
      <p>Łącznie {len(gallery_files)} galerii | Ostatnia aktualizacja: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
    </footer>
  </div>
</body>
</html>
"""

    out_file = os.path.join(gallery_dir, 'index.html')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)

    # ensure icon assets are present next to index.html
    print(f"Wygenerowano: {out_file}")
    return out_file


if __name__ == '__main__':
    build_gallery_for_day("/home/pi/Pictures")
