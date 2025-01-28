# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Action(models.Model):
    action_id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(db_comment='ID пользователя')
    action_type_id = models.PositiveIntegerField()
    object_type_id = models.PositiveIntegerField()
    object_id = models.PositiveIntegerField()
    period_start = models.DateField(blank=True, null=True)
    period_end = models.DateField(blank=True, null=True)
    difference = models.TextField()
    rollback = models.PositiveIntegerField()
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'action'


class AttachmentsBinding(models.Model):
    attachments_binding_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, db_comment='Имя файла')
    mime_type = models.CharField(max_length=100, blank=True, null=True, db_comment='MIME тип файла')
    path = models.CharField(max_length=255, db_comment='Относительный путь к файлу на сервере')
    object_type = models.CharField(max_length=50,
                                   db_comment='Тип объекта, к которому привязано вложение (indicator | indicator_to_mo | indicator_to_mo_fact etc.)')
    object_id = models.PositiveIntegerField(db_comment='ID объекта, к которому привязано вложение')

    class Meta:
        managed = False
        db_table = 'attachments_binding'
        db_table_comment = 'Таблица для хранения данных о вложениях (файлах). Поскольку вложения могут быть для разных типов объектов и при этом хочется использовать foreign_key, то имеем несколько полей id для каждого из возможных типов объектов.\nПример. Если вложение для факта, то значение id объекта будет только в поле indicator_to_mo_fact'


class ClosedPeriod(models.Model):
    closed_period_id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(blank=True, null=True)
    period_start = models.DateField(db_comment='Дата начала периода')
    period_end = models.DateField(db_comment='Дата окончания периода')
    closed_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'closed_period'
        unique_together = (('period_start', 'period_end'),)


class ClosedPeriodValues(models.Model):
    indicator_to_mo_id = models.PositiveBigIntegerField(db_comment='ID показателя у пользователя в матрице')
    period_start = models.DateField()
    period_end = models.DateField()
    period_type = models.IntegerField()
    weight = models.FloatField()
    plan = models.FloatField(blank=True, null=True)
    fact = models.FloatField(blank=True, null=True)
    result = models.FloatField(blank=True, null=True)
    complexity = models.IntegerField(blank=True, null=True)
    complexity_accepted = models.IntegerField(blank=True, null=True)
    cost_plan = models.FloatField(blank=True, null=True)
    cost_fact = models.FloatField(blank=True, null=True)
    cost_accepted = models.FloatField(blank=True, null=True)
    task_status = models.SmallIntegerField(blank=True, null=True)
    existence_flag = models.IntegerField(blank=True, null=True,
                                         db_comment='Признак наличия записи с сохраненными данными для данного показателя (используется в качестве признака существования сохраненных значений, поскольку некоторые могут иметь null и через значение проверить не получится)')
    task_mark = models.PositiveSmallIntegerField(blank=True, null=True, db_comment='Средняя оценка по задаче')

    class Meta:
        managed = False
        db_table = 'closed_period_values'
        unique_together = (('indicator_to_mo_id', 'period_start', 'period_end', 'period_type'),)
        db_table_comment = 'Сохраненные вычисляемые значения для показателей в закрытых периодах (факт / план и т.д.)'


class DbRollback(models.Model):
    db_rollback_id = models.AutoField(primary_key=True)
    query = models.TextField()

    class Meta:
        managed = False
        db_table = 'db_rollback'


class FieldItemValue(models.Model):
    item_field_value_id = models.AutoField(primary_key=True)
    item_id = models.PositiveIntegerField()
    field_id = models.PositiveIntegerField()
    field_value_id = models.PositiveIntegerField()
    alias = models.CharField(max_length=255)
    require = models.IntegerField()
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'field_item_value'


class FieldType(models.Model):
    field_type_id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'field_type'


class FieldValue(models.Model):
    field_value_id = models.AutoField(primary_key=True)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'field_value'


class HelpItems(models.Model):
    order = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    link = models.TextField()

    class Meta:
        managed = False
        db_table = 'help_items'
        db_table_comment = 'Пункты меню для раздела помощь'


