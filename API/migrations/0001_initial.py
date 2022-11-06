# Generated by Django 3.2.8 on 2022-11-06 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BasicCountMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CountMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_count_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.basiccountmethod')),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DetailedCountMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EndJunction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_point_ref', models.IntegerField()),
                ('easting', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('northing', models.IntegerField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RoadName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StartJunction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RoadInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('len_mi', models.FloatField(blank=True, null=True)),
                ('len_km', models.FloatField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.category')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.direction')),
                ('junc_end', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='end_junction_road_name', to='API.endjunction')),
                ('junc_start', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='start_junction_road_name', to='API.startjunction')),
                ('road', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.roadname')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.countmethod')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.date')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.location')),
                ('road', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.roadinfo')),
            ],
        ),
        migrations.AddField(
            model_name='countmethod',
            name='detailed_count_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.detailedcountmethod'),
        ),
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_hgvs', models.IntegerField()),
                ('all_motor_vehicles', models.IntegerField()),
                ('pedal_cycles', models.IntegerField()),
                ('two_wheeled_motor_vehicles', models.IntegerField()),
                ('cars_and_taxis', models.IntegerField()),
                ('buses_and_coaches', models.IntegerField()),
                ('lgvs', models.IntegerField()),
                ('hgvs_2_rigid_axle', models.IntegerField()),
                ('hgvs_3_rigid_axle', models.IntegerField()),
                ('hgvs_4_or_more_rigid_axle', models.IntegerField()),
                ('hgvs_3_or_4_articulated_axle', models.IntegerField()),
                ('hgvs_5_articulated_axle', models.IntegerField()),
                ('hgvs_6_articulated_axle', models.IntegerField()),
                ('record', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='API.record')),
            ],
        ),
    ]
