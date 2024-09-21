from crm import app , db ,bcrypt 
from flask  import render_template , redirect ,url_for ,flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from crm import app , db ,bcrypt ,login_manager
from crm.models import Customer ,Activity ,Stage ,Campaign ,Company ,Negotiation,Record,Visit
from flask import request, redirect, url_for, flash
from crm.forms import VisitForm, CompanyForm,Record_id_Form,RecordForm,DeleteForm,CustomerForm ,ActivityForm ,StageForm ,CampaignForm ,NegotiationForm
from flask import render_template, url_for, flash, redirect, request
from crm.models import User
from crm.forms import LoginForm
from crm.forms import RegistrationForm



@app.route('/')
@login_required  
def home():
    user = User.query.get(current_user.id)    
    # دریافت همه stage_idها
    stages = Stage.query.all()

    # دریافت همه مذاکرات
    negotiations = Negotiation.query.all()

    # ارسال اطلاعات به قالب
    return render_template('home.html', stages=stages, negotiations=negotiations,user=user)







@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # رمز عبور را هش می‌کنیم
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # ساخت شیء جدید از کاربر و ذخیره در دیتابیس
        user = User(name=form.name.data, family=form.family.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        # لاگین کردن کاربر بلافاصله بعد از ثبت‌نام
        login_user(user)
        
        flash('Your account has been created and you are now logged in!', 'success')
        return redirect(url_for('home'))  # هدایت به صفحه اصلی پس از لاگین
    return render_template('register.html', title='Register', form=form)






@app.route("/login", methods=['GET', 'POST'])
def login():
    # اگر کاربر قبلاً لاگین شده باشد، به صفحه خانه هدایت می‌شود
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        # پیدا کردن کاربر بر اساس ایمیل
        user = User.query.filter_by(email=form.email.data).first()

        # بررسی اینکه آیا کاربر وجود دارد و رمز عبور صحیح است یا نه
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')

            # اگر کاربر به صفحه‌ای مشخصی رفته و سپس لاگین کرده، به آن صفحه هدایت شود
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))


@app.route('/customers_ng<int:negotiation_id>', methods=['GET', 'POST'])
@login_required  
def customers_ng(negotiation_id):
    form = CustomerForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            print("Form is valid")
            # دریافت داده‌های فرم
            name = form.name.data
            family = form.family.data
            phone_number = form.phone_number.data
            phone_number_two = form.phone_number_two.data
            phone_number_three = form.phone_number_three.data
            email = form.email.data
            user_id =  current_user.id 
            
            # ایجاد رکورد جدید برای مشتری
            new_customer = Customer(
                name=name, 
                family=family, 
                phone_number=phone_number,
                phone_number_two=phone_number_two,
                phone_number_three=phone_number_three,
                email=email,
                user_id=user_id
            )
            
            # ذخیره در پایگاه داده
            db.session.add(new_customer)
            db.session.commit()
            
            # یافتن مذاکره موجود بر اساس negotiation_id
            negotiation = Negotiation.query.get(negotiation_id)
            if negotiation:
                # اتصال مشتری جدید به مذاکره
                negotiation.customer_id = new_customer.id
                db.session.commit()
                
                # پیام موفقیت
                flash('Customer successfully added and linked to the negotiation!')
                
                # هدایت به صفحه مذاکره
                return redirect(url_for('record_id', negotiation_id=negotiation_id))  # مطمئن شوید که 'record_id' صحیح است
            else:
                flash('Negotiation not found.')
        else:
            # نمایش ارورهای فرم به کاربر
            flash('Please fix the errors in the form.')
            print("Form is invalid")
            print(form.errors)

    # دریافت لیست مشتری‌ها
    customers = Customer.query.all()
    return render_template('customers.html', form=form, customers=customers)




