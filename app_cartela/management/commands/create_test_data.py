from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from betting.models import (
    Event, MarketSelection, CartelaTemplate, CartelaTemplateItem
)


class Command(BaseCommand):
    help = 'Cria dados de teste: eventos, seleções e template de cartela'

    def criar_selecoes_para_evento(self, evento):
        """Cria seleções de mercado para um evento"""
        selecoes_data = [
            {
                'selection_type': 'TOTAL_GOALS_OVER',
                'params': {'line': 2.5},
                'prob_base': 0.65,
                'odd_justa': 1.54,
                'odd_publicada': 1.45,
                'is_live': False,
            },
            {
                'selection_type': 'NEXT_CORNER',
                'params': {'team': 'home'},
                'prob_base': 0.50,
                'odd_justa': 2.00,
                'odd_publicada': 1.90,
                'is_live': False,
            },
            {
                'selection_type': 'TEAM_TO_SCORE',
                'params': {'team': 'home', 'time': 'first_half'},
                'prob_base': 0.55,
                'odd_justa': 1.82,
                'odd_publicada': 1.75,
                'is_live': False,
            },
            {
                'selection_type': 'TOTAL_GOALS_OVER',
                'params': {'line': 1.5},
                'prob_base': 0.75,
                'odd_justa': 1.33,
                'odd_publicada': 1.30,
                'is_live': False,
            },
            {
                'selection_type': 'NEXT_CORNER',
                'params': {'team': 'away'},
                'prob_base': 0.45,
                'odd_justa': 2.22,
                'odd_publicada': 2.10,
                'is_live': False,
            },
        ]
        
        selecoes_criadas = 0
        for sel_data in selecoes_data:
            sel, created = MarketSelection.objects.get_or_create(
                event=evento,
                selection_type=sel_data['selection_type'],
                params=sel_data['params'],
                defaults={
                    'prob_base': sel_data['prob_base'],
                    'odd_justa': sel_data['odd_justa'],
                    'odd_publicada': sel_data['odd_publicada'],
                    'is_live': sel_data['is_live'],
                }
            )
            if created:
                selecoes_criadas += 1
        
        return selecoes_criadas

    def handle(self, *args, **options):
        # Lista de eventos para criar
        eventos_data = [
            {
                'team_home': 'Flamengo',
                'team_away': 'Palmeiras',
                'sport': 'SOCCER',
                'hours_offset': 2,
            },
            {
                'team_home': 'Corinthians',
                'team_away': 'São Paulo',
                'sport': 'SOCCER',
                'hours_offset': 4,
            },
            {
                'team_home': 'Lakers',
                'team_away': 'Warriors',
                'sport': 'BASKETBALL',
                'hours_offset': 6,
            },
            {
                'team_home': 'Nadal',
                'team_away': 'Djokovic',
                'sport': 'TENNIS',
                'hours_offset': 8,
            },
            {
                'team_home': 'Brasil',
                'team_away': 'Argentina',
                'sport': 'SOCCER',
                'hours_offset': 10,
            },
            {
                'team_home': 'Flamengo',
                'team_away': 'Vasco',
                'sport': 'SOCCER',
                'hours_offset': 12,
            },
        ]
        
        eventos_criados = []
        total_selecoes = 0
        
        for evt_data in eventos_data:
            evento, created = Event.objects.get_or_create(
                team_home=evt_data['team_home'],
                team_away=evt_data['team_away'],
                defaults={
                    'sport': evt_data['sport'],
                    'start_time': timezone.now() + timedelta(hours=evt_data['hours_offset']),
                    'status': 'SCHEDULED',
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Evento criado: {evento}'))
                selecoes_criadas = self.criar_selecoes_para_evento(evento)
                total_selecoes += selecoes_criadas
                self.stdout.write(self.style.SUCCESS(f'   └─ {selecoes_criadas} seleções criadas'))
                eventos_criados.append(evento)
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Evento já existe: {evento}'))
        
        # Cria template de cartela (se não existir)
        template, created = CartelaTemplate.objects.get_or_create(
            nome='Cartela do Jogo',
            defaults={
                'descricao': 'Cartela padrão para apostas em jogos',
                'tipo': 'PRE_MATCH',
                'config': {
                    'min_items': 3,
                    'max_items': 5,
                },
                'ativo': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Template criado: {template.nome}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Template já existe: {template.nome}'))
        
        # Cria itens do template (permite todos os tipos)
        tipos_permitidos = ['TOTAL_GOALS_OVER', 'NEXT_CORNER', 'TEAM_TO_SCORE']
        for tipo in tipos_permitidos:
            item, created = CartelaTemplateItem.objects.get_or_create(
                cartela_template=template,
                allowed_selection_type=tipo,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'   └─ Item de template criado: {tipo}'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('✅ Dados de teste criados com sucesso!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'\n📊 Total de eventos criados: {len(eventos_criados)}')
        self.stdout.write(f'🎯 Total de seleções criadas: {total_selecoes}')
        self.stdout.write(f'📋 Template ID: {template.id}')
        
        if eventos_criados:
            self.stdout.write(f'\n📅 Eventos criados:')
            for evt in eventos_criados:
                self.stdout.write(f'   • {evt} (ID: {evt.id}) - {evt.get_sport_display()}')

