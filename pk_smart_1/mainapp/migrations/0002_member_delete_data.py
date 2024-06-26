# Generated by Django 4.2.11 on 2024-04-25 05:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "mem_id",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("mem_pass", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "member",
                "managed": False,
            },
        ),
        migrations.DeleteModel(
            name="data",
        ),
    ]