@app.route('/Customers', methods=['GET', 'POST'])
@login_required  
def Customers():
    form = CustomerForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            print("Form is valid")
            # دریافت داده‌های فرم
            name = form.name.data
            family = form.family.data
            phone_number = form.phone_number.data
            phone_number_two = form.phone_number_two.data
            phone_number_three = form.phone_number_three.data
            email = form.email.data
            user_id =  current_user.id 
            
            # ایجاد رکورد جدید برای مشتری
            new_customer = Customer(
                name=name, 
                family=family, 
                phone_number=phone_number,
                phone_number_two=phone_number_two,
                phone_number_three=phone_number_three,
                email=email,
                user_id=user_id
            )
            
            # ذخیره در پایگاه داده
            db.session.add(new_customer)
            db.session.commit()
            
            # پیام موفقیت
            flash('Customer successfully added!')
            
            # کاربر را به صفحه لیست مشتری‌ها بازمی‌گردانیم
            return redirect(url_for('Customers'))
        else:
            # اگر فرم معتبر نیست، ارورها را پرینت کنید
            print("Form is invalid")
            print(form.errors)

    # دریافت لیست مشتری‌ها
    customers = Customer.query.all()
    return render_template('Customers.html', form=form, customers=customers)



@app.route('/customer/update/<int:customer_id>', methods=['GET', 'POST'])
@login_required  
def update_customer(customer_id):
    # پیدا کردن مشتری مورد نظر از پایگاه داده
    customer = Customer.query.get_or_404(customer_id)
    form = CustomerForm()

    if request.method == 'POST' and form.validate_on_submit():
        # بروزرسانی داده‌های مشتری
        customer.name = form.name.data
        customer.family = form.family.data
        customer.phone_number = form.phone_number.data
        customer.phone_number_two = form.phone_number_two.data
        customer.phone_number_three = form.phone_number_three.data
        customer.email = form.email.data
        
        # ذخیره تغییرات در پایگاه داده
        db.session.commit()
        flash('Customer successfully updated!')
        return redirect(url_for('Customers'))

    # پر کردن فرم با داده‌های مشتری برای ویرایش
    form.name.data = customer.name
    form.family.data = customer.family
    form.phone_number.data = customer.phone_number
    form.phone_number_two.data = customer.phone_number_two
    form.phone_number_three.data = customer.phone_number_three
    form.email.data = customer.email

    return render_template('Customers_update.html', form=form, customer=customer)




@app.route('/customer/delete/<int:customer_id>', methods=['POST'])
@login_required  
def delete_customer(customer_id):
    form = DeleteForm()  # استفاده از فرم حذف

    # پیدا کردن مشتری با شناسه مشخص
    customer_to_delete = Customer.query.get_or_404(customer_id)
    
    try:
        # حذف مشتری از پایگاه داده
        db.session.delete(customer_to_delete)
        db.session.commit()
        flash('Customer successfully deleted!')
    except:
        # در صورت بروز خطا در حذف، پیام خطا نشان داده می‌شود
        flash('There was a problem deleting the customer.')

    # بازگشت به صفحه لیست مشتری‌ها
    return redirect(url_for('Customers'))












# روت برای نمایش فرم و ذخیره داده‌های فرم
@app.route('/activity', methods=['GET', 'POST'])
@login_required  
def activity():
    form = ActivityForm()

    if request.method == 'POST' and form.validate_on_submit():
        # دریافت داده‌های فرم
        name = form.name.data
        
        # بررسی تکراری نبودن فعالیت
        existing_activity = Activity.query.filter_by(name=name).first()
        if existing_activity:
            flash('Activity with this name already exists!')
        else:
            # ایجاد رکورد جدید در پایگاه داده
            new_activity = Activity(name=name)
            db.session.add(new_activity)
            db.session.commit()
            flash('Activity successfully added!')

        # کاربر را به صفحه لیست فعالیت‌ها هدایت می‌کنیم
        return redirect(url_for('activity'))

    # دریافت لیست فعالیت‌ها برای نمایش در صفحه
    activities = Activity.query.all()
    return render_template('activity.html', form=form, activities=activities)