class Indicator(models.Model):
    indicator_id = models.AutoField(primary_key=True, db_comment='ID показателя в бибилиотеке')
    author_id = models.PositiveIntegerField(db_comment='ID автора который добавил показатель')
    pid = models.PositiveIntegerField(db_comment='Вложенность показателя в матрице пользователя')
    indicator_period_id = models.PositiveIntegerField(db_comment='Тип периода, в котором был создан показатель')
    indicator_behaviour_id = models.PositiveIntegerField()
    indicator_calculation_id = models.PositiveIntegerField()
    indicator_calculation_fix = models.PositiveIntegerField()
    indicator_measure_id = models.PositiveIntegerField()
    indicator_measure_fix = models.PositiveIntegerField()
    indicator_interpretation_id = models.PositiveIntegerField()
    indicator_interpretation_fix = models.PositiveIntegerField()
    fact_responsible_type_id = models.PositiveIntegerField()
    plan_responsible_type_id = models.PositiveIntegerField()
    fact_common = models.PositiveIntegerField()
    plan_common = models.PositiveIntegerField()
    fact_period_id = models.IntegerField()
    plan_period_id = models.IntegerField()
    fact_field_set_id = models.IntegerField()
    plan_field_set_id = models.IntegerField()
    name = models.CharField(max_length=255, db_comment='Название показателя')
    name_fix = models.PositiveIntegerField()
    weight = models.PositiveSmallIntegerField(blank=True, null=True, db_comment='Значение веса показателя\r\n')
    weight_fix = models.IntegerField()
    desc = models.TextField(blank=True, null=True)
    desc_fix = models.PositiveIntegerField(blank=True, null=True)
    plan_default = models.DecimalField(max_digits=16, decimal_places=4)
    fact_mo_fix = models.PositiveIntegerField()
    plan_mo_fix = models.PositiveIntegerField()
    dead = models.PositiveIntegerField()
    weight_expression = models.TextField(blank=True, null=True)
    fact_expression = models.TextField(blank=True, null=True)
    plan_expression = models.TextField(blank=True, null=True)
    res_expression = models.TextField(blank=True, null=True)
    repeat_period = models.IntegerField()
    last_repeated_date = models.DateField()
    fact_day = models.PositiveIntegerField()
    fact_month_end = models.PositiveIntegerField()
    protected = models.PositiveIntegerField()
    indicator_key = models.CharField(max_length=32, blank=True, null=True)
    google_synchronize = models.PositiveIntegerField()
    google_id = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField()
    template = models.PositiveIntegerField(db_comment='Является ли показатель шаблоном (отображается ли в библиотеке)')
    calculating_period = models.PositiveIntegerField(
        db_comment='Indicator calculating period (4 - month, 5 - quarter, 6 - year)')
    mark_criterion = models.TextField(blank=True, null=True)
    precision = models.IntegerField(db_comment='Точность округления значений показателя')
    used_supertags = models.TextField(blank=True, null=True,
                                      db_comment='Перечень меток, используемых для расчета показателя (суперметки, массив объектов {tag_id: number, value: any})')
    required_supertags = models.TextField(blank=True, null=True,
                                          db_comment='Перечень обязательных меток для добавляемых фактов (суперметки)')
    fact_default = models.DecimalField(max_digits=16, decimal_places=4, db_comment='Default fact value')
    auto_create_default_fact = models.IntegerField(
        db_comment='Whether to automatically create a default fact on expected dates')

    class Meta:
        managed = False
        db_table = 'indicator'


class IndicatorBehaviour(models.Model):
    indicator_behaviour_id = models.AutoField(primary_key=True, db_comment='Очередной типов показателей')
    key = models.CharField(max_length=255, db_comment='Типы показателей')
    hidden = models.PositiveIntegerField(db_comment='Обозначение скрытых типов показателей')

    class Meta:
        managed = False
        db_table = 'indicator_behaviour'


class IndicatorFunction(models.Model):
    indicator_function_id = models.AutoField(primary_key=True, db_comment='ID математических функций')
    key = models.CharField(max_length=255, db_comment='Ключ основных математических функций в программе')
    function = models.CharField(max_length=255, db_comment='Основные математические функции в программе')
    order = models.PositiveIntegerField(db_comment='Очередность математических функций')

    class Meta:
        managed = False
        db_table = 'indicator_function'


class IndicatorInterpretation(models.Model):
    indicator_interpretation_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_comment='Название функций в программе')
    function = models.CharField(max_length=255)
    protected = models.PositiveIntegerField(db_comment='Настройка позволяющая включить защиту от изменений')
    scale = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'indicator_interpretation'


