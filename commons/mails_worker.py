from django.shortcuts import render
from svdms.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


def test(recepient, username):
    subject = 'Test mails worker'
    from_email = EMAIL_HOST_USER
    to = recepient

    text_content = 'This is an important message.'
    html_content = render_to_string(
        'email-templates/accounts/test.html', {'username': username})

    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to])

    # msg.attach_file('img/banner.png')
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def registration_success(recepient, username):
    subject = 'THÔNG BÁO ĐĂNG KÝ TÀI KHOẢN ĐẠI LÝ'
    from_email = EMAIL_HOST_USER
    to = recepient

    text_content = 'Thông báo đăng ký thành công.'
    html_content = render_to_string(
        'email-templates/accounts/register-success.html', {'username': username})

    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to])

    # msg.attach_file('img/banner.png')
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def locked_account(recepient, admin, contact, username, reason):
    subject = 'THÔNG BÁO KHÓA TÀI KHOẢN TRUY CẬP HỆ THỐNG'
    from_email = EMAIL_HOST_USER
    to = recepient

    text_content = 'Thông báo đăng ký thành công.'
    html_content = render_to_string(
        'email-templates/accounts/account-locked.html',
        {
            'username': username,
            'reason': reason,
            'admin': admin,
            'contact': contact
        }
    )

    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to])

    msg.attach_alternative(html_content, "text/html")
    msg.send()


def invitation():
    pass


def reset_password():
    # sent after user request a new password
    pass


def request_order_success():
    # sent after agency or manager create a request order, directly to agency's email
    pass


def request_order_confirmed():
    # sent after manager accept request any order
    # need provide informs of person who accepted the request
    pass


def agreed_order_planted_for_delivery():
    # sent after manager plan for delivery order
    pass