@app.route('/activity/update/<int:activity_id>', methods=['GET', 'POST'])
@login_required  
def update_activity(activity_id):
    # پیدا کردن فعالیت موجود بر اساس ID
    activity = Activity.query.get_or_404(activity_id)
    form = ActivityForm()

    if request.method == 'POST' and form.validate_on_submit():
        # بروزرسانی داده‌های فعالیت
        activity.name = form.name.data
        
        try:
            # ذخیره تغییرات در پایگاه داده
            db.session.commit()
            flash('Activity successfully updated!')
            return redirect(url_for('activity'))
        except:
            flash('There was an issue updating the activity')

    # پر کردن فرم با داده‌های فعلی برای ویرایش
    form.name.data = activity.name

    return render_template('update_activity.html', form=form, activity=activity)


import traceback

@app.route('/activity/delete/<int:activity_id>', methods=['POST'])
@login_required  
def delete_activity(activity_id):
    form = DeleteForm()  # استفاده از فرم حذف

    # پیدا کردن فعالیت با شناسه مشخص
    activity_to_delete = Activity.query.get_or_404(activity_id)
    
    try:
        # حذف فعالیت از پایگاه داده
        db.session.delete(activity_to_delete)
        db.session.commit()
        flash('Activity successfully deleted!')
    except Exception as e:
        # در صورت بروز خطا، جزئیات خطا پرینت گرفته می‌شود و پیام خطا نمایش داده می‌شود
        print("Error during deletion:", e)
        print(traceback.format_exc())
        flash('There was a problem deleting the activity.')

    # بازگشت به صفحه لیست فعالیت‌ها
    return redirect(url_for('activity'))


@app.route('/stage', methods=['GET', 'POST'])
@login_required  
def create_stage():
    form = StageForm()

    if request.method == 'POST' and form.validate_on_submit():
        # دریافت داده‌های فرم
        name = form.name.data
        
        # بررسی تکراری نبودن مرحله
        existing_stage = Stage.query.filter_by(name=name).first()
        if existing_stage:
            flash('Stage with this name already exists!')
        else:
            # ایجاد رکورد جدید برای مرحله
            new_stage = Stage(name=name)
            db.session.add(new_stage)
            db.session.commit()
            flash('Stage successfully added!')

        return redirect(url_for('create_stage'))

    # دریافت لیست مراحل برای نمایش در صفحه
    stages = Stage.query.all()
    return render_template('stage.html', form=form, stages=stages)


@app.route('/stage/update/<int:stage_id>', methods=['GET', 'POST'])
@login_required  
def update_stage(stage_id):
    # پیدا کردن مرحله مورد نظر بر اساس ID
    stage = Stage.query.get_or_404(stage_id)
    form = StageForm()

    if request.method == 'POST' and form.validate_on_submit():
        # بروزرسانی داده‌های مرحله
        stage.name = form.name.data
        
        try:
            # ذخیره تغییرات در پایگاه داده
            db.session.commit()
            flash('Stage successfully updated!')
            return redirect(url_for('create_stage'))
        except:
            flash('There was an issue updating the stage')

    # پر کردن فرم با داده‌های فعلی
    form.name.data = stage.name

    return render_template('update_stage.html', form=form, stage=stage)



@app.route('/stage/delete/<int:stage_id>', methods=['POST'])
@login_required  
def delete_stage(stage_id):
    form = DeleteForm()  # استفاده از فرم حذف

    # پیدا کردن مرحله مورد نظر بر اساس ID
    stage = Stage.query.get_or_404(stage_id)
    
    try:
        # حذف مرحله
        db.session.delete(stage)
        db.session.commit()
        flash('Stage successfully deleted!')
    except:
        flash('There was an issue deleting the stage')

    return redirect(url_for('create_stage'))

from flask import request, flash, redirect, url_for, render_template