class IndicatorInterpretationPoint(models.Model):
    indicator_interpretation_point_id = models.AutoField(primary_key=True)
    indicator_interpretation = models.ForeignKey(IndicatorInterpretation, models.DO_NOTHING)
    x = models.FloatField()
    y = models.FloatField()
    label = models.CharField(max_length=255)
    desc = models.TextField()

    class Meta:
        managed = False
        db_table = 'indicator_interpretation_point'


class IndicatorLockers(models.Model):
    indicator = models.ForeignKey(Indicator, models.DO_NOTHING, db_comment='Base indicator ID')
    field_name = models.CharField(max_length=50, db_comment='Locked field name')

    class Meta:
        managed = False
        db_table = 'indicator_lockers'
        unique_together = (('indicator', 'field_name'),)
        db_table_comment = "Table contains base indicator fields lockers' state (locked fields records only). All indicator instances will be affacted with field value changes if a field is locked. Otherwise, fields changes affect only the changing base indicator itself."


class IndicatorMeasure(models.Model):
    indicator_measure_id = models.AutoField(primary_key=True, db_comment='Очередность единиц измерения')
    name = models.CharField(unique=True, max_length=255, db_comment='Название единиц измерения')
    is_money = models.PositiveIntegerField(db_comment='Тип денежный или нет')

    class Meta:
        managed = False
        db_table = 'indicator_measure'


class IndicatorMeasureConversion(models.Model):
    indicator_measure_conversion_id = models.AutoField(primary_key=True)
    from_id = models.PositiveIntegerField()
    to_id = models.PositiveIntegerField()
    factor = models.DecimalField(max_digits=65, decimal_places=14)
    since = models.DateField()

    class Meta:
        managed = False
        db_table = 'indicator_measure_conversion'
        unique_together = (('from_id', 'to_id', 'since'),)


class IndicatorOperation(models.Model):
    indicator_operation_id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=255)
    function = models.CharField(max_length=255, db_comment='Все математические операции в программе')
    order = models.PositiveIntegerField(db_comment='Очередность')

    class Meta:
        managed = False
        db_table = 'indicator_operation'


class IndicatorPeriod(models.Model):
    indicator_period_id = models.AutoField(primary_key=True, db_comment='Очередность в программе')
    key = models.CharField(max_length=255, db_comment='Периоды времени (день, неделя, квартал и тд)')

    class Meta:
        managed = False
        db_table = 'indicator_period'


class IndicatorPrivateLibrary(models.Model):
    mo = models.ForeignKey('Mo', models.DO_NOTHING, db_comment='Id объекта управления')
    indicator = models.ForeignKey(Indicator, models.DO_NOTHING, db_comment='Id базового показателя')

    class Meta:
        managed = False
        db_table = 'indicator_private_library'
        unique_together = (('mo', 'indicator'),)
        db_table_comment = 'Таблица содержит информацию о включении базовых показателей в личную библиотеку конкретного ОУ в виде связок indicator_id -> mo_id'


class IndicatorResponsible(models.Model):
    indicator_id = models.PositiveIntegerField(db_comment='ID показателя в бибилиотеке показателей')
    mo_id = models.PositiveIntegerField(db_comment='ID объекта управления')
    plan = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'indicator_responsible'


class IndicatorSecondaryFact(models.Model):
    indicator_secondary_fact_id = models.AutoField(primary_key=True)
    indicator_to_mo_id = models.IntegerField(db_comment='ID показателя в матрице объекта управления')
    res = models.DecimalField(max_digits=15, decimal_places=4)
    fact = models.DecimalField(max_digits=15, decimal_places=4)
    plan = models.DecimalField(max_digits=15, decimal_places=4)
    weight = models.IntegerField(db_comment='Значение веса')
    complexity = models.DecimalField(max_digits=15, decimal_places=4)
    mark = models.DecimalField(max_digits=15, decimal_places=4)
    plan_cost = models.DecimalField(max_digits=15, decimal_places=4)
    fact_cost = models.DecimalField(max_digits=15, decimal_places=4)
    accept_cost = models.DecimalField(max_digits=15, decimal_places=4)
    plan_cost_task = models.DecimalField(max_digits=15, decimal_places=4)
    fact_cost_task = models.DecimalField(max_digits=15, decimal_places=4)
    fact_cost_kpi_task = models.DecimalField(max_digits=15, decimal_places=4)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'indicator_secondary_fact'


