import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from analytics.models import StrategyDocument
from analytics.ai_service import ingest_strategy_document

def seed():
    print("Seeding database...")
    
    docs = [
        {
            "title": "Patch 14.2 Notes: Close Quarters Meta",
            "content": "In patch 14.2, shotguns and SMGs received a 10% buff to hip-fire accuracy. Players struggling in close-quarters combat should prioritize the MP5 or the Nova pump-action. To counter, hold longer angles with an assault rifle."
        },
        {
            "title": "Crossing the 10k Rank Point Threshold",
            "content": "Many players get stuck around 9,000 points. The key to crossing the 10k threshold is consistency rather than high-risk plays. Focus on a K/D ratio above 1.2. If your weapon accuracy is below 25%, spend 15 minutes in aim trainers before queuing for ranked."
        },
        {
            "title": "Handling Loss Streaks",
            "content": "If you lose 3 games in a row, take a 30-minute break. Psychological tilt accounts for a 15% drop in reaction time. Focus on assisting teammates and trading kills rather than taking isolated 1v1 fights when behind."
        }
    ]

    for d in docs:
        doc, created = StrategyDocument.objects.get_or_create(title=d['title'], defaults={'content': d['content']})
        if created:
            print(f"Created doc: {d['title']}")
            # Ingest to Chroma
            success = ingest_strategy_document(d['title'], d['content'])
            if success:
                print("Ingested into vector store.")
            else:
                print("Warning: Google API Key not set, skipped vector embedding.")

if __name__ == '__main__':
    seed()