@app.route('/campaign', methods=['GET', 'POST'])
@login_required  
def create_campaign():
    form = CampaignForm()

    if form.validate_on_submit():
        try:
            # دریافت داده‌های فرم
            name = form.name.data
            description = form.description.data
            user_id =  current_user.id 

            # ایجاد رکورد جدید برای کمپین
            new_campaign = Campaign(
                name=name, 
                description=description,
                user_id=user_id
            )
            db.session.add(new_campaign)
            db.session.commit()
            flash('Campaign successfully added!')

            return redirect(url_for('create_campaign'))
        except Exception as e:
            print(f"Error while saving campaign: {e}")
            flash('An error occurred while saving the campaign.')

    else:
        # پرینت خطاهای فرم در صورت نامعتبر بودن فرم
        print("Form validation errors:", form.errors)

    campaigns = Campaign.query.all()
    return render_template('campaign.html', form=form, campaigns=campaigns)







@app.route('/campaign/update/<int:campaign_id>', methods=['GET', 'POST'])
@login_required  
def update_campaign(campaign_id):
    # پیدا کردن کمپین مورد نظر بر اساس ID
    campaign = Campaign.query.get_or_404(campaign_id)
    form = CampaignForm()

    if request.method == 'POST' and form.validate_on_submit():
        # بروزرسانی داده‌های کمپین
        campaign.name = form.name.data
        campaign.description = form.description.data
        
        try:
            db.session.commit()
            flash('Campaign successfully updated!')
            return redirect(url_for('create_campaign'))
        except:
            flash('There was an issue updating the campaign')

    # پر کردن فرم با داده‌های فعلی کمپین برای ویرایش
    form.name.data = campaign.name
    form.description.data = campaign.description

    return render_template('update_campaign.html', form=form, campaign=campaign)
 
 
 
 
@app.route('/campaign/delete/<int:campaign_id>', methods=['POST'])
@login_required  
def delete_campaign(campaign_id):
    form = DeleteForm()  # استفاده از فرم حذف

    # پیدا کردن کمپین مورد نظر بر اساس ID
    campaign = Campaign.query.get_or_404(campaign_id)

    try:
        # حذف کمپین از دیتابیس
        db.session.delete(campaign)
        db.session.commit()
        flash('Campaign successfully deleted!')
    except:
        db.session.rollback()  # در صورت بروز خطا، عملیات به عقب برگردانده می‌شود
        flash('There was an issue deleting the campaign')

    return redirect(url_for('create_campaign'))


@app.route('/company_ng<int:negotiation_id>', methods=['GET', 'POST'])
@login_required  
def create_company_ng(negotiation_id):
    form = CompanyForm()

    if request.method == 'POST' and form.validate_on_submit():
        # دریافت داده‌های فرم
        name = form.name.data
        address = form.address.data
        phone_number = form.phone_number.data
        phone_number_two = form.phone_number_two.data
        phone_number_three = form.phone_number_three.data
        fax = form.fax.data
        website = form.website.data
        email = form.email.data
        user_id = current_user.id 

        # ایجاد رکورد جدید برای شرکت
        new_company = Company(
            name=name,
            address=address,
            phone_number=phone_number,
            phone_number_two=phone_number_two,
            phone_number_three=phone_number_three,
            fax=fax,
            website=website,
            email=email,
            user_id=user_id
        )
        db.session.add(new_company)
        db.session.commit()
        flash('Company successfully added!')

        # یافتن مذاکره موجود بر اساس negotiation_id
        negotiation = Negotiation.query.get(negotiation_id)
        if negotiation:
            # در اینجا فرض می‌کنیم که قصد دارید مشتری جدیدی اضافه کنید
            # اگر مشتری وجود داشته باشد، به مذاکره متصل کنید
            # به کد زیر نگاه کنید که نیاز دارید برای مشتری نیز تعریف کنید
            # customer_id باید با شناسه مشتری جدید متصل شود
            # برای این مثال فرض می‌کنیم customer_id موجود است
            negotiation.company_id = new_company.id
            db.session.commit()
            
            # پیام موفقیت
            flash('Customer successfully linked to the negotiation!')
        
        return redirect(url_for('record_id', negotiation_id=negotiation_id))

    # دریافت لیست شرکت‌ها برای نمایش در صفحه
    companies = Company.query.all()
    return render_template('company.html', form=form, companies=companies)




