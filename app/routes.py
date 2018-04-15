import requests
import datetime
import os, sys
import json
from app import config as cfg
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import application
from app.models import Customer
from app.forms import LoginForm, ShareForm
from datetime import datetime

@application.template_filter('ctime')
def timectime(s):
    """ Formats a Python timestamp to a human-readable format """
    return datetime.datetime.fromtimestamp(s).strftime('%m/%d/%Y')

@application.template_filter('age')
def calculate_age(born):
    b_date = datetime.strptime(born, '%m/%d/%Y')
    return int((datetime.today() - b_date).days/356)

@application.template_filter('height')
def convert_height(height):
    """ Converts height in inches to feet + inches """
    feet = int(int(height) / 12)
    inches = int(height) - (feet * 12)
    return "%s' %s\"" % (feet, inches)

@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer()
        auth = user.auth(form.access_code.data)
        if not auth:
            flash('Invalid Access Code')
            return redirect(url_for('login'))
        return redirect('/emergency/%s' % user.id)
    return render_template('login.html', title='Medifax Customer Portal Login', form=form)

""" CUSTOMER > Dental """
@application.route('/dental/<user_id>', methods=['GET'])
def customer_dental(user_id):
    url = "%s%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['get'],user_id)
    r = requests.get(url, headers=cfg._AWS['headers'])
    return render_template('customers/dental.html', title='Customer Record | Medifax', data=r.json())

""" CUSTOMER > Insurance """
@application.route('/insurance/<user_id>', methods=['GET'])
def customer_insurance(user_id):
    url = "%s%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['get'],user_id)
    r = requests.get(url, headers=cfg._AWS['headers'])
    return render_template('customers/insurance.html', title='Customer Record | Medifax', data=r.json())

""" CUSTOMER > Share a Link """
@application.route('/share/<user_id>', methods=['GET', 'POST'])
def customer_sharel(user_id):

    # Fetch the customer record.
    url = "%s%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['get'],user_id)
    r = requests.get(url, headers=cfg._AWS['headers'])
    r = r.json()

    form = ShareForm()
    if form.validate_on_submit():
        fullname = "%s %s" % (r['name']['first'], r['name']['last'])
        payload = {
                "email": form.email.data,
                "name": fullname
        }
        payload = json.dumps(payload)
        url = "%s%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['share'],user_id)
        print(url)
        req = requests.post(url, data=payload)
        #print(json.loads(req['body']))
        flash('Your Records were Shared with %s' % form.email.data)
        form.email.data = ''
    return render_template('customers/share.html', title='Share Your Records | Medifax', data=r, form=form)

""" CUSTOMER > Medical """
@application.route('/medical/<user_id>', methods=['GET'])
def customer_medical(user_id):
    url = "%s%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['get'],user_id)
    r = requests.get(url, headers=cfg._AWS['headers'])
    return render_template('customers/medical.html', title='Customer Record | Medifax', data=r.json())

""" CUSTOMER > Emergency """
@application.route('/emergency/<user_id>', methods=['GET'])
def customer_emergency(user_id):
    url = "%s%s%s%s" % (cfg._AWS['customers']['base'],cfg._AWS['status'],cfg._AWS['customers']['get'],user_id)
    r = requests.get(url, headers=cfg._AWS['headers'])
    return render_template('customers/view.html', title='Customer Record | Medifax', data=r.json())

@application.route('/')
@application.route('/index')
def index():
        return redirect(url_for('login'))
