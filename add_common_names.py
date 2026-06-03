"""
Script para adicionar nomes comuns aos dados de primatas
Usa a API da Wikipedia para buscar nomes comuns
"""

import pandas as pd
import requests
import time
from pathlib import Path
from urllib.parse import quote


def format_scientific_name(name):
    """
    Formata nome científico para o padrão Wikipedia
    Ex: TRACHYPITHECUS CRISTATUS -> Trachypithecus cristatus
    """
    parts = name.strip().split()
    if len(parts) >= 2:
        return f"{parts[0].capitalize()} {parts[1].lower()}"
    return name.capitalize()


def get_common_name_from_wikipedia(scientific_name, lang='en'):
    """
    Busca nome comum usando a API da Wikipedia
    
    Args:
        scientific_name: Nome científico da espécie
        lang: Idioma da Wikipedia ('pt' para português, 'en' para inglês)
    
    Returns:
        Nome comum ou None se não encontrado
    """
    formatted_name = format_scientific_name(scientific_name)
    
    try:
        # Headers para simular navegador
        headers = {
            'User-Agent': 'GlobalPrimatesWatch/1.0 (https://github.com/ferropng/Global-Primates-Watch)'
        }
        
        # API da Wikipedia
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            'action': 'query',
            'titles': formatted_name,
            'prop': 'extracts|info',
            'exintro': True,
            'explaintext': True,
            'inprop': 'url',
            'format': 'json',
            'redirects': 1
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        # Verificar se a resposta é válida
        if response.status_code != 200:
            print(f"    ⚠️  HTTP {response.status_code} para {formatted_name}")
            return None
        
        # Verificar se o conteúdo é JSON
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"    ⚠️  Resposta não-JSON para {formatted_name}")
            return None
        
        pages = data.get('query', {}).get('pages', {})
        
        for page_id, page_data in pages.items():
            if page_id == '-1':  # Página não existe
                # Tentar em outro idioma se falhou
                if lang == 'pt':
                    return get_common_name_from_wikipedia(scientific_name, lang='en')
                return None
            
            # Página existe
            extract = page_data.get('extract', '')
            
            if not extract:
                return None
            
            # Extrair primeira linha
            first_line = extract.split('\n')[0].strip()
            
            # Tentar extrair nome comum de padrões comuns
            # Padrões em inglês: "The X is...", "X is a..."
            # Padrões em português: "O/A X é...", "X é um/uma..."
            
            common_name = None
            
            # Tentar padrões em português
            if lang == 'pt':
                if 'é um' in first_line or 'é uma' in first_line:
                    # "O chimpanzé é um..." -> "chimpanzé"
                    words = first_line.split()
                    if len(words) >= 3:
                        # Remover artigos iniciais
                        start_idx = 0
                        if words[0].lower() in ['o', 'a', 'os', 'as', 'um', 'uma']:
                            start_idx = 1
                        # Pegar até o verbo "é"
                        for i in range(start_idx, len(words)):
                            if words[i] == 'é' or words[i] == 'são':
                                common_name = ' '.join(words[start_idx:i])
                                break
            
            # Tentar padrões em inglês
            elif lang == 'en':
                if ' is ' in first_line or ' are ' in first_line:
                    words = first_line.split()
                    if len(words) >= 3:
                        start_idx = 0
                        if words[0].lower() in ['the', 'a', 'an']:
                            start_idx = 1
                        for i in range(start_idx, len(words)):
                            if words[i] in ['is', 'are', 'was', 'were']:
                                common_name = ' '.join(words[start_idx:i])
                                break
            
            # Limpar o nome comum
            if common_name:
                common_name = common_name.strip(' ,;:')
                # Remover parênteses e conteúdo
                if '(' in common_name:
                    common_name = common_name.split('(')[0].strip()
                return common_name if common_name else None
        
        return None
    
    except requests.exceptions.Timeout:
        print(f"    ⚠️  Timeout para {formatted_name}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"    ⚠️  Erro de requisição para {formatted_name}: {e}")
        return None
    except Exception as e:
        print(f"    ⚠️  Erro inesperado para {formatted_name}: {e}")
        return None


def add_common_names_to_csv():
    """Adiciona nomes comuns ao CSV de primatas"""
    project_root = Path(__file__).parent
    csv_path = project_root / 'data' / 'processed' / 'primates_species_clean.csv'
    
    print(f"Procurando arquivo em: {csv_path}")
    
    if not csv_path.exists():
        print(f"❌ Arquivo não encontrado: {csv_path}")
        print("\nVerifique se:")
        print("1. O arquivo 'primates_species_clean.csv' existe em data/processed/")
        print("2. Você executou o notebook 01_data_cleaning.ipynb primeiro")
        return
    
    print("Carregando dados...")
    df = pd.read_csv(csv_path)
    
    # Verificar se já tem common_name
    if 'common_name' in df.columns:
        print("\n⚠️  Coluna 'common_name' já existe!")
        response = input("Deseja sobrescrever? (s/n): ")
        if response.lower() != 's':
            print("Operação cancelada.")
            return
    
    print(f"\nProcessando {len(df)} espécies...")
    print("Isso pode levar alguns minutos...\n")
    
    common_names = []
    found_count = 0
    
    for idx, row in df.iterrows():
        sci_name = row['sci_name']
        formatted = format_scientific_name(sci_name)
        print(f"  [{idx+1}/{len(df)}] Buscando: {formatted}")
        
        # Tentar primeiro em português, depois em inglês
        common_name = get_common_name_from_wikipedia(sci_name, lang='pt')
        
        if not common_name:
            # Tentar em inglês
            common_name = get_common_name_from_wikipedia(sci_name, lang='en')
        
        if common_name:
            found_count += 1
            print(f"    ✓ Encontrado: {common_name}")
        else:
            common_name = 'Não disponível'
            print(f"    ✗ Não encontrado")
        
        common_names.append(common_name)
        
        # Pausa para não sobrecarregar a API
        time.sleep(0.3)
    
    df['common_name'] = common_names
    
    # Salvar
    df.to_csv(csv_path, index=False)
    print(f"\n{'='*60}")
    print(f"✓ Arquivo atualizado: {csv_path}")
    print(f"  - Total de espécies: {len(df)}")
    print(f"  - Com nome comum: {found_count} ({found_count/len(df)*100:.1f}%)")
    print(f"  - Sem nome comum: {len(df) - found_count}")
    print(f"{'='*60}")


if __name__ == "__main__":
    add_common_names_to_csv()