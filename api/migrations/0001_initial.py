from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=32, unique=True)),
                ('about', models.TextField(blank=True, default='')),
                ('password_hash', models.CharField(max_length=256)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('images', models.JSONField(blank=True, default=list)),
                ('phone', models.CharField(max_length=32)),
                ('category', models.CharField(choices=[('automobiles', 'Автомобили'), ('phones', 'Телефоны'), ('realty', 'Недвижимость')], max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='api.member')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='listing',
            index=models.Index(fields=['category', 'created_at'], name='api_listin_categor_0b584b_idx'),
        ),
        migrations.AddIndex(
            model_name='listing',
            index=models.Index(fields=['price'], name='api_listin_price_3f5484_idx'),
        ),
        migrations.CreateModel(
            name='ChatThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('listing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='threads', to='api.listing')),
                ('member_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads_as_a', to='api.member')),
                ('member_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads_as_b', to='api.member')),
            ],
        ),
        migrations.AddIndex(
            model_name='chatthread',
            index=models.Index(fields=['member_a', 'member_b'], name='api_chatth_member__f800a2_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='chatthread',
            unique_together={('member_a', 'member_b', 'listing')},
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='api.member')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='api.chatthread')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['thread', 'created_at'], name='api_messag_thread__61c66c_idx'),
        ),
    ]