class IndicatorTaskStatus(models.Model):
    indicator_task_status_id = models.AutoField(primary_key=True, db_comment='ID записи в таблице')
    key = models.CharField(max_length=255, db_comment='Перечисление статусов закрытия задач')

    class Meta:
        managed = False
        db_table = 'indicator_task_status'


class IndicatorToMo(models.Model):
    indicator_to_mo_id = models.AutoField(primary_key=True, db_comment='ID показателя в матрице сотрудника')
    indicator_id = models.PositiveIntegerField(db_comment='ID показателя в библиотеке показателей')
    mo_id = models.PositiveIntegerField(db_comment='ID сотрудника в оргструктуре')
    author_id = models.PositiveIntegerField(db_comment='ID cотрудника который добавил показатель в матрицу')
    indicator_calculation_id = models.PositiveIntegerField()
    indicator_measure_id = models.PositiveIntegerField()
    priority = models.PositiveIntegerField()
    sequence = models.PositiveIntegerField(db_comment='Очередность показателей')
    fact_field_set_id = models.PositiveIntegerField()
    plan_field_set_id = models.PositiveIntegerField()
    is_notify = models.IntegerField()
    notify_days = models.IntegerField(blank=True, null=True)
    notify_regular = models.IntegerField(blank=True, null=True)
    live_start = models.DateField(db_comment='Начало действия показателя')
    live_end = models.DateField(db_comment='Конец действия показателя')
    created = models.DateTimeField(blank=True, null=True, db_comment='Дата создания показателя')
    fact_day = models.PositiveIntegerField()
    fact_month_end = models.PositiveIntegerField()
    plan_periodic_counting = models.PositiveIntegerField()
    execution_start = models.DateField(blank=True, null=True)
    execution_end = models.DateField(blank=True, null=True)
    calendar_from = models.DateTimeField(blank=True, null=True)
    calendar_to = models.DateTimeField(blank=True, null=True)
    live_start_time = models.TimeField(blank=True, null=True)
    is_pay_main = models.PositiveIntegerField(db_comment='Детализация показателя для типа Оплата')
    last_repeat = models.DateField(blank=True, null=True)
    show_all_facts = models.IntegerField()
    precision = models.IntegerField(db_comment='Точность округления значений показателя')
    hidden = models.IntegerField(
        db_comment='Скрытие показателя от всех кроме администраторов и сотрудников которые ответственные за ввод плана\\факта')
    required_supertags = models.TextField(blank=True, null=True,
                                          db_comment='Перечень обязательных меток для добавляемых фактов (суперметки)')

    class Meta:
        managed = False
        db_table = 'indicator_to_mo'


class IndicatorToMoFact(models.Model):
    indicator_to_mo_fact_id = models.AutoField(primary_key=True)
    indicator_to_mo_id = models.PositiveIntegerField(db_comment='ID показателя в матрице объекта управления')
    true_indicator_to_mo_id = models.PositiveIntegerField(
        db_comment='Истинный indicatorToMoId показателя, для которого был внесен факт (без учета признака common)')
    user_id = models.PositiveIntegerField(blank=True, null=True, db_comment='ID пользователя')
    plan = models.IntegerField(db_comment='Обозначение плана или факта (0-факт 1 - план)')
    value = models.DecimalField(max_digits=16, decimal_places=4, blank=True, null=True,
                                db_comment='Значение факт или плана')
    comment = models.TextField(blank=True, null=True, db_comment='Комментарий плана или факта')
    author = models.CharField(max_length=100, blank=True, null=True, db_comment='Автор плана\\факта')
    measure_id = models.IntegerField(blank=True, null=True)
    in_measure_value = models.IntegerField(blank=True, null=True)
    complexity = models.IntegerField(blank=True, null=True)
    mark = models.IntegerField(blank=True, null=True)
    fact_time = models.DateTimeField(db_comment='Дата плана\\факта')
    post_time = models.DateTimeField(db_comment='Дата добавления плана\\факта')
    common = models.PositiveIntegerField()
    mark_ignored = models.IntegerField()
    dependant_fact_id = models.PositiveIntegerField(db_comment='Dependant fact id (eg. rating fact)')
    period_start = models.DateField(blank=True, null=True, db_comment='Дата начала периода (используется для планов)')
    period_end = models.DateField(blank=True, null=True, db_comment='Дата окончания периода (используется для планов)')

    class Meta:
        managed = False
        db_table = 'indicator_to_mo_fact'


