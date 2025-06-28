from django.core.management.base import BaseCommand
from kidney_stones_app.models import OxalateContent
import json


class Command(BaseCommand):
    help = 'Load oxalate content data from JSON file into database'

    def get_oxalate_level(self, oxalate_mg):
        """Determine oxalate level based on mg content"""
        if oxalate_mg >= 100:
            return 'Very High'
        elif oxalate_mg >= 50:
            return 'High'
        elif oxalate_mg >= 10:
            return 'Medium'
        else:
            return 'Low'

    def handle(self, *args, **options):
        try:
            # Clear existing data
            OxalateContent.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(
                'Cleared existing oxalate data'))

            # Load data from JSON file
            with open('oxalate_en.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            food_data_list = data.get('food_data', [])

            # Create objects
            oxalate_objects = []
            for food_item in food_data_list:
                oxalate_level = self.get_oxalate_level(food_item['oxalate_mg'])
                oxalate_objects.append(OxalateContent(
                    food=food_item['food'],
                    type=food_item['type'],
                    oxalate_mg=food_item['oxalate_mg'],
                    serving_size='1 cup (raw)',  # Default serving size
                    oxalate_level=oxalate_level
                ))

            # Bulk create for efficiency
            OxalateContent.objects.bulk_create(oxalate_objects)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully loaded {len(food_data_list)} oxalate content records')
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    'oxalate_en.json file not found in the project root')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading oxalate data: {str(e)}')
            )
