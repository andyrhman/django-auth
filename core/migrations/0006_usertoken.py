# Generated by Django 5.0.4 on 2024-04-15 12:27

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_rename_temp_id_user_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserToken",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("user_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("token", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expired_at", models.DateTimeField()),
            ],
        ),
    ]