class IndicatorToMoHst(models.Model):
    indicator_to_mo_hst_id = models.AutoField(primary_key=True, db_comment='Номер записи в таблице')
    indicator_to_mo_id = models.PositiveIntegerField(db_comment='ID показателя в матрице объекта управления')
    pid = models.PositiveIntegerField()
    name = models.CharField(max_length=255, db_comment='Название показателя')
    desc = models.TextField()
    weight = models.PositiveSmallIntegerField(blank=True, null=True, db_comment='Вес показателя')
    indicator_calculation_id = models.PositiveIntegerField()
    indicator_interpretation_id = models.PositiveIntegerField()
    fact_period_id = models.PositiveIntegerField()
    plan_period_id = models.PositiveIntegerField()
    plan_as_last_fact = models.IntegerField()
    plan_default = models.DecimalField(max_digits=16, decimal_places=4, blank=True, null=True)
    standard_operation_time = models.IntegerField()
    weight_expression = models.TextField()
    weight_calculation = models.TextField(blank=True, null=True)
    weight_dependences = models.TextField(blank=True, null=True)
    weight_expression_calculated = models.IntegerField()
    fact_expression = models.TextField()
    fact_calculation = models.TextField(blank=True, null=True)
    fact_dependences = models.TextField(blank=True, null=True)
    fact_expression_calculated = models.IntegerField()
    plan_expression = models.TextField()
    plan_calculation = models.TextField(blank=True, null=True)
    plan_dependences = models.TextField(blank=True, null=True)
    plan_expression_calculated = models.IntegerField()
    res_expression = models.TextField()
    res_calculation = models.TextField(blank=True, null=True)
    res_dependences = models.TextField(blank=True, null=True)
    res_expression_calculated = models.IntegerField()
    linked_ids = models.TextField(blank=True, null=True)
    consumers = models.TextField()
    order = models.PositiveSmallIntegerField()
    since = models.DateField()
    mark_criterion = models.TextField(blank=True, null=True)
    dependencies = models.TextField(blank=True, null=True,
                                    db_comment='Поле хранит информацию о всех зависимостях (indicator_to_mo_id) исходя из формул (вес/план/факт/результат) с полной глубиной (включая зависимости зависимостей)')
    calculating_period = models.PositiveIntegerField(
        db_comment='Indicator calculating period (4 - month, 5 - quarter, 6 - year)')
    used_supertags = models.TextField(blank=True, null=True,
                                      db_comment='Перечень меток, используемых для расчета показателя (суперметки, массив объектов {tag_id: number, value: any})')
    auto_supertags = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True,
                                      db_comment='Id меток для автоматического создания при сохранении каждого нового факта')
    fact_default = models.DecimalField(max_digits=16, decimal_places=4, db_comment='Default fact value')

    class Meta:
        managed = False
        db_table = 'indicator_to_mo_hst'
        unique_together = (('indicator_to_mo_id', 'indicator_to_mo_hst_id', 'since'), ('indicator_to_mo_id', 'since'),)


class IndicatorToMoResponsible(models.Model):
    indicator_to_mo_id = models.PositiveIntegerField(db_comment='ID показателя в матрице объекта управления')
    mo_id = models.PositiveIntegerField(db_comment='ID объекта управления')
    plan = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'indicator_to_mo_responsible'


class Layouts(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=70, db_collation='utf8mb3_general_ci', blank=True, null=True)
    layout = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'layouts'


class Mo(models.Model):
    mo_id = models.AutoField(primary_key=True, db_comment='ID объекта управления')
    mo_type_id = models.PositiveIntegerField()
    mo_position_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255, db_comment='Название объекта управления')
    live_start = models.DateField(db_comment='Дата создания объекта управления')
    live_end = models.DateField(db_comment='Дата удаления объекта управления')
    hidden = models.PositiveIntegerField(db_comment='Функция скрытия объекта управления (0 - виден, 1 - скрыт)')
    tarif_id = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    auto_supertags = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True,
                                      db_comment='Данные меток для автоматического добавления для каждого нового факта, добавляемого для показателя, которым владеет ОУ')

    class Meta:
        managed = False
        db_table = 'mo'


