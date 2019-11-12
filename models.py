from django.db import models


# ====================权限相关==================================
# 权限
class Permissions(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    permissions_name = models.FileField(max_length=12, unique=True, verbose_name='权限名称')
    permissions_url = models.FileField(max_length=100, unique=True, verbose_name='权限url')
    permissions_url_function = models.FileField(max_length=100, unique=True, verbose_name='权限url职能')


# ==============人事相关========================================
# 部门表
class Department(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    name = models.FileField(max_length=12, unique=True, blank=True, verbose_name='部门名称')
    department_and_permissions = models.ManyToManyField(to="Permissions", to_field="id", on_delete=models.CASCADE,
                                                        verbose_name='权限与部门多对多关系')


# 员工
class Staff(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    staff_info = models.OneToOneField(to='StaffInfo', to_field="id", on_delete=models.CASCADE,
                                      verbose_name='员工与员工详情一对一关系')
    department_and_staff = models.ManyToManyField(to="Department", to_field="id", on_delete=models.CASCADE,
                                                  verbose_name='员工与部门多对多关系')
    staff_and_permissions = models.ManyToManyField(to="Permissions", to_field="id", on_delete=models.CASCADE,
                                                   verbose_name='权限与员工多对多关系')


# 员工信息
class StaffInfo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    work_number = models.FileField(max_length=12, unique=True, verbose_name='工号')
    password = models.FileField(max_length=12, verbose_name='密码')
    staff_name = models.FileField(max_length=10, verbose_name='员工姓名')
    staff_age = models.FileField(max_length=10, verbose_name='员工年龄')
    staff_gender = models.FileField(max_length=10, verbose_name='员工性别')
    staff_position = models.FileField(max_length=10, verbose_name='员工职位')
    staff_state = models.FileField(max_length=10, choices=((1, '在职'), (2, '办理离职中'), (3, '离职')), verbose_name='员工状态')
    staff_date_birth = models.DateTimeField(verbose_name='员工出生日期')
    staff_induction_date = models.DateTimeField(verbose_name='员工入职时间')
    staff_departure_date = models.DateTimeField(verbose_name='员工离职职时间', blank=True)
    staff_phone = models.FileField(max_length=12, verbose_name='员工联系电话')
    staff_emergency_phone = models.FileField(max_length=12, verbose_name='员工紧急联系电话')
    staff_email = models.EmailField(max_length=20, verbose_name='员工邮箱')
    staff_contract_no = models.EmailField(max_length=20, verbose_name='员工合同编号')
    staff_contract_deadline_date = models.DateTimeField(verbose_name='员工合同截止日期')


# 预约表
class Appointment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    appointment_people = models.FileField(max_length=12, verbose_name='预约人')
    appointment_people_iphone = models.FileField(max_length=12, verbose_name='预约人电话')
    being_appointment_people = models.ManyToManyField(to="Staff", to_field="id", on_delete=models.CASCADE,
                                                      verbose_name='被预约人')
    appointment_date = models.DateTimeField(verbose_name='预约时间')
    apply_date = models.DateTimeField(verbose_name='预约申请时间')
    note = models.FileField(max_length=100, verbose_name='备注')


# ==================仓库=======================================
# 物品类别
class Item_Category(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    category_name = models.CharField(max_length=12, unique=True, verbose_name='物品类别名称')

    def __str__(self):
        return self.category_name


# 物品表
class Items(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    item_name = models.CharField(max_length=21, unique=True, verbose_name='物品名称')
    # 物品表与类别表多对多关系表
    items_and_category = models.ManyToManyField(to="Item_Category", to_field="id", on_delete=models.CASCADE,
                                                verbose_name='物品与类别多对多关系')

    def __str__(self):
        return self.item_name


# 物品详情表
class Item_Details(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    items = models.ForeignKey(to="Items", to_field="id", on_delete=models.CASCADE, verbose_name='物品与物品详情一对多关系')
    item_type = models.CharField(max_length=50, verbose_name='物品型号')
    items_manufacturer = models.CharField(max_length=50, verbose_name='物品厂家', blank=True)
    production_date = models.DateTimeField(verbose_name='生产日期', blank=True)
    period_validity = models.IntegerField(verbose_name='有效期', blank=True)
    quantity = models.IntegerField(verbose_name='数量')
    unit_price = models.FloatField(verbose_name='单价')
    state = models.CharField(max_length=10, verbose_name='状态')


# 出库记录表
class OutStore(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    out_storage_quantity = models.IntegerField(verbose_name='数量')
    out_storage_time = models.DateTimeField(verbose_name='出库时间', blank=True)
    # 物品详情表与出库表多对多关系表
    out_storage_items = models.ManyToManyField(to="Item_Details", to_field="id", on_delete=models.CASCADE,
                                               verbose_name='物品与出库多对多关系')
    get_user = models.ManyToManyField(to="Staff", to_field="id", on_delete=models.CASCADE, verbose_name='物品与领取人多对多关系')
    out_storage_user = models.ManyToManyField(to="Staff", to_field="id", on_delete=models.CASCADE,
                                              verbose_name='物品与出库人多对多关系')
    out_storage_note = models.FileField(max_length=20, verbose_name='物品出库备注')


# 入库记录表
class PutStore(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    # 物品详情表与入库表多对多关系表
    out_storage_items = models.ManyToManyField(to="Item_Details", to_field="id", on_delete=models.CASCADE,
                                               verbose_name='物品与入库多对多关系')
    put_storage_time = models.DateTimeField(verbose_name='入库时间', blank=True)
    procurement = models.ManyToManyField(to="Staff", to_field="id", on_delete=models.CASCADE,
                                         verbose_name='采购人或还物品人多对多关系')
    warehouse_people = models.ManyToManyField(to="Staff", to_field="id", on_delete=models.CASCADE,
                                              verbose_name='入库人与物品多对多关系')
    put_storage_note = models.FileField(max_length=20, verbose_name='物品入库备注', blank=True)
