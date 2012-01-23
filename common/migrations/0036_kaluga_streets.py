# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        KALUGA_UUID = '2f1589f6-bd2d-11e0-99d3-00163e45e1c0'

        STREETS="""
1-й Академический пр.
1-й Берендяковский пер.
1-й Больничный пер.
1-й Заводской пр.
1-й Загородный пр.
1-й Карьерный пер.
1-й Красноармейский пер.
1-й Красносельский пер.
1-й Осенний пр.
1-й Пестеля пер.
1-й Садовый пер.
1-й Секиотовский пр.
1-й Тарутинский пр.
1-й Удачный пер.
1-й Черносвитинский пер.
1-я Загородная ул.
1-я Тарусская ул.
2-й Академический пр.
2-й Берендяковский пер.
2-й Больничный пер.
2-й Брусничный пер.
2-й Заводской пр.
2-й Загородный пр.
2-й Интернациональный пер.
2-й Карьерный пер.
2-й Красноармейский пер.
2-й Красносельский пер.
2-й Осенний пр.
2-й Пестеля пер.
2-й Садовый пер.
2-й Секиотовский пр.
2-й Стекольный пер.
2-й Тарутинский пр.
2-й Тульский пер.
2-й Удачный пер.
2-й Черносвитинский пер.
2-я Загородная ул.
2-я Киевка ул.
2-я Набережная ул.
2-я Тарусская ул.
3-5 июля ул.
3-й Академический пр.
3-я Тарусская ул.
4-я Тарусская ул.
40-летия Октября ул.
5-я линия ул.
5-я Тарусская ул.
6-я Тарусская ул.
7-я Тарусская ул.
8 Марта пер.
8 Марта ул.
8-я Тарусская ул.
Азаровская ул.
Азаровский пр.
Академика Глушко ул.
Академика Королева ул.
Академическая ул.
Александра Матросова ул.
Алексеевская ул.
Аллейная ул.
Анненки ул.
Ароматная ул.
Аэропортовская ул.
Аэропортовский пер.
Багговута ул.
Баженова ул.
Байконур б-р
Байконурская ул.
Баррикад пер.
Баррикад ул.
Баумана ул.
Беговая ул.
Белинского ул.
Белокирпичная ул.
Беляева ул.
Березовая ул.
Березуевская ул.
Березуевский пер.
Берендяковская ул.
Березовый пер.
Билибина ул.
Богородицкая ул.
Богородицкий пер.
Болдина ул.
Болотная ул.
Болотникова ул.
Больничная ул.
Большевиков ул.
Брусничный пер.
Бутома ул.
Бутырская ул.
Вагонная ул.
Вагонный пер.
Валентины Никитиной ул.
Верховая ул.
Веры Андриановой ул.
Весенняя ул.
Взлетная ул.
Вилонова ул.
Вишневая ул.
Вишневского ул.
Воинская ул.
Воинский пер.
Воинский пр.
Войкова ул.
Вокзальная пл.
Волковская ул.
Волковский пер.
Волковский пр.
Вооруженного Восстания ул.
Воробьевская ул.
Воробьевский пер.
Воронина ул.
Воскресенская ул.
Воскресенский пер.
Восточная ул.
Восточный пр.
Врубовая ул.
Врубовой пер.
Выгонная ул.
Высокая ул.
Выставочная ул.
Гагарина ул.
Газовая ул.
Гамазейная ул.
Гамазейный пер.
Гвардейская ул.
Генерала Попова ул.
Георгиевская ул.
Георгия Димитрова ул.
Герцена ул.
Глаголева ул.
Гоголя ул.
Городенская ул.
Гостинорядский пер.
Грабцевское ш.
Григоров пер.
Гурьянова ул.
Дальний пер.
Дальняя ул.
Даниловский пер.
Дарвина пер.
Дарвина пр.
Дарвина ул.
Дачная ул.
Декабристов (проезд) туп.
Декабристов ул.
Детей коммунаров ул.
Дзержинского ул.
Добровольского ул.
Дорожная ул.
Дорожная ул.
Дорожный пер.
Достоевского ул.
Дружбы ул.
Дубрава ул.
Ермоловская ул.
Ждамировская ул.
Железняки ул.
Забойная ул.
Забойный пер.
Заводская ул.
Заводской пер.
Загородносадский (пер.) пр.
Заокская ул.
Западная ул.
Заречная ул.
Заречный пер.
Звездная ул.
Зеленая ул.
Зеленый Крупец ул.
Зерновая ул.
Знаменская ул.
Инженерная ул.
Интернациональный пер.
Ипподромная ул.
Кавказ ул.
Калинина пер.
Калинина ул.
Калужка ул.
Калужская ул.
Калужский пер.
Калужского ополчения ул.
Каракозова пер.
Карачевская ул.
Карачевский пер.
Карла Либкнехта ул.
Карла Маркса пл.
Карла Маркса ул.
Карпова пер.
Карпова ул.
Карьерная ул.
Каштановая ул.
Кибальчича ул.
Киевка ул.
Киевская ул.
Киевский пер.
Киевский пр.
Кирова ул.
Кирпичная ул.
Кирпичный завод МПС ул.
Кирпичный пер.
Клары Цеткин пер.
Клары Цеткин туп.
Клюквина ул.
Кожедуба ул.
Колхозная ул.
Колхозный пер.
Колхозный пр.
Коммунальная ул.
Комсомольская роща ул.
Комсомольская ул.
Комсомольский пер.
Константиновых ул.
Конюшенная ул.
Кооперативная ул.
Кооперативный поселок ул.
Короткий пер.
Космонавта Волкова ул.
Космонавта Комарова ул.
Космонавта Пацаева ул.
Крайний (проезд) пер.
Красная Гора ул.
Красноармейская ул.
Краснопивцева ул.
Красносельская ул.
Красный пр.
Кропоткина ул.
Кубяка ул.
Кукареки ул.
Курсантов ул.
Кутузова ул.
Лаврентьевская ул.
Лаврентьевский пер.
Лазоревая ул.
Лапушкин пер.
Ленина ул.
Лесная ул.
Лесозаводская ул.
Лесозаводской пер.
Линейная ул.
Линейный пер.
Лиственная ул.
Литвиновская ул.
Литвиновский пер.
Литейная ул.
Литейный пер.
Ломоносова ул.
Луговая ул.
Луговой пер.
Луначарского пер.
Луначарского ул.
Льва Толстого ул.
Майская ул.
Максима Горького пер.
Максима Горького ул.
Малинники пер.
Малинники ул.
Малоярославецкая ул.
Малый пер.
Марата ул.
Маршала Жукова ул.
Маршала Зимина ул.
Маяковского пер.
Маяковского пл.
Маяковского ул.
Мелиораторов ул.
Мельничная ул.
Механизаторов пер.
Механизаторов ул.
Мира пл.
Михайловская ул.
Михалевская ул.
Михалевский пер.
Мичурина ул.
Можайская ул.
Молодежная ул.
Монастырская ул.
Московская пл.
Московская ул.
Моторная ул.
Моторостроителей б-р
Набережная ул.
Нагорная ул.
Небесная ул.
Некрасова ул.
Нефтебаза ул.
Нижне-Гамазейная ул.
Нижне-Лаврентьевская ул.
Нижне-Лаврентьевский пер.
Никитина пер.
Никитина ул.
Николая Островского ул.
Николо-Козинская ул.
Новаторская ул.
Новаторский пер.
Новая стройка ул.
Новая ул.
Новозаречная ул.
Новолаврентьевская ул.
Новолаврентьевский пер.
Новорежская ул.
Новосельская ул.
Новослободская ул.
Новослободский пр.
Новый пер.
Овражная ул.
Огарева ул.
Огородная ул.
Одоевское ш.
Окружная ул.
Окружной пер.
Окская ветка ул.
Октябрьская ул.
Октябрьский пер.
Октябрьский пр.
Ольговка ул.
Ольговская ул.
Ольговский пер.
Осенняя ул.
Отбойная ул.
Отбойный пер.
Открытая ул.
Параллельная ул.
Парижской Коммуны ул.
Парковая ул.
Парковый пер.
Паровозный пер.
Первомайская ул.
Первых коммунаров ул.
Первых космонавтов пл.
Переходная ул.
Пестеля ул.
Песчаная ул.
Песчаный пер.
Пионерская ул.
Планерная ул.
Платова ул.
Плеханова ул.
Победы пл.
Подвойского пер.
Подвойского ул.
Подгорная ул.
Покровская ул.
Поле Свободы пер.
Поле Свободы ул.
Полевая ул.
Полянка ул.
Поселковая ул.
Поселковый пер.
Постовалова ул.
Почтовый пер.
Правды ул.
Правобережный пр.
Привокзальная ул.
Пригородная ул.
Прирельсовая ул.
Проезжая ул.
Пролетарская ул.
Промежуточная ул.
Промышленная ул.
Прончищева пер.
Прончищева ул.
Просторная ул.
Прохладная ул.
Путейская ул.
Пухова ул.
Пушкина пер.
Пушкина ул.
Работниц ул.
Радищева ул.
Резванская ул.
Резервный пер.
Родниковая ул.
Ромодановская ул.
Ромодановские Дворики пер.
Ромодановские Дворики ул.
Рылеева ул.
Садовая ул.
Салтыкова-Щедрина пер.
Салтыкова-Щедрина ул.
Свердлова пер.
Светлая ул.
Северная ул.
Северный пер.
Секиотовская ул.
Секиотовский пер.
Секиотовское кольцо ул.
Сельская ул.
Сельский пер.
Семеново Городище пер.
Семеново Городище ул.
Силикатная ул.
Силикатный пер.
Сиреневая ул.
Сиреневый б-р
Складская ул.
Смоленская ул.
Смоленский пер.
Советская ул.
Советский пер.
Советский пр.
Совхозный пер.
Солнечная ул.
Сосновая ул.
Сосновый пр.
Софьи Перовской (тупик) пер.
Социалистическая ул.
Спартака ул.
Спичечная ул.
Спортивная ул.
Средний пер.
Сретенская ул.
Станционная ул.
Станционный пер.
Старая водокачка ул.
Старичков пер.
Старообрядческий пер.
Старый Торг пл.
Стеклянников сад ул.
Стекольная ул.
Стекольный пер.
Степана Разина ул.
Степная ул.
Степной пр.
Строительный пер.
Суворова пер.
Суворова ул.
Тарутинская ул.
Театральная пл.
Театральная ул.
Телевизионная ул.
Тельмана ул.
Тепличная ул.
Теренинский пер.
Терепецкая ул.
Терепецкий пер.
Терепецкий пр.
Терепецкое кольцо ул.
Тихая ул.
Товарная ул.
Тополиная ул.
Тракторная ул.
Тракторный пер.
Трамплинная ул.
Трифоновская ул.
Труда пер.
Труда ул.
Трудовая ул.
Трудовой п.
Тульская ул.
Тульский пер.
Тульский пр.
Турбостроителей ул.
Турынинская ул.
Турынинские Дворики ул.
Удачная ул.
Учхоз ул.
Фабричный пер.
Фридриха Энгельса пер.
Фридриха Энгельса ул.
Хитровка ул.
Хрустальная ул.
Хуторская ул.
Хуторской пер.
Цветочная ул.
Центральная ул.
Циолковского ул.
Чапаева пер.
Чапаева ул.
Чебышева ул.
Черепичный пер.
Черновская ул.
Черносвитинская ул.
Чернышевского ул.
Чехова ул.
Чижевского ул.
Чистые ключи ул.
Чичерина пер.
Чичерина ул.
Шахтеров пер.
Шахтеров ул.
Широкая ул.
Школьный пр.
Шоссейная ул.
Штрековая ул.
Штрековый пер.
Энергетиков ул.
Энтузиастов б-р
Яновских ул.
Яченская ул.
Яченский пер.
Андреевское д.
Верхняя Вырка д.
Воровая д.
Геологоразведочная партия п.
Георгиевское д.
Горенское с.
Желыбино д.
Животинки д.
Колюпаново д.
Усть-Каменогорская ул.
Колюпановская подстанция п.
1-й Мстихинский пер.
2-й Мстихинский пер.
Варшавская ул.
Горная ул.
Домостроителей пр.
Каменный пр.
Лесная ул.
Мстихинская ул.
Остроленская ул.
Прудный пер.
Радужная ул.
Рябиновая ул.
Светлая ул.
Строителей ул.
Хвойная ул.
Центральная ул.
Набережная ул.
Некрасово с.
Николаева ул.
Широкая ул.
Широкий пер.
Нижняя Вырка д.
1-й Садовый пер.
Набережная ул.
Садовая ул.
Садовый пр.
Советская ул.
Торф ул.
Труда ул.
Лесная ул.
Садовая ул.
Совхозная ул.
Совхозный пер.
Центральная ул.
Школьная ул.
Буровая ул.
Железнодорожная ул.
Микрорайон ул.
Школьная ул.
1-й Новорождественский пер.
2-й Новорождественский пер.
3-й Новорождественский пер.
Новорождественская ул.
Покрова ул.
Рождествено д.
Рождественские пруды ул.
Рождественский пер.
Сивково д.
Сосновый Бор п.
Дачная ул.
Зеленая ул.
Зеленый пер.
Лесная ул.
Совхозная ул.
Тинино д.
Чижовка д.
Шахты п.
Домославская ул.
Животноводов пер.
Молодежная ул.
Новая ул.
Центральная ул.
Школьная ул.
Шопино д.
Бабенки д.
Белая д.
Большая Каменка д.
Горенская ж.-д. ст.
Горенское д.
Сосновая ул.
Городок д.
Зеленый п.
Изотов х.
Карачево д.
Проселочная ул.
Козлово с.
1-й Запрудный пр.
1-й Лесной пр.
2-й Запрудный пр.
2-й Лесной пр.
3-й Лесной пр.
4-й Лесной пр.
5-й Лесной пр.
Крутицы д.
Гагарина ул.
Мирный п.
Железнодорожная ул.
Лесная ул.
Малая Лесная ул.
Муратовка п.
Первомайская ул.
Садовая ул.
Энергетиков ул.
Карьерная ул.
Муратовский щебзавод п.
Никола-Лапиносово д.
Новоселки ул.
Новый п.
Орешково д.
Парижская Коммуна п.
Пригородное лесничество п.
Зеленая ул.
Мира ул.
Молодежная ул.
Московская ул.
Пролетарская ул.
Росва п.
Садовая ул.
Советская ул.
Рябинки п.
Сокорево д.
Спас с.
Западная ул.
Лесная ул.
Привокзальная ул.
Рабочая ул.
Садовая ул.
Советская ул.
Совхозная ул.
Тихонова Пустынь ж.-д. ст.
Центральная ул.
Центральный пер.
Школьная ул.
Южная ул.
Угра д.
Юрьевка д.
Яглово д.
Аргуново д.
Галкино д.
Григоровка д.
Груздово д.
Доможирово д.
Жерело д.
Заречье д.
Ильинка д.
Лесная ул.
Староильинская ул.
Центральная ул.
1-й Усадебный пер.
2-й Усадебный пер.
Верхняя Усадебная ул.
Дмитриева ул.
Канищево д.
Кондрова ул.
Лаврова ул.
Нижняя Усадебная ул.
Новая ул.
Писарева ул.
Стрелецкая ул.
Усадебная ул.
Кесарево д.
Лихун д.
Лобаново д.
Макаровка д.
Малая Каменка д.
Хворостянская ул.
Марьино Д.
Матюнино д.
Новоселки д.
Петрово д.
Починки д.
Рожки п.
Тимошево д.
Уварово д.
Уварово-Починковский карьер п.
        """

        from common.models import GeoCity, Street

        kaluga = GeoCity.objects.get(pk=KALUGA_UUID)

        for n in STREETS.split('\n'):
            n = n.strip()
            if n:
                try:
                    Street.objects.get(city=kaluga, name__iexact=n)
                except Street.DoesNotExist:
                    Street.objects.create(city=kaluga, name=n)


    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'common.agent': {
            'Meta': {'ordering': "['last_name', 'first_name', 'patronymic']", 'object_name': 'Agent', '_ormbases': ['common.Person']},
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agents'", 'to': "orm['common.Organization']"}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Person']", 'unique': 'True', 'primary_key': 'True'})
        },
        'common.bankaccount': {
            'Meta': {'object_name': 'BankAccount'},
            'bankname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'bik': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ks': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Organization']"}),
            'rs': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'common.burial': {
            'Meta': {'object_name': 'Burial', '_ormbases': ['common.Order']},
            'account_book_n': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'acct_num_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'acct_num_str1': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'acct_num_str2': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'doverennost': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Doverennost']", 'null': 'True'}),
            'exhumated_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_sync_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2000, 1, 1, 0, 0)'}),
            'order_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Order']", 'unique': 'True', 'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buried'", 'to': "orm['common.Person']"}),
            'print_info': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'common.cemetery': {
            'Meta': {'ordering': "['name']", 'object_name': 'Cemetery'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_sync_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2000, 1, 1, 0, 0)'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cemetery'", 'to': "orm['common.Organization']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.deathcertificate': {
            'Meta': {'object_name': 'DeathCertificate'},
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            's_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'soul': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Soul']", 'unique': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'zags': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ZAGS']", 'null': 'True'})
        },
        'common.documentsource': {
            'Meta': {'object_name': 'DocumentSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'common.doverennost': {
            'Meta': {'object_name': 'Doverennost'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'doverennosti'", 'to': "orm['common.Agent']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expire': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'common.email': {
            'Meta': {'object_name': 'Email'},
            'e_addr': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'soul': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.env': {
            'Meta': {'object_name': 'Env'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'common.geocity': {
            'Meta': {'unique_together': "(('region', 'name'),)", 'object_name': 'GeoCity'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCountry']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoRegion']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.geocountry': {
            'Meta': {'ordering': "['name']", 'object_name': 'GeoCountry'},
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.georegion': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'GeoRegion'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCountry']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.iddocumenttype': {
            'Meta': {'object_name': 'IDDocumentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'common.impbur': {
            'Meta': {'object_name': 'ImpBur'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bur_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'burial_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cemetery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ImpCem']"}),
            'deadman_pk': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gps_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'seat': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'common.impcem': {
            'Meta': {'object_name': 'ImpCem'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'cem_pk': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'f_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99', 'blank': 'True'}),
            'post_index': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '99', 'blank': 'True'})
        },
        'common.location': {
            'Meta': {'object_name': 'Location'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCity']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCountry']", 'null': 'True', 'blank': 'True'}),
            'flat': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'gps_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'post_index': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoRegion']", 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Street']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.media': {
            'Meta': {'object_name': 'Media'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'soul': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.metro': {
            'Meta': {'ordering': "['city', 'name']", 'object_name': 'Metro'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCity']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.operation': {
            'Meta': {'ordering': "['ordering', 'op_type']", 'object_name': 'Operation'},
            'op_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.order': {
            'Meta': {'object_name': 'Order'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': "orm['common.Soul']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordr_customer'", 'to': "orm['common.Soul']"}),
            'date_fact': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_plan': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'doer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'doerorder'", 'null': 'True', 'to': "orm['common.Soul']"}),
            'is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Operation']"}),
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'nal'", 'max_length': '16'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': "orm['common.Product']"}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordr_responsible'", 'to': "orm['common.Soul']"}),
            'responsible_agent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'orders'", 'null': 'True', 'to': "orm['common.Agent']"}),
            'responsible_customer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ordr_responsible_customer'", 'null': 'True', 'to': "orm['common.Soul']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.ordercomments': {
            'Meta': {'ordering': "['date_of_creation']", 'object_name': 'OrderComments'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Order']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.orderfiles': {
            'Meta': {'object_name': 'OrderFiles'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']", 'null': 'True'}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ofile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Order']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.orderposition': {
            'Meta': {'object_name': 'OrderPosition'},
            'count': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Order']"}),
            'order_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.OrderProduct']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.orderproduct': {
            'Meta': {'object_name': 'OrderProduct'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'measure': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ordering': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.organization': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organization', '_ormbases': ['common.Soul']},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'kpp': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99'}),
            'ogrn': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'soul_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Soul']", 'unique': 'True', 'primary_key': 'True'})
        },
        'common.person': {
            'Meta': {'ordering': "['last_name', 'first_name', 'patronymic']", 'object_name': 'Person', '_ormbases': ['common.Soul']},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Role']", 'through': "orm['common.PersonRole']", 'symmetrical': 'False'}),
            'soul_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Soul']", 'unique': 'True', 'primary_key': 'True'})
        },
        'common.personid': {
            'Meta': {'object_name': 'PersonID'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.IDDocumentType']"}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Person']", 'unique': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.DocumentSource']", 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'common.personrole': {
            'Meta': {'unique_together': "(('person', 'role'),)", 'object_name': 'PersonRole'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'personrole'", 'to': "orm['common.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Role']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.phone': {
            'Meta': {'unique_together': "(('soul', 'f_number'),)", 'object_name': 'Phone'},
            'f_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'soul': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.place': {
            'Meta': {'ordering': "['name']", 'object_name': 'Place', '_ormbases': ['common.Product']},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'area_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'area_str1': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'area_str2': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'cemetery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Cemetery']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gps_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'rooms': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'blank': 'True'}),
            'rooms_free': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'blank': 'True'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'row_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'row_str1': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'row_str2': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'seat': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'seat_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'seat_str1': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'seat_str2': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'})
        },
        'common.product': {
            'Meta': {'ordering': "['name']", 'object_name': 'Product'},
            'measure': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'p_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ProductType']"}),
            'soul': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.productcomments': {
            'Meta': {'ordering': "['date_of_creation']", 'object_name': 'ProductComments'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Product']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.productfiles': {
            'Meta': {'object_name': 'ProductFiles'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']", 'null': 'True'}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'pfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Product']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.producttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProductType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.role': {
            'Meta': {'object_name': 'Role'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'djgroups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orgrole'", 'to': "orm['common.Organization']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.roletree': {
            'Meta': {'object_name': 'RoleTree'},
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rltree_master'", 'to': "orm['common.Role']"}),
            'slave': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rltree_slave'", 'to': "orm['common.Role']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.soul': {
            'Meta': {'ordering': "['uuid']", 'object_name': 'Soul'},
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date_no_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birth_date_no_month': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']", 'null': 'True', 'blank': 'True'}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Location']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.soulproducttypeoperation': {
            'Meta': {'unique_together': "(('soul', 'p_type', 'operation'),)", 'object_name': 'SoulProducttypeOperation'},
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Operation']"}),
            'p_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ProductType']"}),
            'soul': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.street': {
            'Meta': {'ordering': "['city', 'name']", 'unique_together': "(('city', 'name'),)", 'object_name': 'Street'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCity']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'default_cemetery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Cemetery']", 'null': 'True', 'blank': 'True'}),
            'default_city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCity']", 'null': 'True', 'blank': 'True'}),
            'default_country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCountry']", 'null': 'True', 'blank': 'True'}),
            'default_operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Operation']", 'null': 'True', 'blank': 'True'}),
            'default_region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoRegion']", 'null': 'True', 'blank': 'True'}),
            'records_order_by': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'records_per_page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'soul': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Soul']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'common.zags': {
            'Meta': {'ordering': "['name']", 'object_name': 'ZAGS'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']