@app.route('/company', methods=['GET', 'POST'])
@login_required  
def create_company():
    form = CompanyForm()

    if request.method == 'POST' and form.validate_on_submit():
        # دریافت داده‌های فرم
        name = form.name.data
        address = form.address.data
        phone_number = form.phone_number.data
        phone_number_two = form.phone_number_two.data
        phone_number_three = form.phone_number_three.data
        fax = form.fax.data
        website = form.website.data
        email = form.email.data
        user_id =  current_user.id 

        # ایجاد رکورد جدید برای شرکت
        new_company = Company(
            name=name,
            address=address,
            phone_number=phone_number,
            phone_number_two=phone_number_two,
            phone_number_three=phone_number_three,
            fax=fax,
            website=website,
            email=email,
            user_id=user_id
        )
        db.session.add(new_company)
        db.session.commit()
        flash('Company successfully added!')

        return redirect(url_for('create_company'))

    # دریافت لیست شرکت‌ها برای نمایش در صفحه
    companies = Company.query.all()
    return render_template('company.html', form=form, companies=companies)



@app.route('/company/update/<int:company_id>', methods=['GET', 'POST'])
@login_required  
def update_company(company_id):
    # پیدا کردن شرکت بر اساس ID
    company = Company.query.get_or_404(company_id)
    form = CompanyForm()

    if request.method == 'POST' and form.validate_on_submit():
        # بروزرسانی داده‌های شرکت
        company.name = form.name.data
        company.address = form.address.data
        company.phone_number = form.phone_number.data
        company.phone_number_two = form.phone_number_two.data
        company.phone_number_three = form.phone_number_three.data
        company.fax = form.fax.data
        company.website = form.website.data
        company.email = form.email.data
        
        try:
            db.session.commit()
            flash('Company successfully updated!')
            return redirect(url_for('create_company'))
        except:
            flash('There was an issue updating the company')

    # پر کردن فرم با داده‌های فعلی برای ویرایش
    form.name.data = company.name
    form.address.data = company.address
    form.phone_number.data = company.phone_number
    form.phone_number_two.data = company.phone_number_two
    form.phone_number_three.data = company.phone_number_three
    form.fax.data = company.fax
    form.website.data = company.website
    form.email.data = company.email

    return render_template('update_company.html', form=form, company=company)


@app.route('/company/delete/<int:company_id>', methods=['POST'])
@login_required  
def delete_company(company_id):
    form = DeleteForm()  # استفاده از فرم حذف

    # پیدا کردن شرکت بر اساس ID
    company = Company.query.get_or_404(company_id)
    
    try:
        # حذف شرکت
        db.session.delete(company)
        db.session.commit()
        flash('Company successfully deleted!')
    except:
        flash('There was an issue deleting the company')

    return redirect(url_for('create_company'))






@app.route('/negotiation', methods=['GET', 'POST'])
@login_required  
def create_negotiation():
    form = NegotiationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            print("Form is valid")
            # دریافت داده‌های فرم
            topic = form.topic.data
            company_id = form.company_id.data.id if form.company_id.data else None
            customer_id = form.customer_id.data.id if form.customer_id.data else None
            amount = form.amount.data
            done = form.done.data
            stage_id = form.stage_id.data.id
            priority = form.priority.data
            campaign_id = form.campaign_id.data.id if form.campaign_id.data else None
            user_id =  current_user.id 

            # ایجاد رکورد جدید برای مذاکره
            new_negotiation = Negotiation(
                topic=topic,
                company_id=company_id,
                customer_id=customer_id,
                amount=amount,
                done=done,
                stage_id=stage_id,
                priority=priority,
                campaign_id=campaign_id,
                user_id=user_id
            )
            
            db.session.add(new_negotiation)
            db.session.commit()
            flash('Negotiation successfully added!')
        else:
            # اگر فرم معتبر نیست، ارورها را پرینت کنید
            print("Form is invalid")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")

    # نمایش فرم
    Negotiations = Negotiation.query.all()
    return render_template('negotiation.html', form=form, Negotiations=Negotiations)