class MoAliases(models.Model):
    mo = models.ForeignKey(Mo, models.DO_NOTHING, db_comment='ID объекта управления')
    name_alias = models.CharField(max_length=255, db_comment='Наименования parser_id объекта управления')

    class Meta:
        managed = False
        db_table = 'mo_aliases'
        db_table_comment = 'Альтернативные названия для любого из ОУ'


class MoHst(models.Model):
    mo_hst_id = models.AutoField(primary_key=True, db_comment='ID записи в таблице')
    mo_id = models.PositiveIntegerField(db_comment='ID объекта управления')
    pid = models.PositiveIntegerField()
    pay_category_id = models.PositiveIntegerField()
    since = models.DateField()
    consumers = models.TextField()
    order = models.PositiveSmallIntegerField()
    hierarchy_path = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True, db_comment='Название объекта управления')
    signers = models.TextField()

    class Meta:
        managed = False
        db_table = 'mo_hst'


class MoPosition(models.Model):
    mo_position_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'mo_position'


class Option(models.Model):
    option_id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(db_comment='ID сотрудника')
    key = models.CharField(max_length=100, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, db_comment='Описание параметра')
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'option'
        unique_together = (('user_id', 'key'), ('user_id', 'key'),)


class Report(models.Model):
    report_id = models.AutoField(primary_key=True, db_comment='ID записи в таблице')
    user_id = models.PositiveIntegerField(db_comment='ID сотрудника')
    name = models.CharField(max_length=255)
    since = models.DateField()
    protected = models.PositiveIntegerField()
    report_key = models.CharField(max_length=32)
    sort = models.CharField(max_length=255)
    hidden_cols = models.TextField(blank=True, null=True)
    columns = models.TextField(blank=True, null=True,
                               db_comment='Перечень отображаемых по умолчанию колонок в отчете в формате JSON (объект ReportColumn)')
    template_id = models.PositiveIntegerField(db_comment='ID шаблона из report_templates')
    indicator_behaviour_id = models.TextField(blank=True, null=True,
                                              db_comment='Comma-separated list of indicator behaviour ids to include in the report')
    indicator_id = models.TextField(blank=True, null=True,
                                    db_comment='Comma-separated list of indicator ids to include in the report')
    mo_id = models.TextField(blank=True, null=True,
                             db_comment='Comma-separated list of mo ids to include in the report')
    description = models.TextField(blank=True, null=True, db_comment='Описание отчета')
    tag_id = models.TextField(blank=True, null=True,
                              db_comment='Список id тегов, по которым будет производится выборка данных')
    weighted_only = models.IntegerField(
        db_comment='Учитывать ли вес показателей при подготовке данных для отчета. Если true, то будут выведены только показатели с весом > 0')
    tags_condition = models.PositiveIntegerField(db_comment='Tags select conditions (true - OR, false - AND)')
    period_start = models.DateField(blank=True, null=True)
    period_end = models.DateField(blank=True, null=True)
    use_own_period = models.IntegerField(
        db_comment='Использовать период из параметров отчета (true) или текущее значение периода в приложении (false, по умолчанию)')
    cols_sort = models.CharField(max_length=100, blank=True, null=True,
                                 db_comment='Тип сортировки показателей в столбцах (id | name | type etc.)')
    period_type = models.IntegerField(blank=True, null=True)
    pid = models.PositiveIntegerField()
    import_specs = models.TextField(blank=True, null=True, db_comment='Разметка файла CSV для импорта')
    config = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report'


class Role(models.Model):
    role_id = models.AutoField(primary_key=True, db_comment='ID роли\r\n')
    name = models.CharField(max_length=255, db_comment='Название роли')
    key = models.CharField(max_length=16, blank=True, null=True)
    accessible_mo_all = models.IntegerField()
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'role'


class RoleAccessibleMo(models.Model):
    role_accessible_mo_id = models.AutoField(primary_key=True, db_comment='ID записи в таблице')
    role_id = models.PositiveIntegerField(db_comment='ID роли')
    mo_id = models.PositiveIntegerField(db_comment='ID объекта управления')

    class Meta:
        managed = False
        db_table = 'role_accessible_mo'
        unique_together = (('mo_id', 'role_id'),)


class RoleToUser(models.Model):
    role_to_user_id = models.AutoField(primary_key=True, db_comment='ID роли объекта управления')
    role_id = models.PositiveIntegerField(db_comment='ID роли ')
    mo_id = models.PositiveIntegerField(blank=True, null=True, db_comment='ID объекта управления')
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'role_to_user'


