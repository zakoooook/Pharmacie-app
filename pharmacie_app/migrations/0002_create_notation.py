from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('pharmacie_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auteur', models.CharField(blank=True, max_length=100)),
                ('note', models.IntegerField()),
                ('commentaire', models.TextField(blank=True)),
                ('service_satisfait', models.CharField(choices=[('oui', 'Oui'), ('non', 'Non')], max_length=3)),
                ('ecoute', models.CharField(choices=[('oui', 'Oui'), ('non', 'Non')], max_length=3)),
                ('revenir', models.CharField(choices=[('oui', 'Oui'), ('non', 'Non')], max_length=3)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('pharmacien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacie_app.pharmacien')),
            ],
        ),
    ]