@app.route('/negotiation/update/<int:negotiation_id>', methods=['GET', 'POST'])
@login_required  
def update_negotiation(negotiation_id):
    negotiation = Negotiation.query.get_or_404(negotiation_id)
    form = NegotiationForm(obj=negotiation)

    if form.validate_on_submit():
        # بروزرسانی داده‌های مذاکره
        negotiation.topic = form.topic.data
        negotiation.company_id = form.company_id.data.id  if form.company_id.data else None
        negotiation.customer_id = form.customer_id.data.id  if form.customer_id.data else None
        negotiation.amount = form.amount.data
        negotiation.done = form.done.data
        negotiation.stage_id = form.stage_id.data.id
        negotiation.priority = form.priority.data
        negotiation.campaign_id = form.campaign_id.data.id if form.campaign_id.data else None
        
        db.session.commit()
        flash('Negotiation successfully updated!')
        return redirect(url_for('create_negotiation'))

    return render_template('negotiation_update.html', form=form, negotiation=negotiation)




@app.route('/negotiation/delete/<int:negotiation_id>', methods=['POST'])
@login_required  
def delete_negotiation(negotiation_id):
    form = DeleteForm()  # استفاده از فرم حذف
    if form.validate_on_submit():
        negotiation = Negotiation.query.get_or_404(negotiation_id)
        try:
            db.session.delete(negotiation)
            db.session.commit()
            flash('Negotiation successfully deleted!')
        except:
            flash('There was an issue deleting the negotiation')
        return redirect(url_for('create_negotiation'))



@app.route('/record', methods=['GET', 'POST'])
@login_required  
def create_record():
    form = RecordForm()

    if form.validate_on_submit():
        try:
            # دریافت داده‌های فرم
            negotiation_id = form.negotiation_id.data.id  # دریافت شناسه مذاکره
            activity_id = form.activity_id.data.id        # دریافت شناسه فعالیت
            note = form.note.data
            user_id = current_user.id 

            # ایجاد رکورد جدید برای Record
            new_record = Record(
                negotiation_id=negotiation_id,
                activity_id=activity_id,
                note=note,
                user_id=user_id
            )
            db.session.add(new_record)
            db.session.commit()

            flash('Record successfully added!', 'success')
            return redirect(url_for('create_record'))

        except Exception as e:
            db.session.rollback()  # اگر خطا رخ داد، تراکنش بازگردانده شود
            flash(f'An error occurred: {str(e)}', 'danger')

    # دریافت لیست رکوردها برای نمایش در صفحه
    records = Record.query.all()
    return render_template('record.html', form=form, records=records)