class Rule(models.Model):
    rule_id = models.AutoField(primary_key=True)
    pid = models.PositiveIntegerField()
    check_key = models.CharField(unique=True, max_length=255)
    key = models.CharField(max_length=255)
    default = models.IntegerField()
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rule'


class RuleToRole(models.Model):
    rule_to_role_id = models.AutoField(primary_key=True)
    rule_id = models.PositiveIntegerField()
    role_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'rule_to_role'
        unique_together = (('rule_id', 'role_id'),)


class SchemaMigrations(models.Model):
    version = models.BigIntegerField(primary_key=True)
    dirty = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'schema_migrations'


class Subscriptions(models.Model):
    object_type = models.CharField(max_length=50,
                                   db_comment='Тип объекта подписки (indicator_to_mo | indicator | mo etc.)')
    object_id = models.PositiveIntegerField(db_comment='ID объекта')
    mo_id = models.PositiveIntegerField(db_comment='ID подписчика')

    class Meta:
        managed = False
        db_table = 'subscriptions'
        unique_together = (('object_type', 'object_id', 'mo_id'),)
        db_table_comment = 'Подписки на рассылку уведомлений об изменениях объектов'


class Supertags(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment='ID записи в таблице')
    name = models.CharField(unique=True, max_length=255, db_comment='Название')
    key = models.CharField(unique=True, max_length=255, db_comment='Уникальный ключ метки')
    values = models.TextField(blank=True, null=True,
                              db_comment='Доступные значения метки в формате json, в виде массива объектов {title: string, value: any}')
    values_source = models.PositiveIntegerField(
        db_comment='Тип источника значений (0 - статический массив значений в поле values, 1 и более динамические)')

    class Meta:
        managed = False
        db_table = 'supertags'
        db_table_comment = 'Справочник меток ("супер"-метки)'


class SupertagsBindings(models.Model):
    id = models.BigAutoField(primary_key=True)
    fact = models.ForeignKey(IndicatorToMoFact, models.DO_NOTHING, db_comment='id факта')
    tag = models.ForeignKey(Supertags, models.DO_NOTHING, db_comment='id метки')
    tag_value = models.CharField(max_length=255, db_comment='Значение метки')

    class Meta:
        managed = False
        db_table = 'supertags_bindings'
        unique_together = (('fact', 'tag', 'tag_value'),)


class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True, db_comment='ID сотрудника')
    login = models.CharField(unique=True, max_length=150, db_comment='Логин сотрудника')
    password = models.TextField(db_comment='Пароль сотрудника')
    first_name = models.CharField(max_length=40, db_comment='Фамилия сотрудника')
    middle_name = models.CharField(max_length=40, db_comment='Имя сотрудника')
    last_name = models.CharField(max_length=40, db_comment='Отчество сотрудника')
    email = models.CharField(max_length=255, blank=True, null=True)
    sms_phone = models.PositiveBigIntegerField(blank=True, null=True)
    emp_code = models.CharField(unique=True, max_length=15, blank=True, null=True,
                                db_comment='Табельный номер сотрудника')
    photo = models.CharField(max_length=255, blank=True, null=True)
    sex = models.IntegerField(db_comment='Пол сотрудника')
    birthday = models.DateField(blank=True, null=True, db_comment='Дата рождения')
    country = models.CharField(max_length=32, db_comment='Страна')
    region = models.CharField(max_length=32, db_comment='Регион\\область')
    city = models.CharField(max_length=32, db_comment='Город')
    latitude = models.CharField(max_length=16)
    longitude = models.CharField(max_length=16)
    status = models.PositiveIntegerField(db_comment='Статус работает или нет')
    description = models.TextField(blank=True, null=True)
    onesignal_id = models.TextField(blank=True, null=True, db_comment='OneSignal Player ID(s)')
    theme = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserToMo(models.Model):
    user_to_mo_id = models.AutoField(primary_key=True, db_comment='Сотрудник прикрепленный к объекту управления')
    user_id = models.PositiveIntegerField(db_comment='ID сотрудника')
    mo_id = models.PositiveIntegerField(db_comment='ID объекта управления\r\n')
    live_start = models.DateField(db_comment='Дата начала ')
    live_end = models.DateField(db_comment='Дата окончания')

    class Meta:
        managed = False
        db_table = 'user_to_mo'
