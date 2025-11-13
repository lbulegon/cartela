"""
Script para gerar ícones do PWA a partir de um ícone base.
Execute: python static/generate_icons.py

Requer: pip install Pillow
"""
from PIL import Image, ImageDraw
import os

def create_icon(size, output_path):
    """Cria um ícone com o logo da Cartela"""
    # Cria uma imagem com fundo amarelo dourado
    img = Image.new('RGB', (size, size), color='#FFD700')
    draw = ImageDraw.Draw(img)
    
    # Desenha o grid 3x3
    cell_size = size // 3
    margin = size // 10
    
    # Linhas horizontais
    for i in range(1, 3):
        y = margin + i * cell_size
        draw.line([(margin, y), (size - margin, y)], fill='#1a1a1a', width=max(2, size//20))
    
    # Linhas verticais
    for i in range(1, 3):
        x = margin + i * cell_size
        draw.line([(x, margin), (x, size - margin)], fill='#1a1a1a', width=max(2, size//20))
    
    # Desenha checkmarks (simplificado)
    check_size = cell_size // 3
    # Top-right
    x1, y1 = margin + 2 * cell_size + cell_size//2 - check_size//2, margin + cell_size//2 - check_size//2
    draw.line([(x1, y1), (x1 + check_size//2, y1 + check_size//2)], fill='#1a1a1a', width=max(3, size//15))
    draw.line([(x1 + check_size//2, y1 + check_size//2), (x1 + check_size, y1 - check_size//2)], fill='#1a1a1a', width=max(3, size//15))
    
    # Middle-center
    x2, y2 = margin + cell_size + cell_size//2 - check_size//2, margin + cell_size + cell_size//2 - check_size//2
    draw.line([(x2, y2), (x2 + check_size//2, y2 + check_size//2)], fill='#1a1a1a', width=max(3, size//15))
    draw.line([(x2 + check_size//2, y2 + check_size//2), (x2 + check_size, y2 - check_size//2)], fill='#1a1a1a', width=max(3, size//15))
    
    # Bottom-left
    x3, y3 = margin + cell_size//2 - check_size//2, margin + 2 * cell_size + cell_size//2 - check_size//2
    draw.line([(x3, y3), (x3 + check_size//2, y3 + check_size//2)], fill='#1a1a1a', width=max(3, size//15))
    draw.line([(x3 + check_size//2, y3 + check_size//2), (x3 + check_size, y3 - check_size//2)], fill='#1a1a1a', width=max(3, size//15))
    
    img.save(output_path, 'PNG')
    print(f'Ícone criado: {output_path} ({size}x{size})')

def main():
    """Gera todos os ícones necessários"""
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    icons_dir = 'static/icons'
    
    # Cria o diretório se não existir
    os.makedirs(icons_dir, exist_ok=True)
    
    for size in sizes:
        output_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
        create_icon(size, output_path)
    
    print('\n✅ Todos os ícones foram gerados!')

if __name__ == '__main__':
    main()