@app.route('/record_id/<int:negotiation_id>', methods=['GET', 'POST'])
@login_required  
def record_id(negotiation_id):
    form = Record_id_Form()
    form_Visit = VisitForm()


    if form.validate_on_submit():
        try:
            # دریافت داده‌های فرم
            activity_id = form.activity_id.data.id  # دریافت شناسه فعالیت
            note = form.note.data
            user_id =  current_user.id 

            # ایجاد رکورد جدید برای Record
            new_record = Record(
                negotiation_id=negotiation_id,  # شناسه مذاکره مستقیماً از URL گرفته می‌شود
                activity_id=activity_id,
                note=note,
                user_id=user_id
            )
            db.session.add(new_record)
            db.session.commit()

            flash('Record successfully added!', 'success')
            return redirect(url_for('record_id', negotiation_id=negotiation_id))

        except Exception as e:
            db.session.rollback()  # اگر خطا رخ داد، تراکنش بازگردانده شود
            flash(f'An error occurred: {str(e)}', 'danger')

    else:
        # بررسی و چاپ خطاهای فرم
        print("Form did not validate.")
        if form.errors:
            for field, errors in form.errors.items():
                print(f"Errors in {field}: {errors}")  # پرینت خطاهای فرم
                for error in errors:
                    flash(f"Error in the {getattr(form, field).label.text} field - {error}", 'danger')

    # دریافت مذاکره مورد نظر به همراه مشتری، شرکت و اطلاعات ویزیت
    negotiation = Negotiation.query.filter_by(id=negotiation_id).first()

    # بررسی اگر مذاکره موجود باشد
    if negotiation:
        customer = negotiation.customer
        company = negotiation.company
        records = Record.query.filter_by(negotiation_id=negotiation_id).all() 
        visits = Visit.query.filter_by(negotiation_id=negotiation_id).all()  # دریافت تمام ویزیت‌های مرتبط با مذاکره

        # ارسال داده‌ها به قالب
        return render_template(
            'record_id.html',
            form=form,
            form_Visit=form_Visit,
            records=records,
            negotiation=negotiation,
            customer=customer,
            company=company,
            visits=visits,
            negotiation_id=negotiation_id  # اضافه کردن negotiation_id به قالب
        )

    else:
        flash('No negotiation found!', 'danger')
        return redirect(url_for('some_other_route'))


@app.route('/record/update/<int:record_id>', methods=['GET', 'POST'])
@login_required  
def update_record(record_id):
    # پیدا کردن رکورد بر اساس ID
    record = Record.query.get_or_404(record_id)
    form = RecordForm()

    if form.validate_on_submit():
        # بروزرسانی داده‌های رکورد
        record.activity_id = form.activity_id.data
        record.note = form.note.data
        
        try:
            db.session.commit()
            flash('Record successfully updated!')
            return redirect(url_for('create_record'))
        except:
            flash('There was an issue updating the record')

    # پر کردن فرم با داده‌های فعلی رکورد برای ویرایش
    form.activity_id.data = record.activity_id
    form.note.data = record.note

    return render_template('update_record.html', form=form, record=record)


@app.route('/record/delete/<int:record_id>', methods=['POST'])
@login_required  
def delete_record(record_id):
    # پیدا کردن رکورد بر اساس ID
    record = Record.query.get_or_404(record_id)

    try:
        # حذف رکورد از دیتابیس
        db.session.delete(record)
        db.session.commit()
        flash('Record successfully deleted!')
    except:
        db.session.rollback()  # در صورت بروز خطا، عملیات به عقب برگردانده می‌شود
        flash('There was an issue deleting the record')

    return redirect(url_for('create_record'))


@app.route('/create_visit/<int:negotiation_id>', methods=['GET', 'POST'])
@login_required  
def create_visit(negotiation_id):
    form = VisitForm()  # Ensure VisitForm is used here

    if form.validate_on_submit():
        visit_date = form.visit_date.data
        new_visit = Visit(
            visit_date=visit_date,
            negotiation_id=negotiation_id
        )
        db.session.add(new_visit)
        db.session.commit()
        flash('Visit successfully added!')
        return redirect(url_for('record_id', negotiation_id=negotiation_id))

    return redirect(url_for('record_id', negotiation_id=negotiation_id))



@app.route('/visit/delete/<int:visit_id>/<int:negotiation_id>', methods=['POST'])
@login_required  
def delete_visit(visit_id,negotiation_id):
    form = DeleteForm()
    
    # پیدا کردن بازدید بر اساس ID
    visit = Visit.query.get_or_404(visit_id)

    if form.validate_on_submit():  # بررسی صحت فرم
        try:
            # حذف بازدید از دیتابیس
            db.session.delete(visit)
            db.session.commit()
            flash('Visit successfully deleted!')
        except:
            db.session.rollback()  # در صورت بروز خطا، عملیات به عقب برگردانده می‌شود
            flash('There was an issue deleting the visit')
    else:
        flash('Form validation failed')

    return redirect(url_for('record_id', negotiation_id=negotiation_id))
