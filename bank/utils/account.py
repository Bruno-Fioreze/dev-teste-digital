from bank.models import Account, User

class AccountUtils:
    
    @staticmethod
    def create_new_account(user: User ) -> int:
        number_account = Account.objects.count() + 1
        account = Account(agency=1, account=number_account, user=user, saldo=0.00, )
        account.save()
        pk_account = account.pk
        return  pk_account 
    