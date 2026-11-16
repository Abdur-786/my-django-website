from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ('quiz', '0002_alter_question_correct_alter_question_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correct',
            field=models.IntegerField(
                choices=[(1, 'Answer 1'), (2, 'Answer 2'), (3, 'Answer 3')],
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(3),
                ],
            ),
        ),
        migrations.AddConstraint(
            model_name='quizdetail',
            constraint=models.UniqueConstraint(
                fields=('user', 'quiz'),
                name='unique_user_quiz_result',
            ),
        ),
    ]
