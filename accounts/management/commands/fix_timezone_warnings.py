"""
Management command to fix timezone warnings by converting naive datetime objects
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.apps import apps
import warnings

class Command(BaseCommand):
    help = 'Fix timezone warnings by converting naive datetime objects to timezone-aware'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Fixing timezone warnings...')
        
        # Suppress the warnings temporarily while we fix them
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            
            fixed_count = 0
            
            # Get all models with DateTimeField
            models_to_fix = []
            
            for model in apps.get_models():
                datetime_fields = []
                for field in model._meta.fields:
                    if field.__class__.__name__ == 'DateTimeField':
                        datetime_fields.append(field.name)
                
                if datetime_fields:
                    models_to_fix.append((model, datetime_fields))
            
            # Fix each model
            for model, datetime_fields in models_to_fix:
                model_name = f"{model._meta.app_label}.{model._meta.model_name}"
                self.stdout.write(f'Checking {model_name}...')
                
                try:
                    objects_to_update = []
                    
                    for obj in model.objects.all():
                        needs_update = False
                        
                        for field_name in datetime_fields:
                            field_value = getattr(obj, field_name)
                            
                            if field_value and field_value.tzinfo is None:
                                # Convert naive datetime to timezone-aware
                                aware_datetime = timezone.make_aware(field_value)
                                setattr(obj, field_name, aware_datetime)
                                needs_update = True
                        
                        if needs_update:
                            objects_to_update.append(obj)
                    
                    # Bulk update if there are objects to fix
                    if objects_to_update:
                        model.objects.bulk_update(objects_to_update, datetime_fields)
                        fixed_count += len(objects_to_update)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✅ Fixed {len(objects_to_update)} objects in {model_name}'
                            )
                        )
                    else:
                        self.stdout.write(f'✅ No issues found in {model_name}')
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Error fixing {model_name}: {str(e)}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n🎉 Timezone fix complete! Fixed {fixed_count} objects total.'
                )
            )
            
            if fixed_count > 0:
                self.stdout.write(
                    self.style.WARNING(
                        '\n⚠️  Note: You may need to restart your Django server for changes to take effect.'
                    )
                )
