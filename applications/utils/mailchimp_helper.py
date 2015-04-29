import mailchimp
from apps.accounts.models import User
from voltbe2.settings import MAILCHIMP_LIST_ID



def add_or_update_to_mailchimp_list(user, mc_list):
    mc_list.subscribe(user.email,
                      {
                          'EMAIL': user.email,
                          'FNAME': user.first_name,
                          'LNAME': user.last_name,
                          'EM_TOTAL': user.total_earthmiles,
                          'EM_BALANCE': user.redeemable_earthmiles,
                          'JOIN_DATE': user.date_joined,
                          'ID': user.id,
                      },
                      double_optin=False,
                      update_existing=True
    )


def add_or_update_single_user(user):
    mc_list = mailchimp.utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
    add_or_update_to_mailchimp_list(user, mc_list)


def update_all_users_in_mailchimp_list():
    user_list = User.objects.filter(is_staff=False).filter(is_superuser=False)
    mc_list = mailchimp.utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)

    for u in user_list:
        add_or_update_to_mailchimp_list(u, mc_list)

